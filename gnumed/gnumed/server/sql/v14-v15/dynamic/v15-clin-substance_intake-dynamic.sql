-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
-- 
-- ==============================================================
\set ON_ERROR_STOP 1
set check_function_bodies to 'on';
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
-- .fk_drug_component
comment on column clin.substance_intake.fk_drug_component is
	'Links to the component of a branded drug taken by a patient.';

\unset ON_ERROR_STOP
alter table clin.substance_intake drop constraint substance_intake_fk_drug_component_fkey cascade;
drop function audit.ft_upd_substance_intake() cascade;
\set ON_ERROR_STOP 1

alter table clin.substance_intake
	add foreign key (fk_drug_component)
		references ref.lnk_substance2brand(pk)
		on update restrict
		on delete restrict;

update clin.substance_intake set
	fk_drug_component = (
		select pk from ref.lnk_substance2brand r_ls2b where
			r_ls2b.fk_brand = fk_brand
				and
			r_ls2b.fk_substance = (
				select pk from ref.consumable_substance r_cs where
					r_cs.description = (
						select description from clin.consumed_substance c_cs where c_cs.pk = clin.substance_intake.fk_substance
					)	and
					r_cs.amount = tmp_amount
						and
					r_cs.unit = tmp_unit
			)
	)
where
	fk_brand is not null
;

-- --------------------------------------------------------------
-- .fk_substance
comment on column clin.substance_intake.fk_substance is
'Links to a substance the patient is taking.

********************************************* 
DO NOT TRY TO USE THIS TO FIND OUT THE BRAND.

IT WILL BE WRONG.
*********************************************';

alter table clin.substance_intake
	alter column fk_substance
		drop not null;

\unset ON_ERROR_STOP
alter table clin.substance_intake drop constraint substance_intake_fk_substance_fkey cascade;
\set ON_ERROR_STOP 1

update clin.substance_intake set
	fk_substance = (
		select rcs.pk									-- "new" pk
		from ref.consumable_substance rcs
		where
			rcs.description = (						-- with description =
				select ccs.description						-- "old" description
				from clin.consumed_substance ccs
				where ccs.pk = fk_substance
			)	and
			rcs.amount = tmp_amount
				and
			rcs.unit = tmp_unit
	)
where
	fk_drug_component is null
;

update clin.substance_intake set
	fk_substance = NULL
where
	fk_drug_component is not null
;

\unset ON_ERROR_STOP
alter table clin.substance_intake drop constraint clin_subst_intake_either_drug_or_substance cascade;
\set ON_ERROR_STOP 1

alter table clin.substance_intake
	add constraint clin_subst_intake_either_drug_or_substance
		check (
			((fk_drug_component is null) and (fk_substance is not null))
				or
			((fk_drug_component is not null) and (fk_substance is null))
		);

alter table clin.substance_intake
	add foreign key (fk_substance)
		references ref.consumable_substance(pk)
		on update cascade
		on delete cascade;

-- --------------------------------------------------------------
-- .preparation
alter table clin.substance_intake
	alter column preparation
		drop not null;

update clin.substance_intake set
	preparation = null
where
	fk_drug_component is not null
;

\unset ON_ERROR_STOP
alter table clin.substance_intake drop constraint clin_subst_intake_sane_prep cascade;
\set ON_ERROR_STOP 1

alter table clin.substance_intake
	add constraint clin_subst_intake_sane_prep
		check (
			((fk_drug_component is null) and (preparation is not null))
				or
			((fk_drug_component is not null) and (preparation is null))
		);

-- --------------------------------------------------------------
-- cleanup
\unset ON_ERROR_STOP
alter table clin.substance_intake drop column tmp_unit cascade;
alter table clin.substance_intake drop column tmp_amount cascade;
alter table clin.substance_intake drop column fk_brand cascade;
alter table audit.log_substance_intake drop column fk_brand cascade;
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
-- trigger
-- --------------------------------------------------------------

-- INSERT
\unset ON_ERROR_STOP
drop function ref.trf_insert_intake_prevent_duplicate_component_links() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_insert_intake_prevent_duplicate_component_links()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_pk_patient integer;
	_pk_intake integer;
