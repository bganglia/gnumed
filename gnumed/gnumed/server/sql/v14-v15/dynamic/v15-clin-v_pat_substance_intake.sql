-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1
set check_function_bodies to 1;
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_pat_substance_intake cascade;
\set ON_ERROR_STOP 1

create view clin.v_pat_substance_intake as

-- brands
select
	c_si.pk
		as pk_substance_intake,
	(select fk_patient from clin.encounter where pk = c_si.fk_encounter)
		as pk_patient,
	c_si.soap_cat,
	r_bd.description
		as brand,
	r_bd.preparation,
	r_cs.description
		as substance,
	r_cs.amount,
	r_cs.unit
		as unit,

	r_cs.atc_code
		as atc_substance,
	r_bd.atc_code
		as atc_brand,
	r_bd.external_code
		as external_code_brand,
	r_bd.external_code_type
		as external_code_type_brand,

	c_si.clin_when
		as started,
	c_si.intake_is_approved_of,
	c_si.schedule,
	c_si.duration,
	c_si.discontinued,
	c_si.discontinue_reason,
	c_si.is_long_term,
	c_si.aim,
	cep.description
		as episode,
	c_si.narrative
		as notes,
	r_bd.is_fake
		as fake_brand,
	-- currently active ?
	case
		-- no discontinue date documented so assumed active
		when c_si.discontinued is null then true
		-- else not active (constraints guarantee that .discontinued > clin_when and < current_timestamp)
		else false
	end::boolean
		as is_currently_active,
	-- seems inactive ?
	case
		when c_si.discontinued is not null then true
		-- from here on discontinued is NULL
		when c_si.clin_when is null then
			case
				when c_si.is_long_term is true then false
				else null
			end
		-- from here clin_when is NOT null
		when (c_si.clin_when > current_timestamp) is true then true
		when ((c_si.clin_when + c_si.duration) < current_timestamp) is true then true
		when ((c_si.clin_when + c_si.duration) > current_timestamp) is true then false
		else null
	end::boolean
		as seems_inactive,
	r_ls2b.fk_brand
		as pk_brand,
	r_bd.fk_data_source
		as pk_data_source,
	r_ls2b.fk_substance
		as pk_substance,
	r_ls2b.pk
		as pk_drug_component,
	c_si.fk_encounter
		as pk_encounter,
	c_si.fk_episode
		as pk_episode,
	cep.fk_health_issue
		as pk_health_issue,
	c_si.modified_when,
	c_si.modified_by,
	c_si.row_version
		as row_version,
	c_si.xmin
		as xmin_substance_intake
from
	clin.substance_intake c_si
		inner join ref.lnk_substance2brand r_ls2b on (c_si.fk_drug_component = r_ls2b.pk)
			inner join ref.branded_drug r_bd on (r_ls2b.fk_brand = r_bd.pk)
			inner join ref.consumable_substance r_cs on (r_ls2b.fk_substance = r_cs.pk)
				left join clin.episode cep on (c_si.fk_episode = cep.pk)

where
	c_si.fk_drug_component is not null


			union all


-- substances w/o brands
select
	c_si.pk
		as pk_substance_intake,
	(select fk_patient from clin.encounter where pk = c_si.fk_encounter)
		as pk_patient,
	c_si.soap_cat,
	null::text
		as brand,
	c_si.preparation,
	r_cs.description
		as substance,
	r_cs.amount,
	r_cs.unit
		as unit,
	r_cs.atc_code
		as atc_substance,
	null::text
		as atc_brand,
	null::text
		as external_code_brand,
	null::text
		as external_code_type_brand,

	c_si.clin_when
		as started,
	c_si.intake_is_approved_of,
	c_si.schedule,
	c_si.duration,
	c_si.discontinued,
	c_si.discontinue_reason,
	c_si.is_long_term,
	c_si.aim,
	cep.description
		as episode,
	c_si.narrative
		as notes,
	null::boolean
		as fake_brand,
	-- currently active ?
	case
		-- no discontinue date documented so assumed active
		when c_si.discontinued is null then true
		-- else not active (constraints guarantee that .discontinued > clin_when and < current_timestamp)
		else false
	end::boolean
		as is_currently_active,
	-- seems inactive ?
	case
		when c_si.discontinued is not null then true
		-- from here on discontinued is NULL
		when c_si.clin_when is null then
			case
				when c_si.is_long_term is true then false
				else null
			end
		-- from here clin_when is NOT null
		when (c_si.clin_when > current_timestamp) is true then true
		when ((c_si.clin_when + c_si.duration) < current_timestamp) is true then true
		when ((c_si.clin_when + c_si.duration) > current_timestamp) is true then false
		else null
	end::boolean
		as seems_inactive,
	null::integer
		as pk_brand,
	null::integer
		as pk_data_source,
	r_cs.pk
		as pk_substance,
	null::integer
		as pk_drug_component,
	c_si.fk_encounter
		as pk_encounter,
	c_si.fk_episode
		as pk_episode,
	cep.fk_health_issue
		as pk_health_issue,
	c_si.modified_when,
	c_si.modified_by,
	c_si.row_version
		as row_version,
	c_si.xmin
		as xmin_substance_intake
from
	clin.substance_intake c_si
		inner join ref.consumable_substance r_cs on (c_si.fk_substance = r_cs.pk)
			left join clin.episode cep on (c_si.fk_episode = cep.pk)

where
	c_si.fk_drug_component is null


;

grant select on clin.v_pat_substance_intake to group "gm-doctors";

-- --------------------------------------------------------------
select gm.log_script_insertion('v12-clin-v_pat_substance_intake.sql', '1.1');

-- ==============================================================
