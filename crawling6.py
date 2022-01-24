from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from crawlingutil import CrawlingUtill

cutil = CrawlingUtill("부산 한마음 스포츠센터")
html = requests.get("http://hmsports.bisco.or.kr/facil/facil01/facil01_1/index.asp").text
htmlAll = bs(html,'html.parser')
tablename = [htmlAll.find("div",{"class":"clist01"}).find("h4").text]
print(tablename)
# table_df_list = cutil.crawlingHtml_to_table(htmlAll)
# table_df_list.pop()
# cutil.table_list_to_csv()
