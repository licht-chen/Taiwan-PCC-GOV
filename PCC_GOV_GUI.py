# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 21:15:49 2021

@author: user
"""

from tkinter import ttk
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import tkinter.font as font
import pandas as pd
# from configparser import ConfigParser
import time
import PCC_GOV_search
import PCC_GOV_searchAppealVendor
import PCC_GOV_QueryPublicReadData
import PCC_GOV_get_orgname
import os
### pcc_gov
def Run_pcc_gov():
    # orgname = orgname_entry.get()
    orgname = orgname_box.get()
    startdate = startdate_entry.get_date()
    enddate = enddate_entry.get_date()
    # print(type(startdate))
    # print(type(enddate))
    search_type = search_type_box.get()
    # mon_folder = folder_box.get()
    home = os.path.expanduser("~")
    mon_folder = os.path.join(home, "Downloads\\")
    if orgname == "":
        result_label.config(text="請輸入機構名稱", font=('標楷體', 20 , "bold"),background='white')
    elif search_type == "":
        result_label.config(text="請輸入招標類型", font=('標楷體', 20 , "bold"),background='white')
    # elif os.path.isdir(mon_folder) != True:
    #     result_label.config(text="您並無該名稱硬碟區\n請重新選取", font=('標楷體', 20 , "bold"),background='white')
    elif (enddate - startdate).days > 93:
        result_label.config(text="起迄時間不可大於93天\n請重新輸入時間", font=('標楷體', 20 , "bold"),background='white')
    else:
        ## datetime to strftime
        startdate = time_to_taiwantime(startdate)
        enddate = time_to_taiwantime(enddate)
        ## data result
        final_result = False
        print('========== ' + search_type + ' ==========')
        if search_type == '招標公告':
            final_result = PCC_GOV_search.pcc_gov_search_basic(orgname, startdate, enddate, 
                                                                search_type, mon_folder)
        elif search_type == '公開徵求':
            final_result = PCC_GOV_searchAppealVendor.pcc_gov_search_searchVendor(orgname, startdate, 
                                                                                  enddate, search_type, mon_folder)
        elif search_type == '公開閱覽':
            final_result = PCC_GOV_QueryPublicReadData.pcc_gov_search_queryPublicReadData(orgname, startdate, 
                                                                                          enddate, search_type, mon_folder)
        if final_result == True:
            result_label.config(text="資料整併完畢", font=('標楷體', 20 , "bold"),background='white')
        elif final_result == False:
            result_label.config(text="該機構無相關資料", font=('標楷體', 20 , "bold"),background='white')
def time_to_taiwantime(string):
    string = string.strftime("%Y/%m/%d")
    temp_time = string.split('/')
    # string = temp_time[0] + "%2F" + temp_time[1] + "%2F" + temp_time[2]
    return string
        
## 鼠標滾輪+ tkinter中滾動條
def on_mousewheel(event): 
    shift = (event.state & 0x1) != 0 
    scroll = -1 if event.delta > 0 else 1 
    if shift: 
     can.xview_scroll(scroll, "units") 
    else: 
     can.yview_scroll(scroll, "units") 
### orgname 模糊搜尋 values 回傳     
def combobox_search_value():
    temp_list = []
    for i in orgname_list:
        if orgname_box.get() in i:
            temp_list.append(i)
    orgname_box['values'] = temp_list
    
## close tkinter
def close():
    window.destroy()
window = tk.Tk()
window.title('政府採購網資料查詢系統')
# # window.geometry('600x900+500+0')
# window.state("zoomed")
# window.configure(background = '#F0FFFF')
## 畫布設定
can = tk.Canvas(window, width = 400, height = 500,  relief = 'raised', bg = '#F0FFFF', scrollregion=(0,0,500,500))
                
## 滑動條設定
vbar=tk.Scrollbar(window,orient='vertical', activebackground='black')
vbar.pack(side='right',fill='y')
vbar.config(command=can.yview)
can.config(yscrollcommand=vbar.set)
can.bind_all("<MouseWheel>", on_mousewheel) 
can.pack()

### title
title_label = tk.Label(window, text='政府採購網資料查詢系統', bg = '#F0FFFF', font=('微軟正黑體', 18))
can.create_window(200, 25, window=title_label)

### org name
orgname_list = list(PCC_GOV_get_orgname.main().values())
orgname_label = ttk.Label(window, text='機構名稱', width=18, background = '#F0FFFF', font=('微軟正黑體', 12))
can.create_window(110, 70, window = orgname_label)
# orgname_entry = ttk.Entry(window)
# can.create_window(200, 70, window = orgname_entry)
orgname_box = ttk.Combobox(window, width = 25, values = orgname_list, postcommand = combobox_search_value)
can.create_window(200, 70, window = orgname_box)

### 招標類型
search_type_label = ttk.Label(window, text='招標類型', width=18, background = '#F0FFFF', font=('微軟正黑體', 12))
can.create_window(110, 140, window = search_type_label)
search_type_box = ttk.Combobox(window, width = 25, values=['招標公告', '公開徵求', '公開閱覽'])
can.create_window(200, 140, window = search_type_box)

### time
date_label = ttk.Label(window, text='查詢時間', width=18, background = '#F0FFFF', font=('微軟正黑體', 12))
can.create_window(110, 210, window = date_label)
startdate_entry = DateEntry(window, width= 10, background= "magenta3", foreground= "white",bd=2)
can.create_window(175, 210, window = startdate_entry)
date_label_2 = ttk.Label(window, text='~', width=2, background = '#F0FFFF', font=('微軟正黑體', 12))
can.create_window(240, 210, window = date_label_2)
enddate_entry = DateEntry(window, width= 10, background= "magenta3", foreground= "white",bd=2)
can.create_window(300, 210, window = enddate_entry)

### 儲存的資料夾硬碟
# folder_lebel = ttk.Label(window, text='儲存硬碟(選取本機有的)', width=25, background = '#F0FFFF', font=('微軟正黑體', 12))
# can.create_window(140, 270, window = folder_lebel)
# folder_box = ttk.Combobox(window, values=['D:/','E:/','F:/'], width= 5)
# can.create_window(250, 270, window = folder_box)
# folder_box.current(0)
### result 
## ttk button font style setting
s = ttk.Style(window)
s.configure('my.TButton', font=('微軟正黑體', 12 , "bold"), background = '#F0FFFF')
result_label = ttk.Label(window, background = '#F0FFFF')
can.create_window(200, 340, window = result_label)
calculate_btn = ttk.Button(window, text='分析開始', command=Run_pcc_gov, style='my.TButton')
can.create_window(110, 410, window = calculate_btn)
quit_btn = ttk.Button(window, text="離開", command=close, style='my.TButton')
can.create_window(280, 410, window = quit_btn)
# enddate = ttk.Label(window, text='終止時間', width=18, background = '#F0FFFF', font=('微軟正黑體', 12))
# can.create_window(110, 70, window = startdate)
window.mainloop()