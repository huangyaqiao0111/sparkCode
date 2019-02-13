#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import MySQLdb
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#今天文件名称
file_path = '/home/worker/prevention/' +time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.txt'

db = MySQLdb.connect("10.0.1.9", "work", "srcRwk8WNcZemaSKflE9", "farmfriend", charset='utf8' )
cursor = db.cursor()

input = open(file_path)
for line in input:
	if len(linelist) > 1 :
		linelist = line.split(',')
		sql = "INSERT INTO govern_msg (title,region,url,publish_time,grab_time) VALUES (%s,%s,%s,%s,%s) "
		cursor.execute(sql,linelist)
		db.commit()
db.close()
