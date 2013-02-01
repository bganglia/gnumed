-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
INSERT INTO dem.message_inbox (
	fk_staff,
	fk_inbox_item_type,
	comment,
	data
) VALUES (
	(select pk from dem.staff where db_user = 'any-doc'),
	(select pk_type from dem.v_inbox_item_type where type = 'memo' and category = 'administrative'),
	'Release Notes for GNUmed 1.2.8 (database v17.8)',
	'GNUmed 1.2.8 Release Notes:

	1.2.8

FIX: backport existence check in expando layout handling
FIX: exception on adding duplicate active name [thanks J.Busser]

IMPROVED: LaTeX -\normalsize SOAPU in formatting encounters [thanks V.Banait]
IMPROVED: $<progress_notes>$ placeholder: template handling
IMPROVED: $<emr_journal>$ placeholder: time_range can be any PG interval
IMPROVED: instrument code to track list widget bug
');

-- --------------------------------------------------------------