BEGIN
	-- any drug at all ?
	if NEW.fk_drug_component is NULL then
		return NEW;
	end if;

	-- which patient ?
	select fk_patient into _pk_patient
	from clin.encounter
	where pk = NEW.fk_encounter;

	-- already exists ?
	select pk into _pk_intake
	from clin.substance_intake
	where
		fk_encounter in (
			select pk from clin.encounter where fk_patient = _pk_patient
		)
			and
		fk_drug_component = NEW.fk_drug_component
	;

	if FOUND then
		raise exception ''[ref.trf_insert_intake_prevent_duplicate_component_links]: drug component ref.lnk_substance2brand.pk=% already linked to patient=% as clin.substance_intake.pk=%'', NEW.fk_drug_component, _pk_patient, _pk_intake;
	end if;

	return NEW;
END;';

comment on function ref.trf_insert_intake_prevent_duplicate_component_links() is
	'Prevent patient from being put on a particular component twice.';

create trigger tr_insert_intake_prevent_duplicate_component_links
	before insert
	on clin.substance_intake
		for each row execute procedure ref.trf_insert_intake_prevent_duplicate_component_links();

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop function ref.trf_insert_intake_links_all_drug_components() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_insert_intake_links_all_drug_components()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_component_count integer;
	_pk_patient integer;
	_pk_brand integer;
	_pk_component integer;
BEGIN

	-- any drug at all ?
	if NEW.fk_drug_component is NULL then
		return NEW;
	end if;

	-- get the brand we are linking to
	select fk_brand into _pk_brand
	from ref.lnk_substance2brand
	where pk = NEW.fk_drug_component;

	-- how many components therein ?
	select count(1) into _component_count
	from ref.lnk_substance2brand
	where fk_brand = _pk_brand;

	-- only one component ?
	if _component_count = 1 then
		return NEW;
	end if;

	-- which patient ?
	select fk_patient into _pk_patient
	from clin.encounter
	where pk = NEW.fk_encounter;

	-- INSERT all components
	for _pk_component in
		select pk from ref.lnk_substance2brand where fk_brand = _pk_brand
	loop

		-- already there ?
		perform 1 from clin.substance_intake
		where
			fk_encounter in (
				select pk from clin.encounter where fk_patient = _pk_patient
			)
				and
			fk_drug_component = _pk_component
		;

		if FOUND then
			continue;
		end if;

		-- insert
		insert into clin.substance_intake (
			fk_drug_component,				-- differentiate
			clin_when,						-- harmonize (started)
			fk_encounter,					-- harmonize
			fk_episode,						-- required
			soap_cat,						-- harmonize
			schedule,						-- harmonize
			duration,						-- harmonize
			intake_is_approved_of,			-- harmonize
			is_long_term,					-- harmonize
			discontinued,					-- harmonize

			narrative,
			-- preparation,					-- drug components already have preps
			aim,
			discontinue_reason
		) values (
			_pk_component,
			NEW.clin_when,
			NEW.fk_encounter,
			NEW.fk_episode,
			NEW.soap_cat,
			NEW.schedule,
			NEW.duration,
			NEW.intake_is_approved_of,
			NEW.is_long_term,
			NEW.discontinued,

			NEW.narrative,
			-- NEW.preparation,
			NEW.aim,
			NEW.discontinue_reason
		);

	end loop;

	return NEW;
END;';


comment on function ref.trf_insert_intake_links_all_drug_components() is
	'If a patient is put on a multi-component drug they must be put on ALL components thereof.';


create trigger tr_insert_intake_links_all_drug_components
	after insert on clin.substance_intake
		for each row execute procedure ref.trf_insert_intake_links_all_drug_components();

-- --------------------------------------------------------------
-- UPDATE
\unset ON_ERROR_STOP
drop function ref.trf_update_intake_must_link_all_drug_components() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_update_intake_must_link_all_drug_components()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_intake_count integer;
	_component_count integer;
	_pk_patient integer;
	_pk_brand integer;
