#!/usr/bin/python
# -*- coding:UTF-8 -*-
import  re, urllib2, sys,chardet
import xlwt
from bs4 import BeautifulSoup

wb=xlwt.Workbook(encoding = 'utf8')
ws=wb.add_sheet('农药信息网')
ws.write(0,0,'登记证号')
ws.write(0,1,'有效起始日')
ws.write(0,2,'有效截止日')
ws.write(0,3,'登记名称')
ws.write(0,4,'毒性')
ws.write(0,5,'剂型')
ws.write(0,6,'生产厂家')
ws.write(0,7,'国家')
ws.write(0,8,'农药类别')
ws.write(0,9,'总含量')
ws.write(0,10,'备注')
ws.write(0,11,'有效成分')
ws.write(0,12,'有效成分含量')
ws.write(0,13,'有效成分')
ws.write(0,14,'有效成分含量')
ws.write(0,15,'有效成分')
ws.write(0,16,'有效成分含量')
ws.write(0,17,'有效成分')
ws.write(0,18,'有效成分含量')
ws.write(0,19,'有效成分')
ws.write(0,20,'有效成分含量')
ws.write(0,21,'作物')
ws.write(0,22,'防治对象')
ws.write(0,23,'制剂用药量')
ws.write(0,24,'施用方法')
ws.write(0,25,'作物')
ws.write(0,26,'防治对象')
ws.write(0,27,'制剂用药量')
ws.write(0,28,'施用方法')
ws.write(0,29,'作物')
ws.write(0,30,'防治对象')
ws.write(0,31,'制剂用药量')
ws.write(0,32,'施用方法')
ws.write(0,33,'作物')
ws.write(0,34,'防治对象')
ws.write(0,35,'制剂用药量')
ws.write(0,36,'施用方法')
ws.write(0,37,'作物')
ws.write(0,38,'防治对象')
ws.write(0,39,'制剂用药量')
ws.write(0,40,'施用方法')
ws.write(0,41,'作物')
ws.write(0,42,'防治对象')
ws.write(0,43,'制剂用药量')
ws.write(0,44,'施用方法')
ws.write(0,45,'作物')
ws.write(0,46,'防治对象')
ws.write(0,47,'制剂用药量')
ws.write(0,48,'施用方法')
ws.write(0,49,'作物')
ws.write(0,50,'防治对象')
ws.write(0,51,'制剂用药量')
ws.write(0,52,'施用方法')
ws.write(0,53,'作物')
ws.write(0,54,'防治对象')
ws.write(0,55,'制剂用药量')
ws.write(0,56,'施用方法')
ws.write(0,57,'作物')
ws.write(0,58,'防治对象')
ws.write(0,59,'制剂用药量')
ws.write(0,60,'施用方法')
ws.write(0,61,'作物')
ws.write(0,62,'防治对象')
ws.write(0,63,'制剂用药量')
ws.write(0,64,'施用方法')
ws.write(0,65,'作物')
ws.write(0,66,'防治对象')
ws.write(0,67,'制剂用药量')
ws.write(0,68,'施用方法')
ws.write(0,69,'作物')
ws.write(0,70,'防治对象')
ws.write(0,71,'制剂用药量')
ws.write(0,74,'防治对象')
ws.write(0,75,'制剂用药量')
ws.write(0,76,'施用方法')
ws.write(0,77,'作物')
ws.write(0,78,'防治对象')
ws.write(0,79,'制剂用药量')
ws.write(0,80,'施用方法')
ws.write(0,81,'作物')
ws.write(0,82,'防治对象')
ws.write(0,83,'制剂用药量')
ws.write(0,84,'施用方法')
ws.write(0,85,'作物')
ws.write(0,86,'防治对象')
ws.write(0,87,'制剂用药量')
ws.write(0,88,'施用方法')
ws.write(0,89,'作物')
ws.write(0,90,'防治对象')
ws.write(0,91,'制剂用药量')
ws.write(0,92,'施用方法')
ws.write(0,93,'作物')
ws.write(0,94,'防治对象')
ws.write(0,95,'制剂用药量')
ws.write(0,96,'施用方法')
ws.write(0,97,'作物')
ws.write(0,98,'防治对象')
ws.write(0,99,'制剂用药量')
ws.write(0,100,'施用方法')
ws.write(0,101,'作物')
ws.write(0,102,'防治对象')
ws.write(0,103,'制剂用药量')
ws.write(0,104,'施用方法')
ws.write(0,105,'作物')
ws.write(0,106,'防治对象')
ws.write(0,107,'制剂用药量')
ws.write(0,108,'施用方法')
ws.write(0,109,'作物')
ws.write(0,110,'防治对象')
ws.write(0,111,'制剂用药量')
ws.write(0,112,'施用方法')
ws.write(0,113,'作物')
ws.write(0,114,'防治对象')
ws.write(0,115,'制剂用药量')
ws.write(0,116,'施用方法')
ws.write(0,117,'作物')
ws.write(0,118,'防治对象')
ws.write(0,119,'制剂用药量')
ws.write(0,120,'施用方法')
ws.write(0,121,'作物')
ws.write(0,122,'防治对象')
ws.write(0,123,'制剂用药量')
ws.write(0,124,'施用方法')

