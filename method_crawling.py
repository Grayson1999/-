from itertools import count
from cv2 import merge
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from scipy.fftpack import diff

class Total_crawling():
    def __init__(self):
        # self.columns = ["프로그램 명","설명","담당자 이름","담당기관","담당자 연락처","신청자격","신청방법","연결 URL"]
        pass
    
    ##초기 변수 셋팅
    def initial_setting(self,sitename,col_list):
        self.dic={}
        self.my_columns = col_list
        for col in self.my_columns:
            self.dic[col]=list()
        self.name_dic={"담당기관":[],"담당자연락처":[],"연결URL":[]}
        self.sitename = sitename


    ## 프로그램 사이트 url 찾기
    def find_data(self,url,program_page=""):
        self.html = requests.get(url+program_page).text
        self.htmlAll = bs(self.html,'html.parser')

    
    ## dic, name_dic 변수에 데이터 추가
    def col_append_data(self, df, site_name,siteNumber,siteURL, current_col=[], differ_col = []):
        for col in current_col:
            for value in df[col]:
                self.dic[col].append(value)
        if len(differ_col) != 0:
            for differ in differ_col:
                for _ in range(len(df[col])):
                    self.dic[differ].append("")
        for _ in range(len(df[current_col[0]].values)):
            self.name_dic["담당기관"].append(site_name)
            self.name_dic["담당자연락처"].append(siteNumber)
            self.name_dic["연결URL"].append(siteURL)
    

    def dic_to_csv(self):
        sort_columns = list(self.my_columns)
        sort_columns.insert(3,"담당기관")
        sort_columns.insert(4,"담당자연락처")
        sort_columns.insert(-1,"연결URL")
        result_df = pd.DataFrame(self.dic)
        result_df = result_df[sort_columns]
        result_df.to_csv('./{}.csv'.format(self.sitename), sep=',', na_rep='NaN',encoding="utf-8-sig", index=False)


    def sbsports(self):##서부재활체육센터
        sitename = "서부재활체육센터"        
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]#,"담당기관","담당자연락처","연결URL"
        url = "http://www.sbsports.or.kr/sub/wrcAble.do"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        siteNumber = self.htmlAll.find("ul",{"class":"clearfix"}).find_all("li")[1].text[5:-2]
        df_list = pd.read_html(self.html,header=0)
        # tb_name_list = [x.text.strip() for x in self.htmlAll.find_all("caption")]

        for i in range(len(df_list)):#len(df_list)
            ##현재 테이블의 컬럼 가져오기
            current_col = df_list[i].columns.tolist()
            for name in current_col:
                df_list[i]=df_list[i].rename({name:name.replace(" ","")},axis=1)
            current_col = df_list[i].columns.tolist()

            merge_cols = []##["참가요일","시간","회비"] => 설명 컬럼에 병합해서 넣기
            for col in current_col:
                if col == "비고":
                    current_col.remove(col)
                if col == "구분" or col == "프로그램":
                    df_list[i]=df_list[i].rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "참가요일 및 시간" or col == "참가요일":
                    df_list[i]=df_list[i].rename({col:"참가요일"},axis=1)
                    merge_cols.append("참가요일")
                    # current_col.remove(col)
                    # current_col.append("참가요일")
                    current_col.remove(col)
                if col == "정원":
                    current_col.remove(col)
                if col == "프로그램.1":
                    current_col.remove(col)
                if col == "대상":
                    df_list[i]=df_list[i].rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
                if col == "시간":
                    merge_cols.append("시간")
                if col == "회비":
                    merge_cols.append("회비")
            
            ## 설명 컴럼 추가
            current_col.append("설명")
            df_list[i]['설명'] =df_list[i][merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))

            self.col_append_data(df_list[i],sitename,siteNumber,url, current_col = inter_col, differ_col = differ_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()
    
    
    def sbsd(self):#서부산권장애인스포츠센터
        sitename = "서부산권장애인스포츠센터"
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]
        url = "https://www.sbsd.kr/Home/"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        program_page = self.htmlAll.find("li",{"class":"cd1 cd1c4"}).find("a")["href"].split("/")[-1]
        self.find_data(url,program_page=program_page)
        siteNumber = " ".join(self.htmlAll.find("address",{"class":"foot_in"}).find("span").text.split()[2:4])
        print(siteNumber)
        pages = self.htmlAll.find('nav',{"class":"tabmenu"}).find_all("li",{"class":"cd3"})
        programURLs = []
        
        for elem in pages:
            programURLs.append(elem.find("a")["href"].split("/")[-1])   ## 페이지 넘버
        for i in range(len(programURLs)):
            self.find_data(url,program_page = programURLs[i])
            initial_df = pd.read_html(self.html,header=0)[0]
            current_col = initial_df.columns.tolist()
            merge_cols = []
            for col in current_col:
                if col == "프로그램":
                    initial_df = initial_df.rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "교육일":
                    current_col.remove(col)
                    merge_cols.append("교육일")
                if col == "대상":
                    initial_df = initial_df.rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
                if col == "시간":
                    current_col.remove(col)
                    merge_cols.append("시간")
                if col == "사용료":
                    current_col.remove(col)
                    merge_cols.append("사용료")
                if col == "정원":
                    current_col.remove(col)
                    merge_cols.append("정원")
            current_col.append("설명")
            initial_df['설명'] =initial_df[merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))
            self.col_append_data(initial_df,sitename,siteNumber,url+programURLs[i], current_col = inter_col,differ_col=differ_col)
            # for col in current_col:
            #     for value in initial_df[col]:
            #         self.dic[col].append(value)
            # for _ in range(len(initial_df[current_col[0]].values)):
            #     self.name_dic["담당기관"].append(sitename)
            #     self.name_dic["담당자연락처"].append(siteNumber)
            #     self.name_dic["연결URL"].append(url)
            
            
        self.dic.update(self.name_dic)
        self.dic_to_csv()
    
    
    def bisco(self):#부산한마음스포츠센터
        sitename = "부산한마음스포츠센터"
        my_columns = ["프로그램명","설명","담당자이름","신청자격","신청방법"]
        url = "http://hmsports.bisco.or.kr"
        self.initial_setting(sitename,my_columns)
        self.find_data(url)
        program_page = self.htmlAll.find_all("li",{"class":"mn_li1"})[1].find("a")["href"]
        self.find_data(url,program_page=program_page)
        siteNumber = ""
        pages = self.htmlAll.find_all("ul",{"class":"depth2"})[-1].find_all("a")
        programURLs = [url["href"] for url in pages]
        del programURLs[-1]## 통합방과후학교 삭제
        del programURLs[4]## 실내골프연습장 삭제
        del programURLs[2]## 피트니스실 삭제      
        for purl in programURLs:
            self.find_data(url,program_page=purl)
            initial_df = pd.read_html(self.html,header=0)[0]
            current_col = initial_df.columns.tolist()
            merge_cols = ["반","교육일","시간"]
            for col in current_col:
                print(col)
                if col == "프로그램":
                    initial_df = initial_df.rename({col:"프로그램명"},axis=1)
                    current_col.remove(col)
                    current_col.append("프로그램명")
                if col == "대상":
                    initial_df = initial_df.rename({col:"신청자격"},axis=1)
                    current_col.remove(col)
                    current_col.append("신청자격")
            current_col.append("설명")
            initial_df['설명'] =initial_df[merge_cols].apply(lambda row: '; '.join(row.values.astype(str)), axis=1) ##;(세미콜론)으로 구분
            inter_col = list(set(self.my_columns) & set(current_col))
            differ_col = list(set(self.my_columns).difference(current_col))
            self.col_append_data(initial_df,sitename,siteNumber,url+purl, current_col = inter_col,differ_col=differ_col)
        self.dic.update(self.name_dic)
        self.dic_to_csv()

s = Total_crawling()
# s.sbsports()
# s.sbsd()
s.bisco()