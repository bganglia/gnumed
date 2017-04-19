-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
drop view if exists clin.v_pat_vaccs4indication cascade;

create view clin.v_pat_vaccs4indication as
select
	c_enc.fk_patient
		as pk_patient,
	c_shot.pk
		as pk_vaccination,
	c_shot.clin_when
		as date_given,
	r_dp.description
		as vaccine,
	_(r_s.atc || '-target', 'en')
		as indication,
	case
		when _(r_s.atc || '-target') = (r_s.atc || '-target') then _(r_s.atc || '-target', 'en')
		else _(r_s.atc || '-target')
	end
		as l10n_indication,
	c_shot.site
		as site,
	c_shot.batch_no
		as batch_no,
	c_shot.reaction
		as reaction,
	c_shot.narrative
		as comment,
	c_shot.soap_cat
		as soap_cat,

	c_shot.modified_when
		as modified_when,
	c_shot.modified_by
		as modified_by,
	c_shot.row_version
		as row_version,

	c_shot.fk_vaccine
		as pk_vaccine,

	r_s.atc
		as atc_indication,
	c_shot.fk_provider
		as pk_provider,
	c_shot.fk_encounter
		as pk_encounter,
	c_shot.fk_episode
		as pk_episode,

	c_shot.xmin
		as xmin_vaccination
from
	clin.vaccination c_shot
		join clin.encounter c_enc on (c_enc.pk = c_shot.fk_encounter)
		join ref.vaccine r_v on (r_v.pk = c_shot.fk_vaccine)
			join ref.drug_product r_dp on (r_dp.pk = r_v.fk_drug_product)
				join ref.lnk_dose2drug r_ld2d on (r_ld2d.fk_drug_product = r_dp.pk)
					join ref.dose r_d on (r_d.pk = r_ld2d.fk_dose)
						join ref.substance r_s on (r_s.pk = r_d.fk_substance)
;

comment on view clin.v_pat_vaccs4indication is
	'Lists all vaccinations for each indication for patients';

grant select on clin.v_pat_vaccs4indication to group "gm-doctors";

-- --------------------------------------------------------------
select gm.log_script_insertion('v22-clin-v_pat_vaccs4indication.sql', '22.0');
