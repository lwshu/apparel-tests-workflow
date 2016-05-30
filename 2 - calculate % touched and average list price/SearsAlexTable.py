# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 23:08:03 2016

@author: lshu0
"""

def SearsAlexAllItem(year_week,week_number, test_name):
    
    table_names={'.00 Pricing Strategy':'00PS','Basics 1':'B1','Basics 2':'B2','Blackout':'Neg','Seasonal Variation':'SV','Simple Messaging Test':'SM'}
    table_name = table_names[test_name]
    query ="""
create table shc_work_tbls.all_item_alex_{tbl_nm}_week{wk_no} as (
select	
	a12.DIV_NBR  DIV_NBR,
	a12.LN_ID  LN_ID,
	max(a12.LN_NBR)  LN_NBR,
	a12.PRD_IRL_NBR  PRD_IRL_NBR,
	max(a12.ITM_NBR)  ITM_NBR0,
	a15.PRD_SUB_ATTR_ID  PRD_SUB_ATTR_ID,
	max(a15.PRD_SUB_ATTR_NM)  PRD_SUB_ATTR_NM,
	sum( CASE WHEN a11.SLS_TYP_CD not in ('M') THEN a11.TRS_SLL_DLR*a11.TY_CTR  end)  SEARSTOTALSALES,
	sum( CASE WHEN a11.SLS_TYP_CD not in ('M') THEN a11.TRS_UN_QT*a11.TY_CTR  end)  SEARSTOTALSALESUNITS,
	sum( CASE WHEN a11.SLS_TYP_CD not in ('M') THEN a11.TRS_CST_DLR*a11.TY_CTR  end)  SEARSCOSTOFMDSESOLD
from	ALEX_ARP_VIEWS_PRD.FACT_SRS_WKLY_OPR_SLS_TYLY	a11
	join	ALEX_ARP_VIEWS_PRD.LU_SRS_PRODUCT_SKU	a12
	  on 	(a11.SKU_ID = a12.SKU_ID)
	join	ALEX_ARP_VIEWS_PRD.REF_SRS_PRD_PROD_ATTR	a13
	  on 	(a12.PRD_IRL_NBR = a13.PRD_IRL_NBR)
	join	ALEX_ARP_VIEWS_PRD.LU_MCT_PRD_ATTR_SSN	a14
	  on 	(a13.ATTR_SE_VALU = a14.PRD_VALU_KEY)
	join	(Select   PRD_SUB_ATTR_ID, PRD_SUB_ATTR_NM, PRD_VALU_KEY, PRD_VALU_ID, PRD_VALU_NM
From     ALEX_ARP_VIEWS_PRD.LU_MCT_PRD_ATTR_SSN 
Where PRD_SUB_ATTR_ID > 10000
And PRD_VALU_CD <> 'FFFF')	a15
	  on 	(a14.PRD_VALU_ID = a15.PRD_VALU_ID)
	join	ALEX_ARP_VIEWS_PRD.LU_SHC_WEEKS	a16
	  on 	(a11.WK_NBR = a16.WK_NBR)
where	(a12.MRCH_NBR in (20000)
 and a11.WK_NBR in ({yr_wk})
 and a11.LOCN_NBR in (
 
 sel locn from shc_work_tbls.sears_all_stores where test_nm = '{test_nm}' and wk_no = {wk_no}
 
 )
 and a11.TRS_TYP_CD in ('A', 'R', 'S')
 and a11.TYLY_DESC in ('TY'))
group by	
	a12.DIV_NBR,
	a12.LN_ID,
	a12.PRD_IRL_NBR,
	a15.PRD_SUB_ATTR_ID

)
with data primary index ( DIV_NBR, ITM_NBR0)

    """.format(tbl_nm=table_name, yr_wk = year_week, wk_no = week_number, test_nm = test_name)
    return query
    
