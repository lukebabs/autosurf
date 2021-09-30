import threading
import requests
import time, re
import random
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup

#List all sites to run requests against

se_lab = ['superveda.impervademo.com', 'acme.impervademo.com', 'isbt.impervademo.com']

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

def use_requests(site):
    for i in range(5):
        result = get_request(site)
        print ("\n Session Cookie is " + str(result))
        switch_ip()
        time.sleep(5)

#This is the controller responsible for rotating exit IP Address
def switch_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="hdfwgufbowhrh234fbhdg")
        controller.signal(Signal.NEWNYM)
        controller.close()

def start_requests(se_lab, i):
    print ("Starting request for " +se_lab)
    use_requests(se_lab)

def load_threading():
    r1 = threading.Thread(target=start_requests, args=(random.choice(se_lab), 0))
    r2 = threading.Thread(target=start_requests, args=(random.choice(se_lab), 0))
#   r3 = threading.Thread(target=start_requests, args=(random.choice(se_lab), 0))
#    r4 = threading.Thread(target=start_requests, args=(random.choice(se_lab), 0))
    try:
        r1.start()
        r2.start()
#        r3.start()
#        r4.start()
    except Exception as e:
        print (e)

if __name__ == "__main__":
    while True:
        load_threading()
