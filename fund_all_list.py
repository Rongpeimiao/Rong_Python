# coding=utf-8
#导入需要使用到的模块
import urllib
import re
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import traceback
import re
import time
import pymysql


#爬虫抓取网页函数
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

  # 正则表达式获取<tr></tr>之间内容
def gettrtext(language):
     try:
         #  language = '''''<tr><th>性別：</th><td>男</td></tr><tr>'''
         res_tr2 = r'<tr class="ev">(.*?)</tr>'             #表格存在2中情况，有class="ev"和没有class的
         m_tr = re.findall(res_tr2, language, re.S | re.M)
         num=1
         fundlist = []   ## 空列表
         for line in m_tr:
             # 获取表格第二列td 属性值
             res_td = r'<td>(.*?)</td>'
             m_td = re.findall(res_td, line, re.S | re.M)
             for nn in m_td:
                 num = num + 1
                 str=nn.replace("---","").replace("\n", "").strip()
                 if ( str!='') and (str.find("div") == -1) and (str.find("a") != -1):
                     fundlist.append(str)
                     # print(str)
         return fundlist
     except:
        return ""

#数据连接地址
def getUrltext():
   Url = 'http://fund.eastmoney.com/fundguzhi1.html'#数据连接地址
   #实施抓取
   # code = getStackCode(getHTMLText(Url))
   html = getHTMLText(Url)
   #gettrtext(code)
   #print(gettrtext(code))
   #for nn in gettrtext(code):
   #    print(nn)
   return gettrtext(html)


def getlists(ls):
    print('连接到mysql服务器...')
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='123', db='fundDB', port=3306, charset='utf8')
   # conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123', db='fundDB', port=3306, charset='utf8')
    print('连接上了!')
    cursor = db.cursor()
    for nn in ls:
        nn=nn.split("</a>")[0].split('.html">')
        code=nn[0].replace('<a href="','')
        name=nn[1]
        insert_fund = ("INSERT INTO FUND_TAB(FUND_CODE,FUND_NAME,CREATE_DATE)" "VALUES(%s,%s,%s)")
        data_fund = (code, name,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        cursor.execute(insert_fund, data_fund)
        db.commit()
        print(nn)
    cursor.close()
    db.close()
def getlists2(ls):
    num=0
    for nn in ls:
        num=num+1
        print(nn+'@@@@'+str(num))
def main():
    getlists(getUrltext())

main()

