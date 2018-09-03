#!/usr/bin/python
# vim: set fileencoding=utf-8 :
'''
Created on 2017-2-23

@author: Administrator
'''

import json
import urllib
import urllib2
import multiprocessing

#########################
#   url:接口的地址
#   url = "http://10.100.24.90:8080/web/monomercollection/add?pic=aa"
#########################
def HttpGet(url):
    try:
        #url = "http://10.100.24.90:8080/web/monomercollection/add?pic=aa"
        req = urllib2.Request(url)
#    print req
        res_data = urllib2.urlopen(req,data=None, timeout=3)
    except urllib2.URLError, e:
        print Exception,":",e,"请求超时"
        return "请求错误"
    res = res_data.read()
    return res


#ura = "http://127.0.0.1:8000?test=000"
#ura ="http://10.100.24.90:8080/web/monomercollection/add?pic=aa"
#print HttpGet("http://127.1.0.0:8765/?test=data")

######################################
#   url:接口的地址
#   http://10.100.24.90:8080/web/uploadfile/upload
#   parameter：post参数值(json格式)
#   {'ServiceCode':'aaaa','b':'bbbbb'}
######################################
def HttpPost(url,parameter):
    
    data_urlencode = urllib.urlencode(parameter)
#    data_urlencode = json.dumps(parameter)
#    data_urlencode = urllib.quote(data_urlencode)
    print data_urlencode
    req = urllib2.Request(url)
    print "111",req,"1111"
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    
    res_data = opener.open(req,data_urlencode)
    res = res_data.read()
    print res
    return res



str = {'username':'admin','password':'1234'}

#print json.decoder
print HttpPost("http://127.0.0.1:8765",str)

#
str1 = {"sign":"aaa","x":23.5,"y":12.5,"structure":"bbb"}


#print HttpPost("http://127.0.0.1:8765",str1)



#print HttpPost("http://10.100.24.90:8080/web/uploadfile/uploadPhoneData",str)
