from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pymysql
import numpy as np
import pandas as pd
import time
import random

# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "12345678",
    "db": "crypto",
    "charset": "utf8"
}


# 建立Connection物件
conn = pymysql.connect(**db_settings)
# 建立Cursor物件
cursor = conn.cursor()
#如果已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_ptt')
#建立table
sql = '''CREATE TABLE data_ptt(
            title VARCHAR(255),
            url VARCHAR(255));'''
cursor.execute(sql)
conn.commit()

#PTT DigiCurrency
url = "https://www.ptt.cc/bbs/DigiCurrency/index.html"
for i in range(2):#爬取兩頁
    g = requests.get(url)
    soup = BeautifulSoup(g.text,"html.parser")#將網頁資料以html.parser
    title = soup.select("div.title a") #標題
    u = soup.select("div.btn-group.btn-group-paging a") #a標籤
    url = "https://www.ptt.cc"+ u[1]["href"] #上一頁的網址
    
    for titles in title: #印出網址跟標題
         cursor.execute("INSERT INTO data_ptt(title, url) VALUES ('%s', '%s');" %(titles.text, titles["href"]) )
         conn.commit()

#取出全部資料
cursor.execute("SELECT * FROM data_ptt")
data_ptt = cursor.fetchall()    

def Ptt(request):
    return render(request, 'crypto.html',{
                'data_ptt' : pd.DataFrame(data_ptt)
    })



#如果已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_block')
#建立table
sql = '''CREATE TABLE data_block(
            title VARCHAR(255),
            url VARCHAR(255));'''
cursor.execute(sql)
conn.commit()

# Blocktempo 動區動趨
url = "https://www.blocktempo.com/2023/"
for i in range(2,4):#爬取2、3頁
    i = str(i)#轉成字串
    g = requests.get(url) #將網頁資料GET下來
    soup = BeautifulSoup(g.text,"html.parser") #將網頁資料以html.parser
    sel = soup.select("h3.jeg_post_title a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    url = "https://www.blocktempo.com/2023/page/" + i
    for s in sel:
        cursor.execute("INSERT INTO data_block(title, url) VALUES ('%s', '%s');" %(s.text, s["href"]) )
        conn.commit()

#取出全部資料
cursor.execute("SELECT * FROM data_block")
data_block = cursor.fetchall() 

def Blocktempo(request):
    return render(request, 'blocktempo.html',{
        'data_block' : pd.DataFrame(data_block)
    })


#如果已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_abmedia')
#建立table
sql = '''CREATE TABLE data_abmedia(
            title VARCHAR(255),
            url VARCHAR(255));'''
cursor.execute(sql)
conn.commit()

# Abmedia 鏈新聞
url = "https://abmedia.io/blog"
for i in range(2,4):#爬取2、3頁
    i = str(i)#轉成字串
    g = requests.get(url) #將網頁資料GET下來
    soup = BeautifulSoup(g.text,"html.parser") #將網頁資料以html.parser
    sel = soup.select("h3.title a") #取HTML標中的class="title"中的<a>標籤存入sel
    url = "https://abmedia.io/blog/page/" + i
    for s in sel:
        cursor.execute("INSERT INTO data_abmedia(title, url) VALUES ('%s', '%s');" %(s.text, s["href"]) )
        conn.commit()

#取出全部資料
cursor.execute("SELECT * FROM data_abmedia")
data_abmedia = cursor.fetchall() 

def Abmedia(request):
    return render(request, 'abmedia.html',{
        'data_abmedia' : pd.Series(data_abmedia)
    })

#增加欄寬，讓資料完整顯示
pd.set_option('max_colwidth', 800)


 #如果crypto已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_defi')
#建立table
sql = '''CREATE TABLE data_defi(
            name text,
            logo text,
            tvl text,
            change_1h text,
            change_1d text,
            change_7d text,
            url text);'''
cursor.execute(sql)
conn.commit()

r = requests.get('https://api.llama.fi/protocols')
time.sleep(random.randint(1,3))#休息1~3秒之間
json = r.json()

for j in json:
        try:
                cursor.execute("INSERT INTO data_defi(name, logo, tvl, change_1h, change_1d, change_7d, url) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(j["name"], j["logo"], j["tvl"], j["change_1h"], j["change_1d"], j["change_7d"], j["url"]))
                conn.commit()
        except Exception as ex:#例外錯誤處理 
                print(ex)

#取出資料
cursor.execute("SELECT logo FROM data_defi WHERE tvl>30000000 and change_1h>0.05 and change_1d>0.1 and change_7d>0.3")
data_logo = cursor.fetchall()
data_logo_0 = ''.join(data_logo[0])#轉str
data_logo_1 = ''.join(data_logo[1])
data_logo_2 = ''.join(data_logo[2])
data_logo_3 = ''.join(data_logo[3])
data_logo_4 = ''.join(data_logo[4])

cursor.execute("SELECT name FROM data_defi WHERE tvl>30000000 and change_1h>0.05 and change_1d>0.1 and change_7d>0.3")
data_name = cursor.fetchall() 
data_name_0 = ''.join(data_name[0])
data_name_1 = ''.join(data_name[1])
data_name_2 = ''.join(data_name[2])
data_name_3 = ''.join(data_name[3])
data_name_4 = ''.join(data_name[4])

cursor.execute("SELECT url FROM data_defi WHERE tvl>30000000 and change_1h>0.05 and change_1d>0.1 and change_7d>0.3")
data_url = cursor.fetchall() 
data_url_0 = ''.join(data_url[0])
data_url_1 = ''.join(data_url[1])
data_url_2 = ''.join(data_url[2])
data_url_3 = ''.join(data_url[3])
data_url_4 = ''.join(data_url[4])

def Defi(request):
    return render(request, 'defi.html',{
        'data_logo_0' : data_logo_0,
        'data_logo_1' : data_logo_1,
        'data_logo_2' : data_logo_2,
        'data_logo_3' : data_logo_3,
        'data_logo_4' : data_logo_4,
        'data_name_0' : data_name_0,
        'data_name_1' : data_name_1,
        'data_name_2' : data_name_2,
        'data_name_3' : data_name_3,
        'data_name_4' : data_name_4,
        'data_url_0' : data_url_0,
        'data_url_1' : data_url_1,
        'data_url_2' : data_url_2,
        'data_url_3' : data_url_3,
        'data_url_4' : data_url_4,
    })



cursor.close()
conn.close()