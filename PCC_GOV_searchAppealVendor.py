# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 22:42:51 2021

@author: user
"""
"""
公開徵求
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
# import urllib #中文網頁轉碼
import os
from datetime import date
import time
import json
import re

today = date.today()
headlist = ["項次", "機關名稱", "標案案號", "標案名稱", "公告次數", "公開徵求", "功能選項",
            "公開徵求公告網址"]
origin_href = "https://web.pcc.gov.tw/prkms/tpAppeal/common/readTpAppeal/advanced/returnToBasic?"
project_href = "https://web.pcc.gov.tw/tps/tp/common/TpAppeal/query/getInitialAppealView?pkTA="
url = origin_href
### 特殊字元 replace
def replace_string(string):
    string = string.replace('\xa0',"")
    string = string.replace('\r',"")
    string = string.replace(" ","")
    string = string.replace('\t',"")
    string = string.replace('\n',"")
    string = string.replace('\u3000',"")
    string = string.replace('\u2002',"")
    string = string.replace('\u2003',"")
    return string
def request_html(url, Payload, page):
    # res = requests.post(url,data=payload,headers=headers)
    if int(page) > 1:
        # print(page)
        res = requests.get(url)
    else:
        res = requests.get(url,params = Payload)
    Soup = BeautifulSoup(res.text,'html.parser')
    return Soup
def page_information(Soup):
    temp_page_url = {}
    ### Find page
    temp_page_data_number = 0
    for i in Soup.find("div",{"class":"page"}).find_all("a"):
        if i.text not in ["第一頁", "下一頁" ,"最後一頁","1"]:
            temp_page_url[i.text] = origin_href + i['href'].replace('?','')
    ### total data numbers in this searching
    total_data_count = int(Soup.find("span",{"id":"pagebanner"}).find("span").get_text().replace(" ",""))
    return temp_page_url, total_data_count
def get_project_name(element,element_id):
    var = element.find("span",{"id":str(element_id)})
    project_name = var.find("script").string
    compile = re.compile('var hw = Geps3.CNS.pageCode2Img(.*?);')
    project_name = compile.match(project_name).groups()[0]
    project_name = project_name.split('("')[1].split('")')[0]
    return project_name
### First requests html information, and find page information 
def td_information_get(Soup):
    # Soup = request_html(url, payload)
    temp_data = pd.DataFrame()
    ### page url information
    # td_information = {}
    ### Find tbody information
    table_information = Soup.find("table",{"class":"tb_01"})
    html_tbody = list(table_information.find_all('tr'))
    for i in range(1,len(html_tbody)):
        td_list = list(html_tbody[i].find_all('td'))
        temp_list = []
        for j in range(len(td_list)):
            if j ==3:
                temp_list.append(get_project_name(td_list[j],i) )
            elif j == len(td_list)-1:
                temp_list.append(project_href + td_list[j].find("a")['href'].split("pk=")[1])
            else:
                temp_list.append(replace_string(td_list[j].get_text()))
        for j in range(len(temp_list)):
            temp_data.loc[i,headlist[j]] = temp_list[j]
    # html_tr[0]
    return temp_data
def create_filder(mon_path, data, filename):
    pcc_path = mon_path + "PCC_GOV/"
    if os.path.isdir(pcc_path) != True:
        os.makedirs(pcc_path)
        try:
            data.to_csv(pcc_path + filename, index = None, encoding = 'ANSI')
        except:
            data.to_csv(pcc_path + filename, index = None, encoding = 'utf-8')
    else:
        try:
            data.to_csv(pcc_path + filename, index = None, encoding = 'ANSI')
        except:
            data.to_csv(pcc_path + filename, index = None, encoding = 'utf-8')
        print("=== output data ===")
    os.startfile(pcc_path)

