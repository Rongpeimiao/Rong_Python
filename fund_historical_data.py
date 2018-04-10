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
def gethistorical(code):
    code=code.split("records:")
    code = str(code[1]).split(",")[0]
    return  code
    #print("zd['records']: ", dict['records'])

def splitdata(code):
     code=code.split("</tr></thead><tbody>")
     num=0
     fundlist=[]
     try:
        for val in code:
            if(num==0):
                val=val.split('<tr>')[1]
                fundlist.append(val)
                num = num + 1
            else:
                 val1=val.split('</tr>')
                 num2 = 0
                 for val2 in val1:
                     num2 = num2+1
                     if (num2 < len(val1)):
                          fundlist.append(val2)
     except Exception as  e:
          print(e)
     return  fundlist

def main():
   print('连接到mysql服务器...')
   db = pymysql.connect(host='127.0.0.1', user='root', passwd='123', db='fundDB', port=3306, charset='utf8')
   print('连接上了!')
   cursor = db.cursor()
   fundlists = do_query(cursor, db)  # 查询基金表
   print(fundlists)
   num=1
   #
   for fundval in fundlists:
       par = '1'
       codedb = fundval
       Url = str(
           'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + codedb + '&page=1&per=' + par + '&sdate=&edate=')  # 数据连接地址  获取一条数据，目的获取总数

       # code = getStackCode(getHTMLText(Url))
       code = getHTMLText(Url)  # 获取表格 数据
       par = gethistorical(code)  # 获取总数
       Url = str(
           'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=161725&page=1&per=' + par + '&sdate=&edate=')  # 数据连接地址   根据总数重新获取历史数据
       code = getHTMLText(Url)
       funddata = splitdata(code)
       # print(funddata)

       cz = createtables(cursor, db, codedb)
       if (cz == '0'):
           for val in funddata:
               do_insert(cursor, db, codedb, val)
       else:
           print('表存在数据库了有数据!' + str(num))
           num2 = do_query_val(cursor, db, codedb, val)
           if (str(num2).__contains__("th")):
               print("存在数据")
           else:
               do_insert(cursor, db, codedb, val)
           num = num + 1
   #
   #createtables(cursor, db)    #创表

   cursor.close()
   db.close()
   #print('close')

#创表
def createtables(cursor,db,codedb):
    # create a table named addfields
    dbname='fund_'+codedb
    strsql="create table "+str(dbname)+"(id int(5) NOT NULL auto_increment, name text,PRIMARY KEY(`id`))"
    try:
        cursor.execute(strsql)
        db.commit()
        return '0'
    except:
        print('The table '+dbname+' exists!'+strsql)
        return  '1'


     # add the fileds
#    try:
#        for i in range(1):
#            sql = "alter table addfields add key%s text" % i
#            cursor.execute(sql)
#    except Exception as  e:
#         print(e)

#    for i in range(4):  # insert 5 lines
#        sql = "insert into addfields set id=%s" % i    #INSERT INTO addfields (id, name,...) VALUES (%s, %s)
#        cursor.execute(sql)
     #  sql = "update addfields set name = 'hello%s' where id= %s" % (i, i)
     #   cursor.execute(sql)
    # for j in range(5):
    #  sql = "update addfields set key%s = 'world%s%s' where id=%s" % (j, i, j, i)
        #  cursor.execute(sql)
            # this is very important
    # sql = "INSERT INTO addfields (id, name) VALUES (%s, %s)" %(1111, '11111')
    #cursor.execute(sql)


def do_query(cursor, db):
    sql = "SELECT * FROM fund_tab "  #\ WHERE INCOME > '%d'

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        print('resuts', cursor.rowcount)
        fundlist = []
        for row in results:
            code = row[1]
            fundlist.append(code)
            lname = row[2]
            # Now print fetched result
            # print( "fname=%s,lname=%s" % (code, lname))
    except:
        print("Error: unable to fecth data")

    return  fundlist


def do_query_val(cursor, db,dbname, val):
    dbname = 'fund_' + dbname
    sql = "SELECT * FROM "+dbname+"  where name="+'"'+val+'" ' #\ WHERE INCOME > '%d'
    print(sql)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        # print('resuts==', cursor.rowcount)

    except:
        print("Error: unable to fecth data")
    return  results


def do_updata(cursor, db):
 # insert
 # Prepare SQL query to INSERT a record into the database.
   sql = "UPDATE tablename SET id = id+1 WHERE id = '%c'" % ('M')
   try:
     cursor.execute(sql)
     db.commit()
   except:
     db.rollback()

def do_delete(cursor, db):
    sql = 'DELETE FROM tablename WHERE id > {}'.format(20)
    try:
       cursor.execute(sql)
       db.commit()
    except:
       db.rollback()

def do_insert(cursor, db, dbname, val ):
    dbname = 'fund_' + dbname
    sql = "INSERT INTO "+str(dbname)+'(name)  VALUES ("%s" )' % (val)
    try:

         cursor.execute(sql)
         print(dbname+'插入数据成功!')
         db.commit()
    except:
         print(dbname+'插入数据失败!'+sql)
         db.rollback()
         #main()
#http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183038179377121452496_1521450212766&fundCode=161725&pageIndex=2&pageSize=20&startDate=&endDate=&_=1521450215571
main()