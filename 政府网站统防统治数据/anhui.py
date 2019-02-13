#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def  printPlistCode():
    #今天文件名称
    file_path = '/home/worker/prevention/result.txt/' +  time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.txt'
    #当前抓取时间
    nowTime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    #昨天发布时间
    yesterdayReleaseTime = time.strftime('%Y-%m-%d',time.localtime(time.time()-86400))
    url_list = ['http://www.ccgp-anhui.gov.cn/searchNewsController/searchNews.do?operType=search&keywords=%25E7%25BB%259F%25E9%2598%25B2%25E7%25BB%259F%25E6%25B2%25BB&channelCode=','http://www.ccgp-anhui.gov.cn/searchNewsController/searchNews.do?channelCode=&keywords=%E7%BB%9F%E9%98%B2%E7%BB%9F%E6%B2%BB&pageNum=2&numPerPage=20&orderField=&orderDirection=','http://www.ccgp-anhui.gov.cn/searchNewsController/searchNews.do?channelCode=&keywords=%E7%BB%9F%E9%98%B2%E7%BB%9F%E6%B2%BB&pageNum=3&numPerPage=20&orderField=&orderDirection=','http://www.ccgp-anhui.gov.cn/searchNewsController/searchNews.do?channelCode=&keywords=%E7%BB%9F%E9%98%B2%E7%BB%9F%E6%B2%BB&pageNum=4&numPerPage=20&orderField=&orderDirection=']

    for i in range (0,len(url_list)):
	html = urllib2.urlopen(url_list[i]).read()
	soup = BeautifulSoup(html,'html.parser')
	#发布时间格式
	p = r'(\d{4}-\d{1,2}-\d{1,2})'
	pattern = re.compile(p)
	for div in soup.find_all('div',class_='zc_contract_top'):
	    for tr in div.find_all('tr'):
		text = tr.text
		a = tr.find('a')
		url = 'http://www.ccgp-anhui.gov.cn' + a['href']
		title = a['title']
		matcher = re.search(pattern,text)
        	release_date = matcher.group(0)
		#发布时间戳
		time_array = time.strptime(release_date, "%Y-%m-%d")
        	time_stamp = int(time.mktime(time_array))
		#当前时间戳
            	nowtime_array = time.strptime(nowTime, "%Y-%m-%d %H:%M")
            	nowtime_stamp = int(time.mktime(nowtime_array))
		if release_date == yesterdayReleaseTime:
		    data = '{"governMsg":"{\\"grabTime\\":%s,\\"publishDate\\":%s,\\"region\\":\\"%s\\",\\"title\\":\\"%s\\",\\"url\\":\\"%s\\"}"}' % (nowtime_stamp,time_stamp,'安徽省',title,url)
            	    print data
            	    #将数据写入文件中
            	    with open(file_path, 'a+') as f:
                	f.write(data+'\n')
                	print data
		    
		    


if __name__ == '__main__':
    #获取网页数据
    printPlistCode()
