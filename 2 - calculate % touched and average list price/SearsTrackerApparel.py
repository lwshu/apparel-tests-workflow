# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 14:12:45 2016

@author: lshu0
"""

def SearsTrackerApparel(year_week,week_number, test_name):
    table_names={'.00 Pricing Strategy':'00PS','Basics 1':'B1','Basics 2':'B2','Blackout':'Neg','Seasonal Variation':'SV','Simple Messaging Test':'SM'}
    table_name = table_names[test_name]
    query = """
select sum(SEARSTOTALSALES), sum( SEARSTOTALSALESUNITS) , sum(SEARSTOTALSALES)- sum(SEARSCOSTOFMDSESOLD)
 from
shc_work_tbls.all_item_alex_{tbl_nm}_week{wk_no} a join shc_work_tbls.sears_all_items  b 
on a.DIV_NBR   =b.div_no  and  a.ITM_NBR0  = b.itm_no
where test_nm = '{test_nm}' and wk_no= {wk_no}
    """.format(tbl_nm=table_name, wk_no = week_number, test_nm = test_name)
    return query