# -*- coding=utf-8 -*-

#导入需要使用到的模块
import urllib
import re
import pandas as pd
import pymysql
import os
import requests
from bs4 import BeautifulSoup
import traceback
import re
import time

#爬虫抓取天天基金每日净值
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
#抓取网页代码函数
def getStackCode(html):
    # print(html)
    s = r'<span class="ui-num">(.+?)</span>'  # <span class="ui-num">161725</span>< span class="ui-font-large ui-color-red ui-num" id="gz_gsz">1.1239</span>  <li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">
    pat = re.compile(s)
    code = pat.findall(html)
    s = r'<a href="http://fund.eastmoney.com/'+code[0].strip()+'.html" target="_self">(.+?)</a>'  #  < span class="ui-font-large ui-color-red ui-num" id="gz_gsz">1.1239</span>  <li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">
    pat = re.compile(s)
    code =code.__add__(list(set(pat.findall(html))))
    s = r'<span class="ui-font-large ui-color-red ui-num" id="gz_gsz">(.+?)</span>'  # 净值估算 < span class="ui-font-large ui-color-red ui-num" id="gz_gsz">1.1239</span>  <li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">
    pat = re.compile(s)
    code = code.__add__(pat.findall(html))
    s = r'<span class="ui-font-large ui-color-green ui-num">(.+?)</span>'  # 单位净值<span class="ui-font-large ui-color-green ui-num">1.1160</span> <li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">
    pat = re.compile(s)
    code = code.__add__(pat.findall(html))
    s = r'<span class="ui-font-large ui-color-red ui-num">(.+?)</span>'  #  累计净值 <span class="ui-font-large ui-color-green ui-num">1.1160</span> <li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">
    pat = re.compile(s)
    code = code.__add__(pat.findall(html))
    allfinds2 = re.findall(s,html, re.S)


    #print(allfinds2[0].strip())  <span class="ui-font-large ui-color-red ui-num">1.6520</span>
    return code

def main():
   Url = 'http://fund.eastmoney.com/161725.html?spm=search'#数据连接地址
   #实施抓取
   code = getStackCode(getHTMLText(Url))
   print(code)

def main2():
   #jsonpgz({"fundcode": "161725", "name": "招商中证白酒指数分级", "jzrq": "2018-03-19", "dwjz": "1.1210", "gsz": "1.1096", "gszzl": "-1.02", "gztime": "2018-03-20 09:49"});  # dwjz:单位净值  gsz：估算值  gszzl:估算值掉率
   Url = 'http://fundgz.1234567.com.cn/js/161725.js'#数据连接地址    http://fundgz.1234567.com.cn/js/161725.js?rt=1521510103714  http://fundgz.1234567.com.cn/js/161725.js?rt=1521514131227  http://fundgz.1234567.com.cn/js/161726.js?rt=1521512756062
   Url2 = 'http://fundgz.1234567.com.cn/js/502023.js'#数据连接地址   http://fundgz.1234567.com.cn/js/502023.js?rt=1521511195535
   #实施抓取                                                                    #  http://fundgz.1234567.com.cn/js/502026.js?rt=1521512491646
   code = getHTMLText(Url)
   code = str(code).replace('jsonpgz(', '')
   code = str(code).replace(');', '')
  # print(code)
   time.sleep(1)
   code2 = getHTMLText(Url2)
   code2 = str(code2).replace('jsonpgz(', '')
   code2 = str(code2).replace(');', '')
   print(code+","+code2)



while True:
  #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
  #main()
  main2()
  time.sleep(1) # wait for 1 second

