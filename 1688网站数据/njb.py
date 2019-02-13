#!/usr/bin/python
# coding=utf-8

import re

str1 = 'http://www.chinapesticide.org.cn/myquery/querydetail?pdno='
str2 = '&pdrgno='
f = open('aaa.txt', 'r')
source = f.read()
rr = re.compile(r'open[(\'](.*)[\']')
s=rr.findall(source)
for line in s:
    temps = line.split(',')
    a = temps[0]
    b = temps[1]
    print str1 + a.replace('\'', '').strip() + str2 + b.replace('\'','').strip()
f.close()