BEGIN
	if NEW.fk_drug_component is not distinct from OLD.fk_drug_component then
		return NEW;
	end if;

	select fk_patient into _pk_patient
	from clin.encounter
	where pk = NEW.fk_encounter;

	-- check the OLD brand unless it is NULL
	if OLD.fk_drug_component is not NULL then
		-- get the brand we were linking to
		select fk_brand into _pk_brand
		from ref.lnk_substance2brand
		where fk_substance = OLD.fk_drug_component;

		-- How many substance intake links for this drug have we got ?
		select count(1) into _intake_count
		from clin.substance_intake
		where
			fk_drug_component in (
				select fk_substance from ref.lnk_substance2brand where fk_brand = _pk_brand
			)
				and
			fk_encounter in (
				select pk from clin.encounter where fk_patient = _pk_patient
			);

		-- unlinking completely would be fine but else:
		if _intake_count != 0 then
			-- How many components *are* there in the drug in question ?
			select count(1) into _component_count
			from ref.lnk_substance2brand
			where fk_brand = _pk_brand;

			-- substance intake link count and number of components must match
			if _component_count != _intake_count then
				raise exception ''[ref.trf_update_intake_must_link_all_drug_components] re-linking brand must unlink all components of old brand [%] (component [% -> %])'', _pk_brand, OLD.fk_drug_component, NEW.fk_drug_component;
			end if;
		end if;
	end if;

	-- check the NEW brand unless it is NULL
	if NEW.fk_drug_component is not NULL then
		-- get the brand we were linking to
		select fk_brand into _pk_brand
		from ref.lnk_substance2brand
		where fk_substance = NEW.fk_drug_component;

		-- How many substance intake links for this drug have we got ?
		select count(1) into _intake_count
		from clin.substance_intake
		where
			fk_drug_component in (
				select fk_substance from ref.lnk_substance2brand where fk_brand = _pk_brand
			)
				and
			fk_encounter in (
				select pk from clin.encounter where fk_patient = _pk_patient
			);

		-- unlinking completely would be fine but else:
		if _intake_count != 0 then
			-- How many components *are* there in the drug in question ?
			select count(1) into _component_count
			from ref.lnk_substance2brand
			where fk_brand = _pk_brand;

			-- substance intake link count and number of components must match
			if _component_count != _intake_count then
				raise exception ''[ref.trf_update_intake_must_link_all_drug_components] re-linking brand must link all components of new brand [%] (component [% -> %])'', _pk_brand, OLD.fk_drug_component, NEW.fk_drug_component;
			end if;
		end if;
	end if;

	return NEW;
END;';

comment on function ref.trf_update_intake_must_link_all_drug_components() is
	'If a patient is put on a different multi-component drug ALL components thereof must be updated.';

create constraint trigger tr_update_intake_must_link_all_drug_components
	after update on clin.substance_intake
		deferrable
		initially deferred
	for each row execute procedure ref.trf_update_intake_must_link_all_drug_components();

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop function ref.trf_update_intake_updates_all_drug_components() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_update_intake_updates_all_drug_components()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_pk_brand integer;
	_component_count integer;
	_pk_patient integer;
BEGIN
	-- does it at all relate to a drug (rather than substance) ?
	if NEW.fk_drug_component is null then
		return NEW;
	end if;

	-- which drug ?
	select fk_brand into _pk_brand
	from ref.lnk_substance2brand
	where pk = NEW.fk_drug_component;

	-- how many components therein ?
	select count(1) into _component_count
	from ref.lnk_substance2brand
	where fk_brand = _pk_brand;

	-- only one component ?
	if _component_count = 1 then
		return NEW;
	end if;

	-- which patient ?
	select fk_patient into _pk_patient
	from clin.encounter
	where pk = NEW.fk_encounter;

	-- update all substance instakes ...
	update clin.substance_intake set
		clin_when = NEW.clin_when,				-- started
		fk_encounter = NEW.fk_encounter,
		soap_cat = NEW.soap_cat,
		schedule = NEW.schedule,
		duration = NEW.duration,
		intake_is_approved_of = NEW.intake_is_approved_of,
		is_long_term = NEW.is_long_term,
		discontinued = NEW.discontinued
	where
		-- ... which belong to this drug ...
		fk_drug_component in (
			select pk from ref.lnk_substance2brand where fk_brand = _pk_brand
		)
			AND
		-- ... but are not THIS component ...
		fk_drug_component != NEW.fk_drug_component
			AND
		-- ... this patient ...
		fk_encounter in (
			select pk from clin.encounter where fk_patient = _pk_patient
		)
			AND
		-- ... are different in value (this will stop recursion as soon as all are equal)
		(
			clin_when is distinct from NEW.clin_when
				OR
			fk_encounter is distinct from NEW.fk_encounter
				OR
			soap_cat is distinct from NEW.soap_cat
				OR
			schedule is distinct from NEW.schedule
				OR
			duration is distinct from NEW.duration
				OR
			intake_is_approved_of is distinct from NEW.intake_is_approved_of
				OR
			is_long_term is distinct from NEW.is_long_term
				OR
			discontinued is distinct from NEW.discontinued
		)
	;

	return NEW;
