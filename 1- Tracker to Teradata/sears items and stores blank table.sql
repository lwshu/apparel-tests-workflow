drop table  shc_work_tbls.sears_all_items;
drop table shc_work_tbls.UV_sears_all_items;
drop table shc_work_tbls.sears_all_stores;
drop table shc_work_tbls.UV_sears_all_stores;
create table shc_work_tbls.sears_all_items
(
wk_no varchar(25),
div_no varchar(25),
itm_no varchar(25),
test_nm varchar(25)
);
create table shc_work_tbls.sears_all_stores
(
wk_no varchar(25),
locn varchar(25),
test_nm varchar(25)
);