kk = 1
#with open('url.txt', 'w') as f:
#for line in f.readlines():  
f = open("url.txt","r")
lines = f.readlines()
for line in lines: 
   line=line.strip('\n')
   if line.strip()=='':
      continue
   #print line  
   #url = 'http://www.chinapesticide.org.cn/myquery/querydetail?pdno=5583D84DF4184EA18EF280315C2C2BC0&pdrgno=PD20102160&___t0.5472141889968529'
   try:
     request = urllib2.Request(line)
     response = urllib2.urlopen(request,timeout = 20) 
     html = response.read()
     soup = BeautifulSoup(html,'html.parser',from_encoding = 'utf-8')
     tables = soup.find_all('table')
     #print len(tables)
     if len(tables) >= 3:
       i = 1
       k = 0
       table0 = tables[0]
       trs0 = table0.find_all('tr')
       for tr0 in trs0:
          td0 = tr0.find_all('td')
          for td_0 in td0:
             if k == 2:
                ws.write(kk,0,td_0.get_text().strip())
             elif k == 4:
                ws.write(kk,1,td_0.get_text().strip())
             elif k == 6:
                ws.write(kk,2,td_0.get_text().strip())
             elif k == 8:
                ws.write(kk,3,td_0.get_text().strip())
             elif k == 10:
                ws.write(kk,4,td_0.get_text().strip())
             elif k == 12:
                ws.write(kk,5,td_0.get_text().strip())
             elif k == 14:
                ws.write(kk,6,td_0.get_text().strip())
             elif k == 16:
                ws.write(kk,7,td_0.get_text().strip())
             elif k == 18:
                ws.write(kk,8,td_0.get_text().strip())
             elif k == 20:
                ws.write(kk,9,td_0.get_text().strip())
             elif k == 22:
                ws.write(kk,10,td_0.get_text().strip())
             k = k + 1
       k = 0
       table2 = tables[2]
       trs2 = table2.find_all('tr')
       for tr2 in trs2:
          td2 = tr2.find_all('td')
          len2 = len(td2)
          for td_2 in td2:
             if k == 3:
                ws.write(kk,11,td_2.get_text().strip())
             elif k == 4:
                ws.write(kk,12,td_2.get_text().strip())
             elif k == 5:
                ws.write(kk,13,td_2.get_text().strip())
             elif k == 6:
                ws.write(kk,14,td_2.get_text().strip())
             elif k == 7:
                ws.write(kk,15,td_2.get_text().strip())
             elif k == 8:
                ws.write(kk,16,td_2.get_text().strip())
             elif k == 9:
                ws.write(kk,17,td_2.get_text().strip())
             elif k == 10:
                ws.write(kk,18,td_2.get_text().strip())
             elif k == 11:
                ws.write(kk,19,td_2.get_text().strip())
             elif k == 12:
                ws.write(kk,20,td_2.get_text().strip())
             k = k + 1

       i = 0
       k = 0
       table3 = tables[3]
       trs3 = table3.find_all('tr')
       for tr3 in trs3:
          td3 = tr3.find_all('td')
          len3 = len(td3)
          for td_3 in td3:
             if k >= 5: 
                ws.write(kk,21+i,td_3.get_text().strip())
                i = i + 1
             k = k + 1
     kk = kk + 1  
   except: 
        print line
        continue          
   #kk = kk + 1
wb.save('农药信息.xls')



