#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def  printPlistCode():
    jpg = ''
    title = ''
    url = ''
    #循环读取文件中的url链接
    for i in open('/home/worker/prevention/result.txt/pesticide1.txt'):

	urls = 'https://s.1688.com/selloffer/offer_search.htm?keywords=' + i + '&button_click=top&earseDirect=false&n=y&netType=1%2C11'
	href = urls.replace('\n','')
	#break
    	html = urllib2.urlopen(href).read()
    	soup = BeautifulSoup(html,'html.parser')
    	#根据元素标签找到对应的值
    	for div in soup.find_all('div',class_='sm-offer-photo sw-dpl-offer-photo',limit=1):
	    for img in div.find_all('img'):
	    	jpg = img['src']
	    	title = img['alt']
		title = title.replace(',','，')
	    for a in div.find_all('a'):
		url = a['href']
	    data = i + ',' + jpg + ',' + url + ',' + title
	    data = data.replace('\n','')
	    #数据文件
	    with open('/home/worker/prevention/result.txt/pesticide1Result.txt', 'a+') as f:
                    f.write(data+'\n')
                    f.close()
                    print data
        #url 数据文件            
	    with open('/home/worker/prevention/result.txt/url.txt', 'a+') as f:
                    f.write(url+'\n')
                    f.close()
                    

if __name__ == '__main__':
    printPlistCode()

