from itertools import count
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from crawlingutil import CrawlingUtill


cutil = CrawlingUtill("서부재활체육센터")
class Crawling4():
    def __init__(self):
        self.html = requests.get("http://www.sbsports.or.kr/sub/wrcAble.do").text
        self.htmlAll = bs(self.html,'html.parser')
        self.tableNames = self.htmlAll.find_all('caption')
        self.tableNameList = []

    ##프로그램 이름 저장
    def mk_table_name_list(self):
        for tablename in self.tableNames:
            self.tableNameList.append(tablename.text.strip())
        return self.html_to_csv()

    ## html table을 df로 저장     
    def html_to_csv(self):
        table_df_list = cutil.crawlingHtml_to_table(self.htmlAll)
        cutil.table_list_to_csv(table_df_list,self.tableNameList)
        return table_df_list

    def run(self):
        return self.mk_table_name_list()

if __name__ =="__main__":
    c4 = Crawling4()
    c4.run()