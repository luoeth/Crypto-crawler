from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# PTT DigiCurrency
w = open('DigiCurrency.txt', 'w', encoding='utf-8')
url = "https://www.ptt.cc/bbs/DigiCurrency/index.html"
for i in range(2):#爬取兩頁
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")#將網頁資料以html.parser
    title = soup.select("div.title a") #標題
    u = soup.select("div.btn-group.btn-group-paging a") #a標籤
    url = "https://www.ptt.cc"+ u[1]["href"] #上一頁的網址
    
    for titles in title: #印出網址跟標題
        # print(titles["href"],titles.text)
        w.write((titles['href'] + titles.text) + '\n')
w.close()
            

r = open('DigiCurrency.txt', 'r', encoding='utf-8')
date_ptt = r.read()#將read存入date
r.close()

def Ptt(request):
    return render(request, 'crypto.html',{
                'date_ptt' : date_ptt
    })


# Blocktempo 動區動趨
w = open('blocktempo.txt', 'w', encoding='utf-8')
url = "https://www.blocktempo.com/2023/"
for i in range(2,4):#爬取2、3頁
    i = str(i)#轉成字串
    g = requests.get(url) #將網頁資料GET下來
    soup = BeautifulSoup(g.text,"html.parser") #將網頁資料以html.parser
    sel = soup.select("h3.jeg_post_title a") #取HTML標中的 <div class="title"></div> 中的<a>標籤存入sel
    url = "https://www.blocktempo.com/2023/page/" + i
    for s in sel:
        w.write((s.text + s["href"]) + '\n')
w.close() 

r = open('blocktempo.txt', 'r', encoding='utf-8')
date_block = r.read()#將read存入date
r.close()

def Blocktempo(request):
    return render(request, 'blocktempo.html',{
        'date_block' : date_block
    })


# Abmedia 鏈新聞
w = open('abmedia.txt', 'w', encoding='utf-8')
url = "https://abmedia.io/blog"
for i in range(2,4):#爬取2、3頁
    i = str(i)#轉成字串
    g = requests.get(url) #將網頁資料GET下來
    soup = BeautifulSoup(g.text,"html.parser") #將網頁資料以html.parser
    sel = soup.select("h3.title a") #取HTML標中的class="title"中的<a>標籤存入sel
    url = "https://abmedia.io/blog/page/" + i
    for s in sel:
        w.write((s.text + s["href"]) + '\n')
w.close() 

r = open('abmedia.txt', 'r', encoding='utf-8')
date_abmedia = r.read()#將read存入date
r.close()

def Abmedia(request):
    return render(request, 'abmedia.html',{
        'date_abmedia' : date_abmedia
    })