def pcc_gov_search_searchVendor(orgname, startdate, enddate, search_type, mon_folder):
    # orgname = '中華郵政'
    # search_type = "公開徵求"
    # orgname = '中央銀行'
    # orgname = '金融監督管理委員會'
    # startdate = "2022/10/03"
    # enddate = "2022/12/03"
    # mon_folder = "D:/"
    Payload = {
            "pageSize":"100",
            "firstSearch":"true",
            "searchType":"advanced",
            "level_1":"on",
            "orgName":orgname,
            "orgId":"",
            "tenderName":"",
            "tenderId":"",
            "tenderType":"SEARCH_APPEAL",
            "dateType":"isDate",
            "startDate":startdate,
            "endDate":enddate,
            "spdtStartDate":"",
            "spdtEndDate":"",
            "opdtStartDate":"",
            "opdtEndDate":"",
            "tenderYmStartY":"",
            "tenderYmStartM":"",
            "tenderYmEndY":"",
            "tenderYmEndM":"",
            "radProctrgCate":"",
            "tenderRange":"TENDER_RANGE_ALL",
            "minBudget":"",
            "maxBudget":"",
            "execLocation":"",
            "location":"",
            "priorityCate":"",
            "radReConstruct":""}
    ### headers 
    # headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    #            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #            "Accept-Encoding": "gzip, deflate, br",
    #            "Accept-Language": "zh-TW,zh;q=0.9",
    #            "Cache-Control": "max-age=0",
    #            "Connection": "keep-alive",
    #            "Sec-Fetch-Dest": "document",
    #            "Sec-Fetch-Mode": "navigate",
    #            "Sec-Fetch-Site": "none",
    #            "Sec-Fetch-User": "?1",
    #            "Upgrade-Insecure-Requests": "1",
    #            "Host": "web.pcc.gov.tw",
    #            "sec-ch-ua": 'Google Chrome;v="107", Chromium;v="107", Not=A?Brand;v="24"',
    #            "sec-ch-ua-mobile": "?0",
    #            "sec-ch-ua-platform": "Windows",
    #            "cookie":'JSESSIONID="tSgZUVv4_TuwysZ2_N4vp-Hc6IHPwfE5JRnSxQBO.aplapp1:instA"; XSRF-TOKEN=bd0a9cc3-1ccf-4d99-8c71-895578f1c408; cookiesession1=678ADA5BEC806D0AF6D66615530EFC33; webpcc=14b5a3d90169c1e5aa1b03402de8c2ebbbb4e4373f5bd8f88db02da12a692bfe9fb2135c'}
    
    ### table search url
    # url = "https://web.pcc.gov.tw/prkms/tender/common/basic/readTenderBasic?firstSearch=truesearchType=basicorgName=%E4%B8%AD%E8%8F%AF%E9%83%B5%E6%94%BF&orgId=&tenderName=&tenderId=&tenderType=TENDER_DECLARATION&tenderWay=TENDER_WAY_ALL_DECLARATION&dateType=isDate&tenderStartDate=2022%2F11%2F01&tenderEndDate=2022%2F11%2F20"
    # keys = list(data.keys())
    # for i in range(len(keys)):
    #     if i == 0:
    #         url = origin_href + keys[i] + "=" + data[keys[i]] + "&"
    #     elif i < len(keys)-1:
    #         url = url + keys[i] + "=" + data[keys[i]] + "&"
    #     else:
    #         url = url + keys[i] + "=" + data[keys[i]]
    print("======", orgname, "======")
    final_table = pd.DataFrame(columns = headlist)
    ### First page html_tr information and page url 
    ### Use data number to find there is data or not in sequence
    print("PAGE 1")
    page = 1
    Soup = request_html(origin_href,Payload,page)
    page_url, total_data_number = page_information(Soup)
    if total_data_number > 0:
        final_table = td_information_get(Soup)
        if len(list(page_url.keys())) > 0:
            for page in list(page_url.keys()):
                Payload["d-49738-p"] = page
                print('sleep 3 sec')
                time.sleep(3)
                print("PAGE "+page)
                Soup = request_html(page_url[page],Payload, page)
                final_table = pd.concat([final_table, td_information_get(Soup)], axis=0)
    if final_table.shape[0] > 0:
        final_table = final_table.reset_index().drop('index',axis=1)
        final_table['項次'] = final_table.index+ 1
        filename = orgname+"_"+search_type+"_"+today.strftime("%Y-%m-%d")+'.csv'
        create_filder(mon_folder, final_table, filename)
        return True
    else:
        print('=== Finish ===')
        return False