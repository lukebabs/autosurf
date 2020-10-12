# autosurf
Web Application Testing Tool - Python3

This tool is ideal for various bot related use-cases:
1. Automated Humanlike Bots - #This can be used for any website
2. Auto scraping with browser - #Ideal for Acme Stock App
3. Simulate Account Take Over, Credential Stuff, etc -  #Ideal for any site with login url
4. Basic Load Test - #This is basic generic python-requests. Still under development to make it less obvious as a bot

# Requirements and Prerequisite
1. Ensure Firefox and Chrome are installed on the test node
2. This package requires Python3.x
3. Install all the required libraries following the steps below:

**CRITICAL**The following are libraries are required to run the package:

    1. beautifulsoup4==4.9.1
    2. bs4==0.0.1
    3. decorator==4.4.2
    4. numpy==1.19.1
    5. pandas==1.1.1
    6. python-dateutil==2.8.1
    7. pytz==2020.1
    8. selenium==3.141.0
    9. six==1.15.0
    10. soupsieve==2.0.1
    11. urllib3==1.25.10
    12. validators==0.18.0
    13. lxml==4.5.2
    14. requests==2.24.0

To automatically install packages, use the following command:
    
    pip3 install -r requirements.txt

    OR

    pip install -r requirements.txt

# Initial usage
    python3 wafautosurf.py -u https://impervademo.com

    -u = Host URL

    Application menu:
    
        MBP:luke.babarinde$ python3 wafautobot.py -u http://www.zetty.me

            ** Caution: Still under development.
            This tool is not intended to be used for nefarious activities.
            The solve purpose of its inception is to measure show the value of in-depth web application security

            1. Simulate Human-like automated surfing
            2. Basic Automated Load Test using Requests - simple load test using 'python requests'
            3. Scrape Content - scrapes tables
            4. Credential Stuffing Attack - #first configure dictionary in data/accounts.txt
            5. Exit/Quit

# Credential Stuff
When using Option 4 for Credential Stuffing, you are required to provide URL, username parameter name and password parameter name. The credentials are stored in ./data/accounts.txt

        MBP:luke.babarinde$ python3 wafautobot.py -u https://impervademo.com

            ** Caution: Still under development.
            This tool is not intended to be used for nefarious activities.
            It is intended to demonstrate the value of advanced bot protection and WAF

            1. Simulate Human-like automated surfing
            2. Basic Automated Load Test using Requests - simple load test using 'python requests'
            3. Scrape Content - scrapes tables
            4. Credential Stuffing Attack - #first configure dictionary in data/accounts.txt
            5. Exit/Quit
            
        What would you like to do? 4

    Credential Stuffing Attack
    ==>Enter the login url: /isbt/login/
    ==>Enter the username parameter name: username
    ==>Enter the password parameter name: password
    Using chromedriver Driver
    Initial URL https://www.impervademo.com/isbt/login/
    Tried user001@gmail.com and password123


# Permissions for Selenium
Be aware that you may have to give Selenium drivers necessary trust permission for the first run. This applies to both Windows and MacOS. On Linux, simply install Chrome broswer

# Human Bot
Added human bot to the toolset. This can be used to automatically surf a site and click randomly as humans would. This can be good for reconnaissance.

# DB_DECEPTICON
This was added to allow an engineer to generate simple queries against a database server.

The two servers covered are:
1. MSSQL
2. Oracle

* Connecting to MSSQL
To connect the script from Windows, first install ODBC Driver for Windows: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15

On a Mac, use Brew to install the following:
    brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
    brew update
    brew install msodbcsql mssql-tools
    brew install unixodbc

* Connecting to Oracle
1. For MacOS: Download Oracle driver from - https://download.oracle.com/otn_software/mac/instantclient/193000/instantclient-basiclite-macos.x64-19.3.0.0.0dbru.zip. Unpackage the file under: ./driver/mac/oracle (File is too large to be added to git)

2. For Windows: Download the driver from: https://download.oracle.com/otn_software/nt/instantclient/19800/instantclient-basic-windows.x64-19.8.0.0.0dbru.zip. Unpackage the files under - ./driver/windows/oracle

# Thanks
Special thanks for Manny Liwanag for actively testing the script, ideas generation, and for the endless feedback loop to make this fit for purpose.