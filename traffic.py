#!/usr/bin/python3
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
    with open('./data/sites.txt') as file:
        sites = [site.strip() for site in file]
    return sites

#This function serves to get user_agents from text file and transform it to a list
def user_agents_list():
    with open('./data/user-agents.txt') as file:
        user_agents = [user_agent.strip() for user_agent in file]  #lambda replacing the newline during extraction
    return user_agents #new list of user_agents in list format

# def pick_user_agent():
#     user_agent = random.choice(get_user_agents)
#     return user_agent

def get_request():
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'
    
    #website = str(input("Enter the website > "))
    try:
        # user_agent = pick_user_agent()
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
    return

#This is the controller responsible for rotating exit IP Address
def switch_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=TOR_KEY) 
        controller.signal(Signal.NEWNYM)
        controller.close()
    return

def start_requests():
    print ("Starting request for " +site)
    use_requests(site)
    return

#Creating multiple threads to scale the events generated
def load_threading():
    r1 = threading.Thread(target=start_requests, args=site)
    # r1 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    # r2 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    # r3 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    # r4 = threading.Thread(target=start_requests, args=(random.choice(sites), 0))
    try:
        r1.start()
        # r2.start()
        # r3.start()
        # r4.start()
    except Exception as e:
        print (e)
    return

if __name__ == "__main__":
    sites = site_list()
    user_agents = user_agents_list()
    while True:
        site = random.choice(sites)
        user_agent = random.choice(user_agents)
        load_threading()
