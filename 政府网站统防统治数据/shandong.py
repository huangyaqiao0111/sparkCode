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

    html = urllib2.urlopen("http://www.ccgp-shandong.gov.cn/sdgp2017/site/listsearchall.jsp?cmd=search&subject=%E7%BB%9F%E9%98%B2%E7%BB%9F%E6%B2%BB").read()
    soup = BeautifulSoup(html,'html.parser')
    #发布时间格式
    p = r'(\d{4}-\d{1,2}-\d{1,2})'

    for td in soup.find_all('td',class_='Font9',limit=6):
        a = td.find('a',class_='aa')
        #信息标题
        title = a['title']
	#链接地址
        url = 'http://www.ccgp-shandong.gov.cn' + a['href']	    
	text = td.text

	#发布日期
        release_date = ''
	date_list = re.findall(p,text)
	for i in range(0,len(date_list)):
	    release_date = date_list[0]
	#发布时间戳
	time_array = time.strptime(release_date, "%Y-%m-%d")
        time_stamp = int(time.mktime(time_array))
	#当前时间戳
        nowtime_array = time.strptime(nowTime, "%Y-%m-%d %H:%M")
        nowtime_stamp = int(time.mktime(nowtime_array))

	if (release_date == yesterdayReleaseTime):
	    time_array = time.strptime(release_date, "%Y-%m-%d")
            time_stamp = int(time.mktime(time_array))
	    data = '{"governMsg":"{\\"grabTime\\":%s,\\"publishDate\\":%s,\\"region\\":\\"%s\\",\\"title\\":\\"%s\\",\\"url\\":\\"%s\\"}"}' % (nowtime_stamp,time_stamp,'山东省',title,url)
	    print data
	    #将数据写入文件中
            with open(file_path, 'a+') as f:
                f.write(data+'\n')
                print data



if __name__ == '__main__':
    #获取网页数据
    text = printPlistCode()
