-- Project: GnuMed
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/country.specific/au/gmDemographics.au.sql,v $
-- $Revision: 1.7 $
-- license: GPL
-- authors: Ian Haywood, Horst Herb, Karsten Hilbert, Richard Terry

-- demographics tables specific f�r Australia

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

reset client_encoding;
-- ===================================================================
create table org_AU (
	id serial primary key,
	id_org integer unique not null references org(id),
	ACN text
) inherits (audit_fields);

select add_table_for_audit('org_au');

comment on table org_AU is
	'organisation information specific to Australia';
comment on column org_AU.id_org is
	'the organisation this row belongs to';
comment on column org_AU.ACN is
	'Australian Company Number';


-- ===================================================================

-- seeding for occupations list
-- this is highly nation-specific!

insert into occupation (name) values ('doctor');
insert into occupation (name) values ('general practitioner');
insert into occupation (name) values ('hospital resident');
insert into occupation (name) values ('hospital registrar');
insert into occupation (name) values ('physician');
insert into occupation (name) values ('cardiologist');
insert into occupation (name) values ('gastroenterologist');
insert into occupation (name) values ('respiratory physician');
insert into occupation (name) values ('neurologist');
insert into occupation (name) values ('dermatologist');
insert into occupation (name) values ('rheumatologist');
insert into occupation (name) values ('geneticist');
insert into occupation (name) values ('pathologist');
insert into occupation (name) values ('obstetrician/gynaecologist');
insert into occupation (name) values ('paediatrician');
insert into occupation (name) values ('psychiatrist');
insert into occupation (name) values ('anaesthetist');
insert into occupation (name) values ('radiologist');
insert into occupation (name) values ('surgeon');
insert into occupation (name) values ('general surgeon');
insert into occupation (name) values ('plastic surgeon');
insert into occupation (name) values ('orthopaedic surgeon');
insert into occupation (name) values ('vascular surgeon');
insert into occupation (name) values ('paediatric surgeon');
insert into occupation (name) values ('neurosurgeon');
insert into occupation (name) values ('cardio-thoracic surgeon');
insert into occupation (name) values ('ENT surgeon');
insert into occupation (name) values ('ophthalmologist');


insert into occupation (name) values ('nurse');
insert into occupation (name) values ('social worker');
insert into occupation (name) values ('physiotherapist');
insert into occupation (name) values ('speech pathologist');
insert into occupation (name) values ('psychologist');
insert into occupation (name) values ('occupational therapist');
insert into occupation (name) values ('dietician');
insert into occupation (name) values ('radiographer');

insert into occupation (name) values ('student');
insert into occupation (name) values ('teacher');
insert into occupation (name) values ('lecturer');
insert into occupation (name) values ('mechanic');
insert into occupation (name) values ('cleaner');
insert into occupation (name) values ('engineer');
insert into occupation (name) values ('hairdresser');
insert into occupation (name) values ('unemployed');
insert into occupation (name) values ('scientist');
insert into occupation (name) values ('retired');
insert into occupation (name) values ('dentist');
insert into occupation (name) values ('police officer');
insert into occupation (name) values ('soldier');
insert into occupation (name) values ('security guard');
insert into occupation (name) values ('farmer');
insert into occupation (name) values ('unknown');

-- ===================================================================
-- do simple schema revision tracking
delete from gm_schema_revision where filename='$RCSfile: gmDemographics.au.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmDemographics.au.sql,v $', '$Revision: 1.7 $');

-- ===================================================================
-- $Log: gmDemographics.au.sql,v $
-- Revision 1.7  2004-03-02 10:22:41  ihaywood
-- support for martial status and occupations
-- .conf files now use host autoprobing
--
-- Revision 1.6  2004/01/05 00:59:14  ncq
-- - remove ourselves from schema revision table
--
-- Revision 1.5  2003/12/29 15:49:46  uid66147
-- - reset client_encoding
--
-- Revision 1.4  2003/10/01 16:12:01  ncq
-- - AU -> au
--
-- Revision 1.3  2003/10/01 15:45:20  ncq
-- - use add_table_for_audit() instead of inheriting from audit_mark
--
-- Revision 1.2  2003/08/17 00:27:33  ncq
-- - log_ tables removed, now auto-created
--
-- Revision 1.1  2003/08/05 09:24:51  ncq
-- - first checkin
--
