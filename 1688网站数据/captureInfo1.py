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
    	for url in open('/home/worker/prevention/result.txt/url1.txt'):

	#urls = 'https://detail.1688.com/offer/557382132715.html'
	#href = urls.replace('\n','')
    		html = urllib2.urlopen(url).read()
    		soup = BeautifulSoup(html,'html.parser')

		number1 = ' '
        	price1 = ' '
        	number2 = ' '
        	price2 = ' '
        	number3 = ' '
        	price3 = ' '
        	pesticideNumber = ' '
        	turnover = ' '
		data = ''

        # 因为价位会有三种，不同价位的元素标签也不一样，所以需要三种
		# 如果有3个价位的话，class为ladder-3-1  ladder-3-2 ladder-3-3
    		for td in soup.find_all('td',class_='ladder-3-1'):
			text = td.text
			text = text.replace('\n','').strip()
			if number1 == ' ' :
				number1 = text
			else :
				price1 = text
		
		for td in soup.find_all('td',class_='ladder-3-2'):
                	text = td.text
                	text = text.replace('\n','').strip()
                	if number2 == ' ' :
                        	number2 = text
                	else :
                        	price2 = text

		for td in soup.find_all('td',class_='ladder-3-3'):
                	text = td.text
                	text = text.replace('\n','').strip()
                	if number3 == ' ' :
                        	number3 = text
                	else :
                        	price3 = text
	
		# 如果有2个价位的话，class为ladder-2-1  ladder-2-2
		if number1 == ' ':
			for td in soup.find_all('td',class_='ladder-2-1'):
                		text = td.text
                		text = text.replace('\n','').strip()
                		if number1 == ' ' :
                        		number1 = text
                		else :
                        		price1 = text

        		for td in soup.find_all('td',class_='ladder-2-2'):
                		text = td.text
                		text = text.replace('\n','').strip()
                		if number2 == ' ' :
                        		number2 = text
                		else :
                        		price2 = text	


		# 如果有1个价位的话，class为ladder-1-1
		if number1 == ' ':
                	for td in soup.find_all('td',class_='ladder-1-1'):
                        	text = td.text
                        	text = text.replace('\n','').strip()
                        	if number1 == ' ' :
                                	number1 = text
                        	else :
                                	price1 = text
	

		data = price1 + ',' + number1  + ',' + price2 + ',' + number2 + ',' + price3  + ',' + number3 + ','
	
		for a in soup.find_all('a',class_='officaldoc-link',limit=1):
			pesticideNumber = a.string.replace('\n','').strip() + ','

		for p in soup.find_all('p',class_='bargain-number'):
			turnover = p.text.replace('\n','').strip() 

		line = pesticideNumber + data + turnover 
		#将数据写入文件中
        	with open('/home/worker/prevention/result.txt/0212.txt', 'a+') as f:
        		f.write(line+'\n')
                	f.close()
                	print line

if __name__ == '__main__':
	printPlistCode()

