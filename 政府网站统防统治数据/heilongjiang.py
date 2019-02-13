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

    html = urllib2.urlopen("http://www.ccgp-heilongj.gov.cn/xwzs!queryXwxxSsqx.action?xwzsPage.GJZ=%E7%BB%9F%E9%98%B2%E7%BB%9F%E6%B2%BB").read()
    soup = BeautifulSoup(html,'html.parser')
    p = r"href='([\s\S]*)';re"
    for div in soup.find_all('div',class_='xxei',limit=5):
	a = div.find('a')
	#信息标题
	title = a.string
	url_text = ''.join(a['onclick'])
	url_list = re.findall(p, url_text)
	#链接地址
	url = 'http://www.ccgp-heilongj.gov.cn' + url_list[0]
	span = div.find('span',class_='sjej')
	#发布日期
	release_date = span.string
	#匹配昨天发布日期
        if release_date == yesterdayReleaseTime :	
	    #发布时间戳	
	    time_array = time.strptime(release_date, "%Y-%m-%d")
            time_stamp = int(time.mktime(time_array))
	    #当前时间戳
            nowtime_array = time.strptime(nowTime, "%Y-%m-%d %H:%M")
            nowtime_stamp = int(time.mktime(nowtime_array))
	    
	    data = '{"governMsg":"{\\"grabTime\\":%s,\\"publishDate\\":%s,\\"region\\":\\"%s\\",\\"title\\":\\"%s\\",\\"url\\":\\"%s\\"}"}' % (nowtime_stamp,time_stamp,'黑龙江省',title,url)
            #将数据写入文件中
            with open(file_path, 'a+') as f:
                f.write(data+'\n')
                print data


if __name__ == '__main__':
    #获取网页数据
    printPlistCode()
