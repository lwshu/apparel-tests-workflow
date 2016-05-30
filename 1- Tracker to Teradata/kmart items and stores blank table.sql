drop table  shc_work_tbls.kmart_all_items;
drop table shc_work_tbls.WT_kmart_all_items;
drop table shc_work_tbls.ET_kmart_all_items;
drop table shc_work_tbls.UV_kmart_all_items;
drop table shc_work_tbls.kmart_all_stores;
drop table shc_work_tbls.WT_kmart_all_stores;
drop table shc_work_tbls.ET_kmart_all_stores;
drop table shc_work_tbls.UV_kmart_all_stores;
create table shc_work_tbls.kmart_all_items
(
wk_no varchar(25),
div_no varchar(25),
ksn varchar(25),
test_nm varchar(25)
);
create table shc_work_tbls.kmart_all_stores
(
wk_no varchar(25),
locn varchar(25),
test_nm varchar(25)
);