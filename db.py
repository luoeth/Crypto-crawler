import pymysql
import requests
from bs4 import BeautifulSoup
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
 #如果crypto已經存在的話就刪除
cursor.execute('DROP TABLE IF EXISTS data_defi')
#建立table
sql = '''CREATE TABLE data_defi(
            name text,
            logo text,
            tvl text,
            change_1h text,
            change_1d text,
            change_7d text);'''
cursor.execute(sql)
conn.commit()

r = requests.get('https://api.llama.fi/protocols')
time.sleep(random.randint(1,5))#休息1~5秒之間
json = r.json()

for j in json:
        try:
                cursor.execute("INSERT INTO data_defi(name, logo, tvl, change_1h, change_1d, change_7d) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" %(j["name"], j["logo"], j["tvl"], j["change_1h"], j["change_1d"], j["change_7d"]))
                conn.commit()
        except Exception as ex:#例外錯誤處理 
                print(ex)

#取出資料
cursor.execute("SELECT name, logo FROM data_defi WHERE tvl>30000000 and change_1h>0.05 and change_1d>0.1 and change_7d>0.3")
f = cursor.fetchall() 
# data_defi = "".join([str(l) for l in f])
print(f)
cursor.close()
conn.close()



# #defillama
# url = "https://defillama.com/"
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
# g = requests.get(url, headers=headers)
# time.sleep(random.randint(1,10)) #休息1~10秒之間)  
# soup = BeautifulSoup(g.text,"html.parser")#將網頁資料以html.parser

# title = soup.select('span.sc-97364596-0.bshIeC a') #標題

# for t in title:
#         print(t.text)
        # cursor.execute("INSERT INTO crypto(title, url) VALUES ('%s', '%s');" %(titles.text, titles["href"]))
        # conn.commit()


# cursor.execute("SELECT * FROM crypto")
# for cur in cursor:
#     print(cur, '\n')

# conn.close()
# data_ptt = cursor.fetchmany(20)
# conn.close()
# print(data_ptt)


# try:
#     # 建立Connection物件
#     conn = pymysql.connect(**db_settings)
#     # 建立Cursor物件
#     with conn.cursor() as cursor:
       
# #例外錯誤處理      
# except Exception as ex:
#     print(ex)

