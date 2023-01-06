import requests
import threading

url = 'https://ecommerce.impvdemo.com/'

# class thread(threading.Thread):
#     def __init__(self, thread_name, thread_ID):
#         threading.Thread.__init__(self)
#         self.thread_name = thread_name
#         self.thread_ID = thread_ID

#     def run(self):
#         print(str(self.thread_name) +" "+ str(self.thread_ID));
 
# thread1 = thread(make_requests, 1000)
# thread2 = thread(make_requests, 2000);

def make_requests():
    i = 0
    while i < 100:
        response = requests.get(url)
        print (response.headers)
        i=+1

if __name__=="__main__":
    make_requests()
