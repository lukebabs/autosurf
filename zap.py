import time
from pprint import pprint
from zapv2 import ZAPv2
from stem import Signal
from stem.control import Controller

def switch_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="hdfwgufbowhrh234fbhdg")
        controller.signal(Signal.NEWNYM)
        controller.close()

se_lab = ['api.topplayers.pro','superveda.impervademo.com', 'acme.impervademo.com', 'isbt.impervademo.com']

i = 0
while i < 100:
    for site in se_lab:
        target = str("http://"+site)
        print (target)
        apikey = 'Webco123Webco' # Change to match the API key set in ZAP, or use None if the API key is disabled
        #
        # By default ZAP API client will connect to port 8080
        zap = ZAPv2(apikey=apikey)
        # Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
        # zap = ZAPv2(apikey=apikey, proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

        # Proxy a request to the target so that ZAP has something to deal with
        print('Accessing target {}'.format(target))
        zap.urlopen(target)
        # Give the sites tree a chance to get updated
        switch_ip()
        time.sleep(2)

        print('Spidering target {}'.format(target))
        scanid = zap.spider.scan(target)
        # Give the Spider a chance to start
        time.sleep(2)
        while (int(zap.spider.status(scanid)) < 100):
            # Loop until the spider has finished
            print('Spider progress %: {}'.format(zap.spider.status(scanid)))
            switch_ip()
            time.sleep(2)

        print ('Spider completed')

        while (int(zap.pscan.records_to_scan) > 0):
            print ('Records to passive scan : {}'.format(zap.pscan.records_to_scan))
            time.sleep(2)

        print ('Passive Scan completed')

        print ('Active Scanning target {}'.format(target))
        scanid = zap.ascan.scan(target)
        while (int(zap.ascan.status(scanid)) < 100):
            # Loop until the scanner has finished
            print ('Scan progress %: {}'.format(zap.ascan.status(scanid)))
            switch_ip()
            time.sleep(5)

        print ('Active Scan completed')

        # Report the results

        print ('Hosts: {}'.format(', '.join(zap.core.hosts)))
        print ('Alerts: ')
        pprint (zap.core.alerts())
        switch_ip()
        time.sleep(600)
    i +=1
