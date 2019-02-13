#coding:utf8

import urllib2
#json解析库,对应到lxml
import json
#json的解析语法，对应到xpath
import jsonpath
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

    url="http://www.jxsggzy.cn/fulltextsearch/rest/getfulltextdata?format=json&wd=%E7%BB%9F%E9%98%B2%E7%BB%9F%E6%B2%BB&sdt=20180121161432&edt=20190121161432&srch_cgy=1&sort=0&pn=0&rn=10&cl=150"
    header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0"}
    request=urllib2.Request(url,headers=header)
    response=urllib2.urlopen(request)
    #取出json文件里的内容，返回的格式是字符串
    html=response.read()
    #把json形式的字符串转换成python形式的Unicode字符串
    unicodestr=json.loads(html)
    #python形式的列表
    title_list=jsonpath.jsonpath(unicodestr,"$..title")  #不管有多少层，写两个.都能取到
    link_list=jsonpath.jsonpath(unicodestr,"$..link")
    date_list=jsonpath.jsonpath(unicodestr,"$..date")
    #打印每个城市
    for i in range (0,5):
 	release_date = date_list[i].split(' ')[0]
	if release_date == yesterdayReleaseTime :
	    title = title_list[i].replace("<font color='#CC0000'>","").replace("</font><font color='#CC0000'>","").replace("</font>","")
            url = link_list[i]
	    #发布时间戳
	    time_array = time.strptime(release_date, "%Y-%m-%d")
            time_stamp = int(time.mktime(time_array))
	    #当前时间戳
	    nowtime_array = time.strptime(nowTime, "%Y-%m-%d %H:%M")
	    nowtime_stamp = int(time.mktime(nowtime_array))
	    data = '{"governMsg":"{\\"grabTime\\":%s,\\"publishDate\\":%s,\\"region\\":\\"%s\\",\\"title\\":\\"%s\\",\\"url\\":\\"%s\\"}"}' % (nowtime_stamp,time_stamp,'山东省',title,url)
            print data
            #将数据写入文件中
            with open(file_path, 'a+') as f:
                f.write(data+'\n')
                print data

if __name__ == '__main__':
    printPlistCode()
