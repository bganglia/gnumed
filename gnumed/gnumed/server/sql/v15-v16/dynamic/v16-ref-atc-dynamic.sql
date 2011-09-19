-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
-- 
-- ==============================================================
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop trigger tr_upd_ref_code_tbl_check_backlink on ref.atc;
drop trigger tr_del_ref_code_tbl_check_backlink on ref.atc;
\set ON_ERROR_STOP 1


-- UPDATE
create trigger tr_upd_ref_code_tbl_check_backlink
	before update on ref.atc
		for each row execute procedure ref.trf_upd_ref_code_tbl_check_backlink();

-- DELETE
create trigger tr_del_ref_code_tbl_check_backlink
	before update on ref.atc
		for each row execute procedure ref.trf_del_ref_code_tbl_check_backlink();

-- --------------------------------------------------------------
select gm.log_script_insertion('v16-ref-atc-dynamic.sql', '1.0');

-- ==============================================================