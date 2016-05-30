# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 11:47:09 2016

@author: lshu0
"""


from __future__ import division
import os,glob
import pandas as pd

paths=[]
wd = "C:/Users/lshu0/Documents/Teradata driver/Sears"  # change to directory of all excel files
pattern   = "*.xls"
for x in os.walk(wd):
    paths.extend(glob.glob(os.path.join(x[0],pattern))) 

metrics = ['ASP', 'Margin', 'Sales', 'Quantity']

week = '05/14/2016'  # change to date of Saturday in that week
wk_no = 15  # change to week number
total_site_num = 685 

all_test={}
for path in paths:
    xls = pd.ExcelFile(path)        
    sheets=xls.sheet_names
    test_name=xls.parse(sheets[0]).columns[0]
    print '\n Detected a test "'+ test_name + '"\n'
    test_site_num = int(raw_input('\n Please type in # of test stores\n'))
    
    test_info = {}
    test_info['Week'] = 'Wk'+str(wk_no).zfill(2)
    test_info['Test Name']=test_name
    test_info['Format'] = 'Sears'
    test_info['# of test stores']= test_site_num
    test_info['# of all stores'] = total_site_num
    test_info['% stores touched'] = '{0:.1f}%'.format(test_site_num/total_site_num*100)
    
    for sheet in sheets:
        df=xls.parse(sheet)
        df.columns=df.ix[2]
        df=df.ix[3:]
        df=df.set_index('Date')
        metric = [metric for metric in metrics if metric in sheet][0]
        df['expected']=df['Test actual']-df['Estimated impact']
        df['actual']=df['Test actual']
        df['total expected']=df['expected']*df['Number of sites reporting']
        df['total actual']=df['actual']*df['Number of sites reporting']
        df['total lift']=df['Estimated impact']*df['Number of sites reporting']
        if metric == 'ASP':
            test_info['ASP % Lift'] = df.ix[week,'Lift'] 
            test_info['ASP Test Actual'] = df.ix[week,'actual']
            test_info['ASP Test Expected'] = df.ix[week,'expected']
            test_info['ASP $ Lift'] = df.ix[week,'actual'] - df.ix[week,'expected']
        else:
            test_info[metric + ' Act/st'] = df.ix[week,'actual']
            test_info[metric + ' Exp/st'] = df.ix[week,'expected']
            test_info[metric + ' Test Actual'] = df.ix[week,'total actual']
            test_info[metric + ' Test Expected'] = df.ix[week,'total expected']
            test_info[metric + ' Incremental'] = df.ix[week,'total lift']
            test_info[metric + ' % Lift'] = df.ix[week,'Lift']
    test_info['Total Revenue in Test Stores']=test_info['Sales Test Actual']
    all_test[test_name]=test_info

output=pd.DataFrame(all_test)
output=output.T
metric_list= ['Week','Format','Test Name','# of test stores','# of all stores','% stores touched','Total Revenue in Test Stores','ASP Test Expected','ASP Test Actual','ASP % Lift','ASP $ Lift','Quantity Exp/st','Quantity Act/st','Quantity Test Expected','Quantity Test Actual','Quantity % Lift','Quantity Incremental','Sales Exp/st','Sales Act/st','Sales Test Expected','Sales Test Actual','Sales % Lift','Sales Incremental','Margin Exp/st','Margin Act/st','Margin Test Expected','Margin Test Actual','Margin % Lift','Margin Incremental']
output=output.reindex(columns=metric_list)
output.to_excel('sears_output.xlsx',index= False)
