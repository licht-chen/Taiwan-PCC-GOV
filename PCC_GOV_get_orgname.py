# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 15:02:09 2022

@author: user
"""
import requests
from bs4 import BeautifulSoup
import os
from configparser import ConfigParser
pcc_url = "https://web.pcc.gov.tw"
origin_url = "https://web.pcc.gov.tw/prkms/tender/common/orgName/indexTenderOrgName?searchType=advanced"
path = os.getcwd()
def orgname_get(path, filename):
    filename = "Config.ini"
    filename_list = os.listdir(path)
    # print(filename_list)
    config = ConfigParser()
    if filename not in filename_list :
        print("Download vender information")
        vender_inf = pcc_gov_get_orgname()
        config["orgname"] = vender_inf
        config.write(open(filename,"w"))
    else:
        print("Read vender information")
        config.optionxform = str  ##更改設定，保留大小寫
        config.read(filename)
        vender_inf = {}
        for key, value in config.items("orgname"):
            vender_inf[key] = value
        
    return vender_inf

def pcc_gov_get_orgname():
    ### link OrgName page
    res = requests.get(origin_url)
    Soup = BeautifulSoup(res.text,'html.parser')
    # find table
    table_information = list(Soup.find_all("table",{"class":"tb_03c"}))[1]
    # get all <a>
    vender_a = list(table_information.find_all("a"))
    vender_inf = {}
    for i in range(len(vender_a)):
        href = pcc_url + vender_a[i]['href']
        vender_res = requests.get(href)
        Soup = BeautifulSoup(vender_res.text,'html.parser')
        table_information = Soup.find("table",{"align":"center"})
        vender_page = list(table_information.find_all("tr"))
        for j in range(1, len(vender_page)):
            temp_vender = list(vender_page[j].find_all("td"))
            if len(temp_vender) > 1:
                vender_inf[temp_vender[0].get_text()] = temp_vender[1].get_text()
    return vender_inf

def main():
    # print(path)
    return orgname_get(path,'Config.ini')
# if __name__ == "__main__":
#     main()
