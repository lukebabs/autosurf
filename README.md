# autosurf
Web Application Testing Tool - Python3

This tool is ideal for various bot related use-cases:
1. Automated Humanlike Bots - #Ideal for SuperVeda Classic
2. Simulate Account Take Over, Credential Stuff, etc -  #Ideal for 'Imperva Saving Bank Trust' app
3. Auto scraping with browser - #Ideal for Acme Stock App
4. Basic Load Test - #This is basic generic python-requests. Still under development to make it less obvious as a bot

# Requirements and Prerequisite
This package was tested with Python 3.7.3 IDE

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
    python3 wafautosurf.py -u https://impervademo.com -t 1

    -u = Host URL
    -t = How many session iterations. Setting up a limit helps to control WAF testing in a functional way without turning the exercise into brite force.

    Application menu:
    
        MBP:autosurf$ python3 wafautobot.py -u http://www.zetty.me -t 2

            ** Caution: Still under development.
            This tool is not intended to be used for nefarious activities.
            The solve purpose of its inception is to measure show the value of in-depth web application security

            1. Basic Automated Load Test using Requests - simple load test using 'python requests'
            2. Scrape Content - scrapes tables
            3. Credential Stuffing Attack - #first configure dictionary in data/accounts.txt
            4. Exit/Quit

# Permissions for Selenium
Be aware that you may have to give Selenium drivers necessary trust permission during the first run. This applies to both Windows and MacOS.

# Human Bot
Added human bot to the toolset. This will be used to scape the site under chrome driver and with time delays to simulate slow surfing by human.

    def humanbot()

