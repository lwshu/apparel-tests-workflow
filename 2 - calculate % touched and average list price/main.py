# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 22:41:31 2016

@author: lshu0
"""
import jaydebeapi
import jpype
import AvgListRegKmart
import AvgListRegSears
import SearsAlexTable
import SearsAllApparelItem
import SearsTrackerApparel
import KmartAlexTable
import KmartAllApparelItem
import KmartTrackerApparel
import pandas as pd

def teraConnection(tduser='lshu0',tdpwd='slw1234'):


    driverClass='com.teradata.jdbc.TeraDriver'
    path='jdbc:teradata://s00t0108.searshc.com'
    classpath = """C:\\Users\\lshu0\\Documents\\Teradata driver\\tdgssconfig.jar;C:\\Users\\lshu0\\Documents\\Teradata driver\\terajdbc4.jar"""
    jvm_path =  u'C:\\Program Files\\Java\\jre7\\bin\\server\\jvm.dll'
    jpype.startJVM(jvm_path, "-Djava.class.path=%s" % classpath)
    conn = jaydebeapi.connect(driverClass,[path,tduser,tdpwd])
    cursor = conn.cursor()
    return cursor

cursor=teraConnection()    
    
sears_test=['Blackout']
kmart_test=["Basics Combine",'Blackout (no DW)','Blackout w DW','Kmart Seasonal Dec',"Kmart Seasonal Inc"]
wk= 201616

ALRS={}
for test_nm in sears_test:
    yr_wk=str(wk)
    wk_no= str(wk%100)
    query=AvgListRegSears.AvgListRegSears(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    rows=cursor.fetchall()
    if len(rows) != 0:
        ALRS[test_nm]=rows[0][8]
        print rows[0]
        
Avg_List_Reg_Sears = pd.DataFrame.from_dict(ALRS,'index')
Avg_List_Reg_Sears.columns = ['AverageListPrice']

ALRK={}        
for test_nm in kmart_test:
    yr_wk=str(wk)
    wk_no= str(wk%100)
    query=AvgListRegKmart.AvgListRegKmart(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    rows=cursor.fetchall()
    if len(rows) != 0:
        ALRK[test_nm]=rows[0][8]
        print rows[0]
    
Avg_List_Reg_Kmart = pd.DataFrame.from_dict(ALRK,'index')
Avg_List_Reg_Kmart.columns = ['AverageListPrice']

SAAI={}
STA={}
for test_nm in sears_test:
    wk_no= str(wk%100)
    yr_wk=str(wk)
    query = SearsAlexTable.SearsAlexAllItem(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    query = SearsAllApparelItem.SearsAllApparelItem(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    rows=cursor.fetchall()
    if len(rows) != 0:
        SAAI[test_nm]=rows[0]
    query = SearsTrackerApparel.SearsTrackerApparel(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    rows=cursor.fetchall()
    if len(rows) != 0:
        STA[test_nm]=rows[0]
        print rows[0]
    
SearsAllApparel = pd.DataFrame.from_dict(SAAI,'index')
SearsAllApparel.columns = ['Total Sales','Total Units','Total Margin']
SearsTracker = pd.DataFrame.from_dict(STA,'index')
SearsTracker.columns= ['Tracker Sales','Tracker Units','Tracker Margin']
Sears = pd.merge(Avg_List_Reg_Sears, SearsAllApparel, left_index= True, right_index = True , how = 'inner')
Sears = pd.merge(Sears, SearsTracker, left_index= True, right_index = True , how = 'inner')
Sears.to_csv('Sears_'+str(wk) +'_list_prc_%touched.csv')

KAAI={}  
KTA={}
for test_nm in kmart_test:
    wk_no= str(wk%100)
    yr_wk=str(wk)
    query = KmartAlexTable.KmartAlexTable(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    query = KmartAllApparelItem.KmartAllApparelItem(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    rows=cursor.fetchall()
    if len(rows) != 0:
        KAAI[test_nm]=rows[0]
    query = KmartTrackerApparel.KmartTrackerApparel(yr_wk,wk_no,test_nm)
    cursor.execute(query)
    rows=cursor.fetchall()
    if len(rows) != 0:
        KTA[test_nm]=rows[0]
        print rows[0]
    
KmartAllApparel = pd.DataFrame.from_dict(KAAI, 'index')
KmartAllApparel.columns=['Total Sales','Total Units','Total Margin']
KmartTracker = pd.DataFrame.from_dict(KTA,'index')
KmartTracker.columns = ['Tracker Sales','Tracker Units','Tracker Margin']
Kmart = pd.merge(Avg_List_Reg_Kmart, KmartAllApparel, left_index= True, right_index = True , how = 'inner')
Kmart = pd.merge(Kmart, KmartTracker, left_index= True, right_index = True , how = 'inner')
Kmart.to_csv('Kmart_'+str(wk) +'list_prc_%touched.csv')
