from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from crawlingutil import CrawlingUtill

cutil = CrawlingUtill('서부산권 장애인 스포츠 센터')

## 페이지 url 확인
html = requests.get("https://www.sbsd.kr/Home").text
htmlAll = bs(html,'html.parser')
programpage = htmlAll.find("li",{"class":"cd1 cd1c4"}).find("a")["href"].split("/")[-1]

## '프로그램' 페이지 접근
html = html = requests.get("https://www.sbsd.kr/Home/"+programpage).text
htmlAll = bs(html,'html.parser')
pages = htmlAll.find('nav',{"class":"tabmenu con_tab four no_pdt"}).find_all("li",{"class":"cd3"})

## 프로그램 페이지 url 확인
programURLs = []
for elem in pages:
    programURLs.append(elem.find("a")["href"].split("/")[-1])   ## 페이지 넘버

## n 개의 프로그램 접근 및 함수용 데이터 전처리
tableLists = []
programNames = []
for programURL in programURLs:
    ## 테이블 리스트 생성 생성 
    html = requests.get("https://www.sbsd.kr/Home/"+programURL).text
    htmlAll = bs(html,'html.parser')
    ##전체 테이블 추가
    tableList = cutil.crawlingHtml_to_table(htmlAll)    ## html to table
    for table in tableList:
        tableLists.append(table)
    ##전체 이름 추가
    programName = [htmlAll.find('div',{'class':'s_subject'}).find("p").text] * len(tableList)
    for name in programName:
        programNames.append(name)

## df to csv
cutil.table_list_to_csv(tableLists,programNames)


