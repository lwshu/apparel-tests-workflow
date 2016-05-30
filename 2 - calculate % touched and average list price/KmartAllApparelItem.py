# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 17:02:46 2016

@author: lshu0
"""

def KmartAllApparelItem(year_week,week_number, test_name):
    table_names={"Basics Combine":'BasiC','Blackout (no DW)':'NegNoDW','Blackout w DW':'BDW','Kmart Seasonal Dec':'SeaDec',"Kmart Seasonal Inc":'SeaInc'}
    table_name = table_names[test_name]
    if test_name in ['Basics 1','Basics 2','Basics Combine']:
        basics = '='
    else:
        basics = '<>'
    query = """
select sum(KMARTTOTALSALES), sum(KMARTTOTALSALESUNITS), sum(KMARTTOTALSALES)-sum(KMARTCOSTOFMDSESOLD) 
 from shc_work_tbls.all_item_kmart_{tbl_nm}_week{wk_no} a join shc_work_tbls.Kmart_Apparel_Div_Cat b
 on a.DVSN_NBR  =b.div_no  and a.CATG_NBR  =b.cat_no
 where MST_SSN_DESC {bs} 'Basic';
    """.format(tbl_nm=table_name, wk_no = week_number, test_nm = test_name, bs=basics)
    return query