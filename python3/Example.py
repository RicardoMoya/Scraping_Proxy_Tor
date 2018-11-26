# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from ConnectionManager import ConnectionManager

cm = ConnectionManager(60)
for j in range(5):
    for i in range(3):
        print ("\t\t" + cm.request("http://icanhazip.com").data.decode('utf-8'))