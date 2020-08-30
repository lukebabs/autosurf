import time
import os
import platform
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
import sys, getopt
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import validators
import pandas as pd

def main():
    url = ''
    trials = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:],"u:t:")
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
        auto_surf(url, trials)
    else:
        print ("Check the input parameters for url and no. of trials")
        print ('python wafautosurf.py -u <Host URL> -t <No of Trials>')

def select_browser():
    option = webdriver.ChromeOptions()
    option.add_argument("-incognito")
    plt = platform.system()
    try:
        '''Drivers downloaded from https://chromedriver.chromium.org/
        and placed inside ./drivers/ or .\drivers\.'''
        if plt == 'Darwin':
            browser = webdriver.Chrome(executable_path="./drivers/chromedriver", options=option)
            return browser
        elif plt == 'Linux':
            browser = webdriver.Chrome(executable_path="./drivers/chromedriver-2", options=option)
            return browser
        elif plt == 'Windows':
            browser = webdriver.Chrome(executable_path=".\drivers\chromedriver.exe", options=option)
            return browser
    except:
        print ("Place driver for browser in /usr/local/bin. This can be downloaded from https://chromedriver.chromium.org/")
        return

def login(username, password):
    driver = select_browser()
    driver.get (url)
    try:
        time.sleep(2)
        driver.find_element_by_name('username').send_keys(username)
        element = driver.find_element_by_name('password')
        element.send_keys(password)
        element.send_keys(Keys.RETURN)
        # driver.close()
    except:
        time.sleep(1) #slight delay to closely simulate a real browser
        print("Tried {} as username and {} as password".format(username, password))
        # driver.close()
        return

def scrape_data(url):
    driver = select_browser()
    driver.get(url)
    time.sleep(1)

    
# Find the first table on the page and start scraping - 
# not too sophisticated but should be good enough for illustration
    '''Start the browser, input a search, and look for tables
    In this example, we are using AAPL as the input criteria'''
    try:
        element = driver.find_element_by_name('ticker')
        element.send_keys("AAPL")
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()

    # Find table on the page and start scraping
        tab_data = soup.select('table')[1]

        #Parse the data from the table to CSV using pandas library
        n = 0
        item = []
        scraped_data = "./data/scraped.csv"
        while n <= 5: #Scrape the first 5 rows (this is enough for illustration)
            for items in tab_data.select('tr'):
                item = [elem.text for elem in items.select('th,td')]
                item.append
            n += 1
            print (item)
            df = pd.DataFrame(item)
            df.to_csv(scraped_data, index=False, header=False)
    except ValueError as e:
        print (e, "**ALERT** wafautobot could not access the page. Check that the site is active")


def auto_surf(url, trials):
    n = 1
    while n <= trials:
        scrape_data(url)
        n += 1
        print (f'Round {n-1} of {trials} automated browsing of {url}')

def cred_spray():
    #Grap credentials from specified file and use for padding
    with open('./data/accounts.txt', 'r') as f:
        for line in f:
            combo = line.strip('\r\n').split(':')
            username = combo[0]
            password = combo[1]

            # params = {
            #     'username': username,
            #     'password': password,
            # }
            login(username, password)
        return

def menu():
    menu=True
    while menu:
        print("""
        ** Caution: Still under development.
        This tool is not intended to be used for nefarious activities.
        The solve purpose of its inception is to measure show the value of in-depth web application security

        1. Automated Human-like Surfing - under construction
        2. Scrape Content - scrapes tables
        3. Credential Stuffing Attack - under construction
        4. Exit/Quit
        """)

        menu=input("What would you like to do? ")
        if menu=="1":
            print("\nLaunching Automated Surfing")
            main()
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