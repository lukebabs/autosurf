# autosurf
Web Application Testing Tool - Python3

This tool contains various testing options
1. Bots
2. Stress test - under development
3. Automated browsers - ready to use

# Requirements
The following are the required libraries for the program:
    beautifulsoup4==4.9.1
    bs4==0.0.1
    decorator==4.4.2
    numpy==1.19.1
    pandas==1.1.1
    python-dateutil==2.8.1
    pytz==2020.1
    selenium==3.141.0
    six==1.15.0
    soupsieve==2.0.1
    urllib3==1.25.10
    validators==0.18.0

To automatically install packages, use the following:
    pip3 install -r requirements.txt

# Initial usage
    python3 wafautosurf.py -u https://www.google.com -t 1

    -u = Host URL
    -t = How many session iterations. Setting up a limit helps to control WAF testing in a functional way without turning the exercise into brite force.

# Setting up Selenium
Download full program package which should include two directories - data and drivers.

This package has been setup to provide chrome drivers for Windows, Linux and Mac and automatically select the right chrome driver based on the underlining operating system.

To update the drivers, go to https://chromedriver.chromium.org/ and place the driver under in ./drivers folder for this program package. 

# Human Bot
Added human bot to the toolset. This will be used to scape the site under chrome driver and with time delays to simulate slow surfing by human.

    def humanbot()

