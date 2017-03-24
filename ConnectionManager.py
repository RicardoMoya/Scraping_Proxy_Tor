# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

import time
import urllib2
import Const as c
from stem import Signal
from stem.control import Controller


class ConnectionManager:
    def __init__(self):
        self.new_ip = c.FIRST_IP
        self.old_ip = c.FIRST_IP
        self.new_identity()

    @classmethod
    def _get_connection(self):
        """
        TOR new connection
        """
        with Controller.from_port(port=c.CONTROL_PORT_TOR) as controller:
            controller.authenticate(password=c.PASS_TOR)
            controller.signal(Signal.NEWNYM)
            controller.close()

    @classmethod
    def _set_url_proxy(self):
        """
        Request to URL through local proxy
        """
        proxy_support = urllib2.ProxyHandler({"http": c.PROXY_HANDLER})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    @classmethod
    def request(self, url):
        """
        TOR communication through local proxy
        :param url: web page to parser
        :return: request
        """
        try:
            self._set_url_proxy()
            request = urllib2.Request(url, None, {'User-Agent': c.USER_AGENT})
            request = urllib2.urlopen(request)
            return request
        except urllib2.HTTPError, e:
            return e.message

    def new_identity(self):
        """
        new connection with new IP
        """
        # First Connection
        if self.new_ip == c.FIRST_IP:
            self._get_connection()
            self.new_ip = self.request(c.URL_GET_IP).read()
        else:
            self.old_ip = self.new_ip
            self._get_connection()
            self.new_ip = self.request(c.URL_GET_IP).read()

        seg = 0

        # If we get the same ip, we'll wait 5 seconds to request a new IP
        while self.old_ip == self.new_ip:
            time.sleep(5)
            seg += 5
            print ("Waiting to obtain new IP: %s Seconds" % seg)
            self.new_ip = self.request(c.URL_GET_IP).read()

        print ("New connection with IP: %s" % self.new_ip)
