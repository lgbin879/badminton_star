# -*- coding: utf-8 -*-
"""
Created on Sep. 13th 2017
@author: Robin Li
"""

import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from bs4 import BeautifulSoup
import requests
import time

urls=['http://www.aiyuke.com/sport_players/index----{}.html'.format(str(i)) for i in range(1,10,1)]

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
    'Cookie':'bid="+RZMojI+I84"; ll="118281"; viewed="7056708_10863574_26647176_3288908"; gr_user_id=7758d24b-1ff7-4bfb-aac5-da0cebb3b129; _ga=GA1.2.1164329915.1430920272; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1457141967%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DwlFfuGH8nDDaDfhuElvs2e-927672lPlTf3UP5ra2LVTDrCK1YcFpyYiIAPJcOqq%26wd%3D%26eqid%3D86da232a00235c820000000356da38c0%22%5D; ps=y; ue="alovera@sina.com"; dbcl2="61719891:SKQE4SmJJ7U"; ck="WzE9"; ap=1; push_noty_num=0; push_doumail_num=0; __utma=30149280.1164329915.1430920272.1457093782.1457141968.44; __utmb=30149280.6.10.1457141968; __utmc=30149280; __utmz=30149280.1457141968.44.23.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.6171; __utma=223695111.1164329915.1430920272.1457093782.1457141968.6; __utmb=223695111.0.10.1457141968; __utmc=223695111; __utmz=223695111.1457141968.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.4cf6=051573cd37c5bc0e.1446452093.6.1457142204.1457093853.; _pk_ses.100001.4cf6=*'
}

name=[]
gender=[]
country=[]
group=[]
winloss=[]
ratio=[]
link=[]

length=[]
birthday=[]
horoscope=[]

def allstar(web_url,data=None):    
    web_data=requests.get(web_url)
    soup=BeautifulSoup(web_data.text,'lxml')
    time.sleep(2)

    tags = soup.find_all('li', class_='clearfix')

    for tag in tags:
        print(tag.select('a')[1]['title'].strip()+' : '+tag.select('a')[1]['href'])
        name.append(tag.select('a')[1]['title'].strip())
        gender.append(tag.select('p')[0].get_text().split('\t')[1][0])
        country.append(tag.select('p')[0].get_text().split('\t')[2][0:6].strip())
        group.append(tag.select('p')[0].getText().split('\t')[-1].strip())
        winloss.append(tag.select('p')[1].getText().split('\r')[2].strip().split('\t')[1][0:4].strip()+'/'+tag.select('p')[1].getText().split('\r')[3].strip().split('\t')[1][0:4].strip())
        ratio.append(int(tag.select('p')[1].getText().split('\r')[2].strip().split('\t')[1][0:4].strip())/(int(tag.select('p')[1].getText().split('\r')[2].strip().split('\t')[1][0:4].strip())+int(tag.select('p')[1].getText().split('\r')[3].strip().split('\t')[1][0:4].strip())))
        link.append(tag.select('a')[1]['href'])

        detail_link=tag.select('a')[1]['href']
        detail_info=requests.get(detail_link)
        detail_soup=BeautifulSoup(detail_info.text,'lxml')

        if(len(detail_soup.findAll('div',class_='player_de_top clearfix')[0].findAll('li')[2].getText().split('\r'))>2) :
            length.append(detail_soup.findAll('div',class_='player_de_top clearfix')[0].findAll('li')[2].getText().split('\r')[-2].strip())
        else :
            length.append("")
        
        if(len(detail_soup.findAll('div',class_='player_de_top clearfix')[0].findAll('li'))>1) :
            birthday.append(detail_soup.findAll('div',class_='player_de_top clearfix')[0].findAll('li')[-2].getText().split('\t')[-1].strip())
            horoscope.append(detail_soup.findAll('div',class_='player_de_top clearfix')[0].findAll('li')[-1].getText().split(':')[-1].strip())
        else:
            birthday.append("")
            horoscope.append("")
            
j=0
for sigle_url in urls:
    print("----"+str(j)+"----")
    j+=1
    allstar(sigle_url)
    
data={'姓名':name,
      '性别':gender,
      '身高':length,
      '生日':birthday,
      '星座':horoscope,
      '国家':country,
      '项目':group,
      '战绩':winloss,
      '胜率':ratio,
      'Link':link}

frame=DataFrame(data,columns=[u'姓名',u'性别',u'身高',u'生日',u'星座',u'国家',u'项目',u'战绩', u'胜率', u'Link'])

print('done!!')

#将dataframe数据写入csv或xlsx文件
frame.to_csv('badminton.csv', index=True)
