from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from crawlingutil import CrawlingUtill

cutil =CrawlingUtill("서부재활체육센터")

html = requests.get("http://www.sbsports.or.kr/sub/wrcAble.do").text
htmlAll = bs(html,'html.parser')
tableNames = htmlAll.find_all('caption')

##프로그램 이름 저장
tableNameList = []
for tablename in tableNames:
    tableNameList.append(tablename.text.strip())

## html table을 df로 저장
table_df_list = cutil.crawlingHtml_to_table(htmlAll)
cutil.table_list_to_csv(table_df_list,tableNameList)
