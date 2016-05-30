# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 19:57:21 2016

@author: lshu0
"""

import pandas as pd
path='C:/Users/lshu0/Documents/apparel tracker uploader/Store List and Item List Summary- Kmart.xlsx'
xls = pd.ExcelFile(path)
sheets=xls.sheet_names

items=[]
stores=[]

for sheet in sheets:
    df=xls.parse(sheet)
    test_nm=sheet.split('-')[0].strip()
    cname=[i.split('.')[0].split(' ')[1] for i in df.columns]
    df.columns=[cname,df.iloc[0]]
    df.columns.names=['week_no','info']
    df=df.drop(0)
    df2=df.stack('week_no')
    df2.reset_index(level=1, inplace=True)
    
    store_list = df2[['week_no','Test Store List']]
    store_list.dropna(subset = ['Test Store List'],inplace=True)
    store_list['test_nm'] = test_nm
    
    item_list=df2[['week_no','Div','Item']]
    item_list.dropna(subset = ['Div','Item'], how='all',inplace=True)
    item_list['test_nm'] = test_nm
    
    items.append(item_list)
    stores.append(store_list)
    
all_items=pd.concat(items)
all_items.drop_duplicates(inplace=True)
all_stores=pd.concat(stores)
all_stores.drop_duplicates(inplace=True)

all_items.to_csv('C:/Users/lshu0/Documents/apparel tracker uploader/all_item_kmart.txt', header=None, index=None, sep=',')
all_stores.to_csv('C:/Users/lshu0/Documents/apparel tracker uploader/all_stores_kmart.txt',header=None, index=None, sep=',')