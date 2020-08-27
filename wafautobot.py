import time
import os
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
    except getopt.GetoptError as e:
        print (e, 'python wafautosurf.py -u <Host URL> -t <No of Trials>')
        sys.exit(2)

    #Start automated browsing after validating the url
    if validators.url(url) and trials > 0:
        auto_surf(url, trials)
    else:
        print ("Check the innput parameters for url and no. of trials")
        print ('python wafautosurf.py -u <Host URL> -t <No of Trials>')

def set_driver():
    option = webdriver.ChromeOptions()
    option.add_argument("-incognito")
    try:
        '''Provide the path for the driver that is required to connect with local broswer
        By default, it is assumed that Chrome is install on the test machine.
        With driver downloaded from https://chromedriver.chromium.org/
        and placed inside /usr/bin/local on a mac. For Windows, simply change the path'''
        browser = webdriver.Chrome(executable_path="./drivers/chromedriver", options=option)
        return browser
    except:
        print ("Place driver for browser in /usr/local/bin. This can be downloaded from https://chromedriver.chromium.org/")
        return

def login(url):
    driver = set_driver()
    driver.get (url)
    try:
        time.sleep(2)
        driver.find_element_by_name('username').send_keys("random")
        element = driver.find_element_by_name('password')
        element.send_keys('bad_password')
        element.send_keys(Keys.RETURN)
        driver.close()
    except:
        time.sleep(1) #slight delay to closely simulate a real browser
        print(driver.get_network_conditions)
        driver.close()
        return

def humanbot(url):
    driver = set_driver()
    driver.get(url)

    time.sleep(1)

    try:
        element = driver.find_element_by_name('ticker')
        element.send_keys("AAPL")
        element.send_keys(Keys.RETURN)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.quit()
    # Find table on the page and start scraping
        tab_data = soup.select('table')[1]
        n = 0
        item = []
        scraped_data = "./data/scraped.csv"
        while n <= 5:
            for items in tab_data.select('tr'):
                item = [elem.text for elem in items.select('th,td')]
                item.append
            n += 1
            print (item)
            df = pd.DataFrame(item)
            df.to_csv('./data/scraped.csv', index=False, header=False)
    except:
        print ("Could not access the page. Check that for firewalls")


def auto_surf(url, trials):
    n = 1
    while n <= trials:
        # login(url)
        humanbot(url)
        n += 1
        print (f'Round {n-1} of {trials} automated browsing of {url}')


def cred_spray():
    with open('./data/accounts.txt', 'r') as f:
        new_list = []
        for line in f:
            combo = line.strip('\r\n').split(':')
            username = combo[0]
            password = combo[1]

            params = {
                'username': username,
                'password': password,
            }
            new_list.append(params)
        return new_list

def menu():
    menu=True
    while menu:
        print("""
        ** Caution: Still under development.
        This tool is not intended to be used for nefarious activities.
        The solve purpose of its inception is to measure show the value of in-depth web application security

        1. Launch Automated Surfing - under construction
        2. Scrape Content - scrapes tables
        3. Credential Stuffing Attack - under construction
        4. Exit/Quit
        """)
        menu=input("What would you like to do? ")
        if menu=="1":
            print("\nLaunch Automated Surfing")
            main()
        elif menu=="2":
            print("\n Scrape Content")
            main()
        elif menu=="3":
            print("\n Credential Stuffing Attack")
            main()
        elif menu=="4" or "q":
            break
        elif menu == None:
            print("\n Not Valid Choice Try again")

if __name__ == "__main__":
    menu()