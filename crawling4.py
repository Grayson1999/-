import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


my_columns = ["프로그램", "대상","참가요일","시간","회비"]

##dic 초기화
dic={}
for col in my_columns:
    dic[col]=list()

##데이터 가져오기
html = requests.get("http://www.sbsports.or.kr/sub/wrcAble.do").text
htmlAll = bs(html,'html.parser')

## 모든 표 df로 만들기
df_list = pd.read_html(html,header=0)

## 프로그램 이름 리스트
tableNames = htmlAll.find_all('caption')
tb_names_list = [name.text.strip() for name in tableNames]
name_dic = {"구분":[]}

for i in range(len(tb_names_list)):

    ##현재 테이블의 컬럼 가져오기
    current_col = df_list[i].columns.tolist()
    for name in current_col:
        df_list[i]=df_list[i].rename({name:name.replace(" ","")},axis=1)
    current_col = df_list[i].columns.tolist()

    ## 3중 for문 등 여러 문제로 인해 하드한 코딩으로 진행함
    for col in current_col:
        if col == "비고":
            current_col.remove(col)
        elif col == "구분":
            df_list[i]=df_list[i].rename({col:"프로그램"},axis=1)
        elif col == "참가요일 및 시간":
            df_list[i]=df_list[i].rename({col:"참가요일"},axis=1)
        elif col == "정원":
            current_col.remove(col)

    inter_col = list(set(my_columns) & set(current_col))
    differ_col = list(set(my_columns).difference(current_col))
    print(inter_col,differ_col)

    ##dic 데이터 추가
    for inter in inter_col:
        for value in df_list[i][inter]:
            dic[inter].append(value)
    for differ in differ_col:
        for _ in range(len(df_list[i][inter_col[0]])):
            dic[differ].append("")
    for _ in range(len(df_list[i][inter_col[0]])):
        name_dic["구분"].append(tb_names_list[i][:-3]+"프로그램" if tb_names_list[i].find("테이블")!=-1 else tb_names_list[i])
dic.update(name_dic)

print(pd.DataFrame(dic))## 컬럼 재 정렬 필요

