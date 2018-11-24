# -*- coding: utf-8 -*-
__author__ = 'Diego Castro'

import time
import urllib3
import json
from stem import Signal
from stem.control import Controller

class ConnectionManager:
    def __init__(self, requests_per_identity = 10):
        """
        Disable SSL Warnings
        """
        urllib3.disable_warnings()
        
        self.ipify_url = "https://api.ipify.org/?format=json"
        self.new_ip = "0.0.0.0"
        self.old_ip = "0.0.0.0"
        self.requests_done = 0
        self.requests_per_identity = requests_per_identity
        self._new_identity()

    def request(self, url):
        try:
            if self.requests_done >= self.requests_per_identity:
                print ("Reached the maximum request using ip %s" % self.new_ip)
                self._new_identity()
      
            print ("Requesting url '%s' with ip %s (%d/%d requests done)" % (url, self.new_ip, self.requests_done + 1, self.requests_per_identity))
                
            http = urllib3.ProxyManager("http://127.0.0.1:8118")
            request = http.request('GET', url, headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/10.10 Chromium/17.0.963.65 Chrome/17.0.963.65 Safari/535.11"
            })
    
            self.requests_done += 1
            
            return request
        except urllib3.exceptions.HTTPError as e:
            return e.message

    def _get_new_connection(self):
        """
        TOR new connection
        """
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="thisismylongpassword")
            controller.signal(Signal.NEWNYM)

    def _get_external_ip(self):
        try:
            http = urllib3.ProxyManager("http://127.0.0.1:8118")
            return json.loads(http.request('GET', self.ipify_url).data.decode('utf-8'))['ip']
        except urllib3.exceptions.HTTPError as e:
            return e.message
    
    def _new_identity(self):
        print ("Getting new identity (currentIp: %s)" % self.new_ip)
        
        if self.new_ip != "0.0.0.0":
            self.old_ip = self.new_ip
            
        self._get_new_connection()
        self.new_ip = self._get_external_ip()
        
        seg = 0

        # If we get the same ip, we'll wait 5 seconds to request a new IP
        while self.old_ip == self.new_ip:
            time.sleep(5)
            seg += 5
            print ("Waiting %s Seconds to obtain new identity..." % seg)
            self.new_ip = self._get_external_ip()

        print ("Obtained new identity with ip: %s" % self.new_ip)
        
        self.requests_done = 0
