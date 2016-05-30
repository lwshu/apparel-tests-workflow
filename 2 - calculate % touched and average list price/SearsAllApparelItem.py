# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:02:29 2016

@author: lshu0
"""

def SearsAllApparelItem(year_week,week_number, test_name):
    table_names={'.00 Pricing Strategy':'00PS','Basics 1':'B1','Basics 2':'B2','Blackout':'Neg','Seasonal Variation':'SV','Simple Messaging Test':'SM'}
    table_name = table_names[test_name]
    if test_name in ['Basics 1','Basics 2']:
        basics = '='
    else:
        basics = '<>'
    query = """
select sum(SEARSTOTALSALES), sum( SEARSTOTALSALESUNITS) , sum(SEARSTOTALSALES)- sum(SEARSCOSTOFMDSESOLD)
from  shc_work_tbls.all_item_alex_{tbl_nm}_week{wk_no} a join  shc_work_tbls.Sears_Apparel_Div_Line b on
a.DIV_NBR = b.div_no and a.LN_NBR= b.ln_no
where PRD_SUB_ATTR_NM {bs} 'BASIC'
    """.format(tbl_nm=table_name, yr_wk = year_week, wk_no = week_number, test_nm = test_name, bs=basics)
    return query