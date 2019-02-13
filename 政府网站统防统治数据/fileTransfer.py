#coding:utf8
import requests
import json
import time

url = "http://10.0.1.9:8895/management/api/unifiedPrevent/addGovernMsg"

headers = {
    'cache-control': "no-cache",
    'Postman-Token': "61bf48ee-bfd7-40e6-987a-554f531b60e3"
    }


#今天文件名称
file_path = time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.txt'

f = open("/home/worker/prevention/result.txt/"+file_path, "r")  
while True:  
    line = f.readline()  
    if line:  
	dictinfo = json.loads(line)
	#print type(dictinfo)
	response = requests.request("POST", url, headers=headers, params=dictinfo)
	print(response.text)
    else:  
        break
f.close()
