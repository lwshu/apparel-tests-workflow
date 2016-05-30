# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:47:30 2016

@author: lshu0
"""

def KmartAlexTable (year_week,week_number, test_name):
    table_names={"Basics Combine":'BasiC','Blackout (no DW)':'NegNoDW','Blackout w DW':'BDW','Kmart Seasonal Dec':'SeaDec',"Kmart Seasonal Inc":'SeaInc'}
    table_name = table_names[test_name]
    query = """
create table shc_work_tbls.all_item_kmart_{tbl_nm}_week{wk_no} as (
select	a12.DVSN_NBR  DVSN_NBR,
	max(a12.DVSN_DESC)  DVSN_DESC,
	a12.CATG_ID  CATG_ID,
	max(a12.CATG_DESC)  CATG_DESC,
	max(a12.DVSN_NBR)  DVSN_NBR0,
	max(a12.CATG_NBR)  CATG_NBR,
	a12.KSN_ID  KSN_ID,
	max(a12.KSN_DESC)  KSN_DESC,
	a11.WK_NBR  WK_NBR,
	max(Substr(a15.WK_NBR,10,11)||' '|| a15.WK_END_DT)  WK_DESC0,
	a13.MST_SSN_CD  MST_SSN_CD,
	max(a14.MST_SSN_DESC)  MST_SSN_DESC,
	sum((a11.TRS_SLL_DLR * a11.TY_CTR))  KMARTTOTALSALES,
	sum((a11.TRS_UN_QT * a11.TY_CTR))  KMARTTOTALSALESUNITS,
	sum((a11.TRS_CST_DLR * a11.TY_CTR))  KMARTCOSTOFMDSESOLD
from	ALEX_ARP_VIEWS_PRD.FACT_SHC_WKLY_OPR_SLS_TYLY	a11
	join	ALEX_ARP_VIEWS_PRD.LU_SHC_VENDOR_PACK	a12
	  on 	(a11.VEND_PACK_ID = a12.VEND_PACK_ID)
	join	ALEX_ARP_VIEWS_PRD.REF_SHC_SSN_TO_MST_SSN	a13
	  on 	(a12.SHC_SSN_CD = a13.SHC_SSN_CD and 
	a12.SSN_YR_NBR = a13.SSN_YR_NBR)
	join	ALEX_ARP_VIEWS_PRD.LU_SHC_MST_SSN	a14
	  on 	(a13.MST_SSN_CD = a14.MST_SSN_CD)
	join	ALEX_ARP_VIEWS_PRD.LU_SHC_WEEKS	a15
	  on 	(a11.WK_NBR = a15.WK_NBR)
where	(a12.MRCH_NBR in (10000)
 and a11.WK_NBR in ({yr_wk})
 and a11.LOCN_NBR in (
sel locn from shc_work_tbls.kmart_all_stores where test_nm = '{test_nm}' and wk_no = {wk_no} 
 )
 and a11.TRS_TYP_CD in ('A', 'R', 'S')
 and a11.TYLY_DESC in ('TY'))
group by	a12.DVSN_NBR,
	a12.CATG_ID,
	a12.KSN_ID,
	a11.WK_NBR,
	a13.MST_SSN_CD
) with data primary index (DVSN_NBR, KSN_ID)
    """.format(tbl_nm=table_name, yr_wk = year_week, wk_no = week_number, test_nm = test_name)
    return query