END;';

comment on function ref.trf_update_intake_updates_all_drug_components() is
	'If a drug component substance intake is updated all sibling components must receive some values thereof.';

create constraint trigger tr_update_intake_updates_all_drug_components
	after update on clin.substance_intake
		deferrable
		initially deferred
	for each row execute procedure ref.trf_update_intake_updates_all_drug_components();

-- --------------------------------------------------------------
-- DELETE
\unset ON_ERROR_STOP
drop function ref.trf_delete_intake_document_deleted() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_delete_intake_document_deleted()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_msg text;
	_row record;
	_pk_episode integer;
BEGIN
	select
		* into _row
	from
		clin.v_pat_substance_intake_journal
	where
		src_pk = OLD.pk;

	_pk_episode := _row.pk_episode;

	-- create episode if needed
	if _pk_episode is null then
		select pk into _pk_episode
		from clin.episode
		where
			description = _(''Medication history'')
				and
			fk_encounter in (
				select pk from clin.encounter where fk_patient = _row.pk_patient
			);
		if not found then
			insert into clin.episode (
				description,
				is_open,
				fk_encounter
			) values (
				_(''Medication history''),
				FALSE,
				OLD.fk_encounter
			) returning pk into _pk_episode;
		end if;
	end if;

	insert into clin.clin_narrative (
		fk_encounter,
		fk_episode,
		soap_cat,
		narrative
	) values (
		_row.pk_encounter,
		_pk_episode,
		NULL,
		_(''Deletion of'') || '' '' || _row.narrative
	);

	return OLD;
END;';

comment on function ref.trf_delete_intake_document_deleted() is
	'Document the deletion of a substance intake.';

create trigger tr_delete_intake_document_deleted
	before delete on clin.substance_intake
	for each row execute procedure ref.trf_delete_intake_document_deleted();

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop function ref.trf_delete_intake_turns_other_components_into_substances() cascade;
\set ON_ERROR_STOP 1

create or replace function ref.trf_delete_intake_turns_other_components_into_substances()
	returns trigger
	language 'plpgsql'
	as '
DECLARE
	_pk_brand integer;
	_component_count integer;
	_pk_patient integer;
BEGIN
	-- did it at all relate to a drug (rather than substance) ?
	if OLD.fk_drug_component is NULL then
		return OLD;
	end if;

	-- which drug ?
	select fk_brand into _pk_brand
	from ref.lnk_substance2brand
	where pk = OLD.fk_drug_component;

	-- how many components therein ?
	select count(1) into _component_count
	from ref.lnk_substance2brand
	where fk_brand = _pk_brand;

	-- only one component ?
	if _component_count = 1 then
		return OLD;
	end if;

	-- which patient ?
	select fk_patient into _pk_patient
	from clin.encounter
	where pk = OLD.fk_encounter;

	-- relink all other intakes into substances
	update clin.substance_intake set
		fk_drug_component = null,
		fk_substance = (
			select fk_substance from ref.lnk_substance2brand where pk = fk_drug_component
		),
		preparation = (
			select preparation from ref.branded_drug where pk = (
				select fk_brand from ref.lnk_substance2brand where pk = fk_drug_component
			)
		)
	where
		fk_drug_component is not null
			and
		fk_drug_component in (
			select pk from ref.lnk_substance2brand where fk_brand = _pk_brand
		)
			and
		fk_encounter in (
			select pk from clin.encounter where fk_patient = _pk_patient
		)
	;

	return OLD;
END;';

comment on function ref.trf_delete_intake_turns_other_components_into_substances() is
	'If a patient is stopped from a multi-component drug intake other components thereof must be turned into non-brand substance intakes.';

create trigger tr_delete_intake_turns_other_components_into_substances
	after delete on clin.substance_intake
	for each row execute procedure ref.trf_delete_intake_turns_other_components_into_substances();

-- --------------------------------------------------------------
select gm.log_script_insertion('v15-clin-substance_intake-dynamic.sql', 'Revision: 1.1');

-- ==============================================================
