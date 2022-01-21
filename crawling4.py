from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

html = requests.get("http://www.sbsports.or.kr/sub/wrcAble.do").text
htmlAll = bs(html,'html.parser')
tableNames = htmlAll.find_all('caption')

##프로그램 이름 저장
tableNameList = []
for tablename in tableNames:
    tableNameList.append(tablename.text.strip())

## html table을 df로 저장
htmlTable = htmlAll.find_all("table")
table_html = str(htmlTable)
table_df_list = pd.read_html(table_html)
print(table_df_list)
count = 99
for num in range(len(table_df_list)):
    count+=1
    table_df_list[num].index = table_df_list[num].index + 1
    table_df_list[num].index.name = tableNameList[num]
    table_df_list[num].to_csv('./file'+str(count)+'.csv', sep=',', na_rep='NaN')
