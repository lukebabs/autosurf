import threading
import requests
import time, re, os
import random
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

TOR_KEY = os.getenv('TOR')

#Create list of  sites to run requests against from ./data/sites.txt
def site_list():
    file_list = open('./data/sites.txt').readlines() #Grabs list of sites defined in file
    sites = []
    for i in file_list:
        sites.append(re.sub('\n', '', i)) #removes newline when adding to list
    return sites

#This function serves to get user_agents from text file and transform it to a list
def tranform_user_agent_list():
    file_list = open('./data/user-agents.txt').readlines()
    new_list = []
    for i in file_list:
        new_list.append(re.sub('\n', '', i)) #replacing the newline during extraction
    return new_list #new list of user_agents in list format

def pick_user_agent():
    user_agent_list = tranform_user_agent_list()
    user_agent = random.choice(user_agent_list)
    return (user_agent)

def get_request(site):
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'
    
    #website = str(input("Enter the website > "))
    try:
        user_agent = pick_user_agent()
        headers = {'User-Agent':user_agent}
        url = "http://"+site
        r = session.get(url, headers=headers)
    except Exception as e:
        print (str(e))
    else:
        return session.cookies

def use_requests(sites):
    for i in range(5):
        result = get_request(sites)
        print ("\n Session Cookie is " + str(result))
        switch_ip()
        time.sleep(5)
    return

#This is the controller responsible for rotating exit IP Address
def switch_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=TOR_KEY) 
        controller.signal(Signal.NEWNYM)
        controller.close()
    return

def start_requests(se_lab, i):
    print ("Starting request for " +se_lab)
    use_requests(sites)
    return

#Creating multiple threads to scale the events generated
def load_threading(sites):
    r1 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    r2 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    r3 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    r4 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    try:
        r1.start()
        r2.start()
        r3.start()
        r4.start()
    except Exception as e:
        print (e)
    return

if __name__ == "__main__":
    sites = site_list()
    while True:
        load_threading(sites)
