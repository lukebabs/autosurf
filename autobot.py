###########MOVED TO WAFAUTOBOT#############
# from sys import argv
# import time
# import os
# from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys
# import sys, getopt
# import validators

# def main():
#     url = ''
#     trials = ''
#     driver_path = ''
#     try:
#         opts, args = getopt.getopt(sys.argv[1:],"H:t:d:")
#         for opt, arg in opts:
#             if opt == '-H':
#                 url = str(arg)
#                 if validators.url(url):
#                     continue
#                 else:
#                     print ("Enter a FQDN host e.g. http://domain.com")
#                     return
#             elif opt == '-t':
#                 try:
#                     trials = int(arg)
#                 except ValueError:
#                     print ("Enter a valid number for trials")
#             elif opt == '-d':
#                 driver_path = str(arg)
#     except getopt.GetoptError as e:
#         print (e, 'python autosurf.py -H <Host> -t <No of Trials> -d <selenium driver path>')
#         sys.exit(2)
#     return url, trials, driver_path

#     # #Start automated browsing after validating the url

#     # if validators.url(url) and trials > 0:
#     #     auto_surf(url, trials)
#     # else:
#     #     print ("Check the innput parameters for url and no. of trials")
#     #     print ('python autosurf.py -H <Host> -i <No of Trials>')

# def set_driver(url, driver_path):
#     option = webdriver.ChromeOptions()
#     option.add_argument("-incognito")
#     print (driver_path)
#     browser = webdriver.Chrome(executable_path="./chromedriver", options=option)
#     print (f'{browser}')
#     # print ("set",driver_path)
#     # browser = webdriver.Chrome(executable_path=path+"/chromedriver", options=option)
#     # # browser.get(url)
#     # return browser


#     # specify_path = str(input("Enter Selenium driver full path :"))
#     # driver_path = driver_path
#     # try:
#     #     '''Provide the path for the driver that is required to connect with local broswer
#     #     By default, it is assumed that Chrome is install on the test machine.
#     #     With driver downloaded from https://chromedriver.chromium.org/
#     #     and placed inside /usr/bin/local on a mac. For Windows, simply change the path'''
        
#     #     browser = webdriver.Chrome(executable_path=driver_path, options=option)
#     #     return browser
#     #     # print (browser)
#     # except:
#     #     print ("Place driver for browser in /usr/local/bin. This can be downloaded from https://chromedriver.chromium.org/")
#     #     return

# def login(url, driver_path):
#     driver_path = f"""\"{driver_path}\""""
#     driver = set_driver(url, driver_path)
#     # set_driver(url, driver_path)
#     # print ("test", driver)
#     # driver.get(url)
#     # try:
#     #     time.sleep(2)
#     #     driver.find_element_by_name('username').send_keys("random")
#     #     element = driver.find_element_by_name('password')
#     #     element.send_keys('bad_password')
#     #     element.send_keys(Keys.RETURN)
#     #     driver.close()
#     # except:
#     #     time.sleep(1) #slight delay to closely simulate a real browser
#     #     print(driver.get_network_conditions)
#     #     driver.close()
#     #     return

# def auto_surf(url, trials, driver_path):
#     n = 1
#     while n <= trials:
#         login(url, driver_path)
#         n += 1
#         print (f'Round {n-1} of {trials} automated browsing of {url}')


# def cred_spray():
#     with open('./data/accounts.txt', 'r') as f:
#         for line in f:
#             combo = line.strip('\r\n').split(':')
#             username = combo[0]
#             password = combo[1]

#             params = {
#                 'username': username,
#                 'password': password,
#             }
#             # response = requests.get(
#             #     'http://localhost:5000/login', params=params)
#             # if response.content == 'SUCCESS':
#             #     print response.content, ' --> ', username, ':', password
#             print (params)

# if __name__ == "__main__":
#     url, trial, driver_path = main()
#     auto_surf(url, trial, driver_path)
#     # cred_spray() #Still under development. Will introduce multithreading