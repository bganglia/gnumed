-- Projekt GnuMed
-- Impfkalender der Hersteller von Influenza-Impfstoff

-- Quellen: Beipackzettel

-- author: Karsten Hilbert <Karsten.Hilbert@gmx.net>
-- license: GPL
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/country.specific/de/Impfplan-Influenza.sql,v $
-- $Revision: 1.1 $
-- =============================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- Impfplan erstellen
insert into vacc_regime
	(fk_recommended_by, fk_indication, description)
values (
	-1,
	(select id from vacc_indication where description='influenza'),
	'Influenza (>6 Monate, Hersteller)'
);

-- Impfzeitpunkte definieren
insert into vacc_def
	(fk_regime, seq_no, min_age_due, is_booster, min_interval, comment)
values (
	currval('vacc_regime_id_seq'),
	1,
	'6 months'::interval,
	false,
	'4 weeks'::interval,
	'nie zuvor geimpfte Kinder in 4 Wo boostern'
);

-- =============================================
-- do simple revision tracking
delete from gm_schema_revision where filename = '$RCSfile: Impfplan-Influenza.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: Impfplan-Influenza.sql,v $', '$Revision: 1.1 $');

-- =============================================
-- $Log: Impfplan-Influenza.sql,v $
-- Revision 1.1  2003-11-30 12:37:39  ncq
-- - InfectoVac Flu 2003/4
--
-- Revision 1.4  2003/11/28 08:15:57  ncq
-- - PG 7.1/pyPgSQL/mxDateTime returns 0 for interval=1 month,
--   it works with interval=4 weeks, though, so use that
--
-- Revision 1.3  2003/11/26 23:54:51  ncq
-- - lnk_vaccdef2reg does not exist anymore
--
-- Revision 1.2  2003/11/26 00:12:19  ncq
-- - fix fk_recommended_by value
--
-- Revision 1.1  2003/11/26 00:10:45  ncq
-- - Prevenar
--
