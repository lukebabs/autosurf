# autosurf
Web Application Testing Tool - Python3

This tool contains various testing options
1. Bots
2. Stress test
3. Automated browsers

# Requirements
    pip install the following:
    1. Selenium
    2. Validators

    i.e.    pip3 install selenium
            pip3 install validators

# Initial usage
    python3 autosurf.py -h https://www.google.com -i 1

    -h = Host URL
    -i = How many session iterations. Setting up a limit helps to control WAF testing in a functional way without turning the exercise into brite force

# Setting up Selenium
Provide the path for the driver that is required to connect with local broswer. By default, it is assumed that Chrome is install on the test machine. With driver downloaded from https://chromedriver.chromium.org/ and placed inside /usr/bin/local on a mac. For Windows, simply change the path to where selenium driver has been downloaded.
