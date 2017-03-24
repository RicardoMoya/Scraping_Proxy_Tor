# -*- coding: utf-8 -*-
__author__ = 'RicardoMoya'

from bs4 import BeautifulSoup
from ConnectionManager import ConnectionManager

URL_BASE = "http://jarroba.com/"
MAX_PAGES = 30
counter_post = 0

cm = ConnectionManager()
for i in range(1, MAX_PAGES):

    # Build URL
    if i > 1:
        url = "%spage/%d/" % (URL_BASE, i)
    else:
        url = URL_BASE
    print (url)

    # Do the request
    req = cm.request(url)
    status_code = req.code if req != '' else -1
    if status_code == 200:
        html = BeautifulSoup(req.read(), "html.parser")
        posts = html.find_all('div', {'class': 'col-md-4 col-xs-12'})
        for post in posts:
            counter_post += 1
            title = post.find('span', {'class': 'tituloPost'}).getText()
            author = post.find('span', {'class': 'autor'}).getText()
            date = post.find('span', {'class': 'fecha'}).getText()
            print (
            str(counter_post) + ' - ' + title + ' | ' + author + ' | ' + date)

    else:
        # if status code is diferent to 200
        break

    # obtain new ip if 5 requests have already been made
    if i % 5 == 0:
        cm.new_identity()
