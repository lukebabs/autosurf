import requests
import time
import random
from stem import Signal
from stem.control import Controller

user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:92.0) Gecko/20100101 Firefox/92.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 EdgiOS/46.3.13 Mobile/15E148 Safari/605.1.15'
]

website = str(input("Enter the website > "))
def get_current_ip():
    session = requests.session()

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'
    
    #website = str(input("Enter the website > "))
    try:
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent':user_agent}
        url = "http://"+website
        r = session.get(url, headers=headers)
    except Exception as e:
        print (str(e))
    else:
        return

# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    fp.update_preferences()
    options = Options()
    options.headless = True
    return webdriver.Firefox(options=options, firefox_profile=fp)


def renew_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="hdfwgufbowhrh234fbhdg")
        controller.signal(Signal.NEWNYM)
        controller.close()

if __name__ == "__main__":
    for i in range(100):
        print (get_current_ip())
        #time.sleep(5)
        renew_tor_ip()
        time.sleep(5)