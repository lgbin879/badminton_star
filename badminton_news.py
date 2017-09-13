# -*- coding: utf-8 -*-
"""
Created on Sep. 13th 2017
@author: Robin Li
"""

from bs4 import BeautifulSoup
import requests

url='http://sports.sina.com.cn/others/badmin.shtml'

def get_news():
    web_data=requests.get(url)
    web_data.encoding='utf-8'

    soup=BeautifulSoup(web_data.text,'html.parser')

    print("-----today's badminton news-----")

    for news in soup.findAll('ul', class_="list2")[0].getText().split('\n'):
        print(news)
    
    for news in soup.findAll('ul', class_="list2")[1].getText().split('\n'):
        print(news)

if __name__ == "__main__" :
    get_news()


