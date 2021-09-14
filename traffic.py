import requests
import time, re
import random
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup


se_lab = ['superveda.impervademo.com', 'superveda-protected.impervademo.com', 'acme.impervademo.com', 'isbt.impervademo.com']
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


def get_request():
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'
    
    #website = str(input("Enter the website > "))
    try:
        user_agent = pick_user_agent()
        headers = {'User-Agent':user_agent}
        url = "http://"+website
        r = session.get(url, headers=headers)
    except Exception as e:
        print (str(e))
    else:
        return session.cookies

# get a new selenium webdriver with tor as the proxy
def my_proxy(TOR_IP, TOR_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",TOR_IP)
    fp.set_preference("network.proxy.socks_port",int(TOR_PORT))
    fp.update_preferences()
    options = Options()
    options.headless = True
    return webdriver.Firefox(options=options, firefox_profile=fp)

def use_selenium():
    for i in range(1):
        proxy = my_proxy("127.0.0.1", 9050)
        proxy.get("https://whatismyip.com/")
        html = proxy.page_source
        soup = BeautifulSoup(html, 'lxml')
        print(soup.find("span", {"id": "ipv4"}))
        print(soup.find("span", {"id": "ipv6"}))
        proxy.quit()
        switch_ip()

def use_requests():
    for i in range(500):
        result = get_request()
        print ("\n Session Cookie is " + str(result))
        switch_ip()
        time.sleep(5)

#This is the controller responsible for rotating exit IP Address
def switch_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="hdfwgufbowhrh234fbhdg")
        controller.signal(Signal.NEWNYM)
        controller.close()



if __name__ == "__main__":
    for site in se_lab:
        #website = str(input("Enter the website > "))
        website = site
        use_requests()
