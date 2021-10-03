#!/usr/bin/python3
from concurrent.futures import thread
import threading
import requests
import time, os
import random
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

TOR_KEY = os.getenv('TOR') #Grab key from .env file

#List all sites to run requests against
def site_list():
    with open('./data/sites.txt') as file:
        sites = [site.strip() for site in file] #function to turn the txt file content into list
    return sites

#Get user_agents from text file and transform it to a list
def get_user_agents():
    with open('./data/user-agents.txt') as file:
        user_agents = [site.strip() for site in file] #function to turn the txt file content into list
    return user_agents #new list of user_agents in list format

def get_request(site):
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'

    #website = str(input("Enter the website > "))
    try:
        user_agent = random.choice(user_agent_list)
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

#This is the controller responsible for rotating TOR exit IP Address
def switch_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password=TOR_KEY) # Password is defined in .env file as TOR_KEY
        controller.signal(Signal.NEWNYM)
        controller.close()

def start_requests(sites, i):
    print ("Starting request for " +sites)
    use_requests(sites)

def load_threading():
    #Setting up for threads to enhance request output
    r1 = threading.Thread(target=start_requests, args=(random.choice(sites),0))
    r2 = threading.Thread(target=start_requests, args=(random.choice(sites),0))
    r3 = threading.Thread(target=start_requests, args=(random.choice(sites),0))
    r4 = threading.Thread(target=start_requests, args=(random.choice(sites),0))
    try:
        r1.start()
        r2.start()
        r3.start()
        r4.start()
    except Exception as e:
        print (e)

if __name__ == "__main__":
    sites = site_list() #Get site list from text file - ./data/sites.txt
    user_agent_list = get_user_agents() #Get user-agents from text - ./data/user-agent.txt
    while True: #Infinite loop to allow the code to run as a service
        load_threading()
        time.sleep(5)