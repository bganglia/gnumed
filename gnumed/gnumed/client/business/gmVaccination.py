"""GNUmed vaccination related business objects.
"""
#============================================================
__author__ = "K.Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL"

import sys
import logging
import io


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmBusinessDBObject
from Gnumed.pycommon import gmPG2
from Gnumed.pycommon import gmI18N
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDateTime
if __name__ == '__main__':
	gmI18N.activate_locale()
	gmI18N.install_domain()
from Gnumed.business import gmMedication


_log = logging.getLogger('gm.vacc')

#============================================================
URL_vaccination_plan = u'http://www.rki.de/DE/Content/Infekt/EpidBull/Archiv/2017/Ausgaben/34_17.pdf?__blob=publicationFile'

#============================================================
_SQL_create_substance4vaccine = u"""-- in case <%(substance_tag)s> already exists: add ATC
UPDATE ref.substance SET atc = '%(atc)s' WHERE lower(description) = lower('%(desc)s') AND atc IS NULL;

INSERT INTO ref.substance (description, atc)
	SELECT
		'%(desc)s',
		'%(atc)s'
	WHERE NOT EXISTS (
		SELECT 1 FROM ref.substance WHERE
			atc = '%(atc)s'
				AND
			description = '%(desc)s'
	);

-- generic English
SELECT i18n.upd_tx('en', '%(orig)s', '%(trans)s');
-- user language, if any, fails if not set
SELECT i18n.upd_tx('%(orig)s', '%(trans)s');"""

_SQL_map_indication2substance = u"""-- old-style "%(v21_ind)s" => "%(desc)s"
INSERT INTO staging.lnk_vacc_ind2subst_dose (fk_indication, fk_dose, is_live)
	SELECT
		(SELECT id FROM ref.vacc_indication WHERE description = '%(v21_ind)s'),
		(SELECT pk_dose FROM ref.v_substance_doses WHERE
			amount = 1
				AND
			unit = 'dose'
				AND
			dose_unit = 'shot'
				AND
			substance = '%(desc)s'
		),
		%(is_live)s
	WHERE EXISTS (
		SELECT 1 FROM ref.vacc_indication WHERE description = '%(v21_ind)s'
	);"""

_SQL_create_vacc_product = u"""-- --------------------------------------------------------------
-- in case <%(prod_name)s> exists: add ATC
UPDATE ref.drug_product SET atc_code = '%(atc_prod)s' WHERE
	atc_code IS NULL
		AND
	description = '%(prod_name)s'
		AND
	preparation = '%(prep)s'
		AND
	is_fake IS TRUE;

INSERT INTO ref.drug_product (description, preparation, is_fake, atc_code)
	SELECT
		'%(prod_name)s',
		'%(prep)s',
		TRUE,
		'%(atc_prod)s'
	WHERE NOT EXISTS (
		SELECT 1 FROM ref.drug_product WHERE
			description = '%(prod_name)s'
				AND
			preparation = '%(prep)s'
				AND
			is_fake = TRUE
				AND
			atc_code = '%(atc_prod)s'
	);"""

_SQL_create_vaccine = u"""-- add vaccine if necessary
INSERT INTO ref.vaccine (is_live, fk_drug_product)
	SELECT
		%(is_live)s,
		(SELECT pk FROM ref.drug_product WHERE
			description = '%(prod_name)s'
				AND
			preparation = '%(prep)s'
				AND
			is_fake = TRUE
				AND
			atc_code = '%(atc_prod)s'
		)
	WHERE NOT EXISTS (
		SELECT 1 FROM ref.vaccine WHERE
			is_live IS %(is_live)s
				AND
			fk_drug_product = (
				SELECT pk FROM ref.drug_product WHERE
					description = '%(prod_name)s'
						AND
					preparation = '%(prep)s'
						AND
					is_fake = TRUE
						AND
					atc_code = '%(atc_prod)s'
			)
	);"""

_SQL_create_vacc_subst_dose = u"""-- create dose, assumes substance exists
INSERT INTO ref.dose (fk_substance, amount, unit, dose_unit)
	SELECT
		(SELECT pk FROM ref.substance WHERE atc = '%(atc_subst)s' AND description = '%(name_subst)s' LIMIT 1),
		1,
		'dose',
		'shot'
	WHERE NOT EXISTS (
		SELECT 1 FROM ref.dose WHERE
			fk_substance = (SELECT pk FROM ref.substance WHERE atc = '%(atc_subst)s' AND description = '%(name_subst)s' LIMIT 1)
				AND
			amount = 1
				AND
			unit = 'dose'
				AND
			dose_unit IS NOT DISTINCT FROM 'shot'
	);"""

_SQL_link_dose2vacc_prod = u"""-- link dose to product
INSERT INTO ref.lnk_dose2drug (fk_dose, fk_drug_product)
	SELECT
		(SELECT pk from ref.dose WHERE
			fk_substance = (SELECT pk FROM ref.substance WHERE atc = '%(atc_subst)s' AND description = '%(name_subst)s' LIMIT 1)
				AND
			amount = 1
				AND
			unit = 'dose'
				AND
			dose_unit IS NOT DISTINCT FROM 'shot'
		),
		(SELECT pk FROM ref.drug_product WHERE
			description = '%(prod_name)s'
				AND
			preparation = '%(prep)s'
				AND
			is_fake = TRUE
				AND
			atc_code = '%(atc_prod)s'
		)
	WHERE NOT EXISTS (
		SELECT 1 FROM ref.lnk_dose2drug WHERE
			fk_dose = (
				SELECT PK from ref.dose WHERE
					fk_substance = (SELECT pk FROM ref.substance WHERE atc = '%(atc_subst)s' AND description = '%(name_subst)s' LIMIT 1)
						AND
					amount = 1
						AND
					unit = 'dose'
						AND
					dose_unit IS NOT DISTINCT FROM 'shot'
			)
				AND
			fk_drug_product = (
				SELECT pk FROM ref.drug_product WHERE
					description = '%(prod_name)s'
						AND
					preparation = '%(prep)s'
						AND
					is_fake = TRUE
						AND
					atc_code = '%(atc_prod)s'
			)
	);"""

_SQL_create_indications_mapping_table = u"""-- set up helper table for conversion of vaccines from using
-- linked indications to using linked substances,
-- to be dropped after converting vaccines
DROP TABLE IF EXISTS staging.lnk_vacc_ind2subst_dose CASCADE;

CREATE UNLOGGED TABLE staging.lnk_vacc_ind2subst_dose (
	fk_indication INTEGER
		NOT NULL
		REFERENCES ref.vacc_indication(id)
			ON UPDATE CASCADE
			ON DELETE RESTRICT,
	fk_dose INTEGER
		NOT NULL
		REFERENCES ref.dose(pk)
			ON UPDATE CASCADE
			ON DELETE RESTRICT,
	is_live
		BOOLEAN
		NOT NULL
		DEFAULT false,
	UNIQUE(fk_indication, fk_dose),
	UNIQUE(fk_indication, is_live)
);


DROP VIEW IF EXISTS staging.v_lnk_vacc_ind2subst_dose CASCADE;

CREATE VIEW staging.v_lnk_vacc_ind2subst_dose AS
SELECT
	s_lvi2sd.is_live
		as mapping_is_for_live_vaccines,
	r_vi.id
		as pk_indication,
	r_vi.description
		as indication,
	r_vi.atcs_single_indication,
	r_vi.atcs_combi_indication,
	r_d.pk
		as pk_dose,
	r_d.amount,
	r_d.unit,
	r_d.dose_unit,
	r_s.pk
		as pk_substance,
	r_s.description
		as substance,
	r_s.atc
		as atc_substance
FROM
	staging.lnk_vacc_ind2subst_dose s_lvi2sd
		inner join ref.vacc_indication r_vi on (r_vi.id = s_lvi2sd.fk_indication)
		inner join ref.dose r_d on (r_d.pk = s_lvi2sd.fk_dose)
			inner join ref.substance r_s on (r_s.pk = r_d.fk_substance)
;"""

_SQL_create_generic_vaccines_script = u"""-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- THIS IS A GENERATED FILE. DO NOT EDIT.
--
-- ==============================================================
\set ON_ERROR_STOP 1
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
-- indications mapping helper table
-- --------------------------------------------------------------
%s

-- --------------------------------------------------------------
-- generic vaccine "substances" (= indications)
-- --------------------------------------------------------------
%s

-- --------------------------------------------------------------
-- generic vaccines
-- --------------------------------------------------------------
-- new-style vaccines are not linked to indications, so drop
-- trigger asserting that condition,
DROP FUNCTION IF EXISTS clin.trf_sanity_check_vaccine_has_indications() CASCADE;


-- need to disable trigger before running
ALTER TABLE ref.drug_product
	DISABLE TRIGGER tr_assert_product_has_components
;

%s

-- want to re-enable trigger as now all inserted
-- vaccines satisfy the conditions
ALTER TABLE ref.drug_product
	ENABLE TRIGGER tr_assert_product_has_components
;

-- --------------------------------------------------------------
-- indications mapping data
-- --------------------------------------------------------------
-- map old style
--		(clin|ref).vacc_indication.description
-- to new style
--		ref.v_substance_doses.substance

%s

-- --------------------------------------------------------------
select gm.log_script_insertion('v%s-ref-create_generic_vaccines.sql', '%s');
"""

#============================================================
def write_generic_vaccine_sql(version, include_indications_mapping=False, filename=None):
	if filename is None:
		filename = gmTools.get_unique_filename(suffix = u'.sql')
	_log.debug('writing SQL for creating generic vaccines to: %s', filename)
	sql_file = io.open(filename, mode = 'wt', encoding = 'utf8')
	sql_file.write(create_generic_vaccine_sql (
		version,
		include_indications_mapping = include_indications_mapping
	))
	sql_file.close()
	return filename

#------------------------------------------------------------
def create_generic_vaccine_sql(version, include_indications_mapping=False):

	_log.debug('including indications mapping table with generic vaccines creation SQL: %s', include_indications_mapping)

	from Gnumed.business import gmVaccDefs

	sql_create_substances = []
	sql_populate_ind2subst_map = []
	sql_create_vaccines = []

	for substance_tag in gmVaccDefs._VACCINE_SUBSTANCES:
		subst = gmVaccDefs._VACCINE_SUBSTANCES[substance_tag]
		args = {
			'substance_tag': substance_tag,
			'atc': subst['atc4target'],
			'desc': subst['name'],
			'orig': subst['target'].split(u'::')[0],
			'trans': subst['target'].split(u'::')[-1]
		}
		sql_create_substances.append(_SQL_create_substance4vaccine % args)
		try:
			for v21_ind in subst['v21_indications']:
				args['v21_ind'] = v21_ind
				args['is_live'] = u'false'
				sql_populate_ind2subst_map.append(_SQL_map_indication2substance % args)
		except KeyError:
			pass
		try:
			for v21_ind in subst['v21_indications_live']:
				args['v21_ind'] = v21_ind
				args['is_live'] = u'true'
				sql_populate_ind2subst_map.append(_SQL_map_indication2substance % args)
		except KeyError:
			pass
		args = {}

	for key in gmVaccDefs._GENERIC_VACCINES:
		vaccine_def = gmVaccDefs._GENERIC_VACCINES[key]
		# create product
		args = {
			'atc_prod': vaccine_def['atc'],
			'prod_name': vaccine_def['name'],
			# generic vaccines always have the English preparation
			'prep': u'vaccine',
			'is_live': vaccine_def['live']
		}
		sql_create_vaccines.append(_SQL_create_vacc_product % args)
		# create doses
		for ingredient_tag in vaccine_def['ingredients']:
			vacc_subst_def = gmVaccDefs._VACCINE_SUBSTANCES[ingredient_tag]
			args['atc_subst'] = vacc_subst_def['atc4target']
			args['name_subst'] = vacc_subst_def['name']
			# substance already created, only need to create dose
			sql_create_vaccines.append(_SQL_create_vacc_subst_dose % args)
			# link dose to product
			sql_create_vaccines.append(_SQL_link_dose2vacc_prod % args)
			# the following does not work because there are mixed vaccines
			# any live ingredients included ?
#			if vacc_subst_def.has_key('v21_indications_live'):
#				if vaccine_def['live'] is False:
#					print vaccine_def
#					raise Exception('vaccine def says "NOT live" but ingredients DO map to <v21_indications_LIVE>')
#			if vacc_subst_def.has_key('v21_indications'):
#				if vaccine_def['live'] is True:
#					print vaccine_def
#					raise Exception('vaccine def says "live" but ingredients do NOT map to v21_indications_LIVE')

		# create vaccine
		sql_create_vaccines.append(_SQL_create_vaccine % args)

	# join
	sql = _SQL_create_generic_vaccines_script % (
		gmTools.bool2subst (
			include_indications_mapping,
			_SQL_create_indications_mapping_table,
			u'-- indications mapping table not included'
		),
		u'\n\n'.join(sql_create_substances),
		u'\n\n'.join(sql_create_vaccines),
		gmTools.bool2subst (
			include_indications_mapping,
			u'\n\n'.join(sql_populate_ind2subst_map),
			u'-- indications mapping table not populated'
		),
		version,
		version
	)
	return sql

#============================================================
# vaccine related code
#------------------------------------------------------------
_SQL_get_vaccine_fields = u"""SELECT * FROM ref.v_vaccines WHERE %s"""

class cVaccine(gmBusinessDBObject.cBusinessDBObject):
	"""Represents one vaccine."""

	_cmd_fetch_payload = _SQL_get_vaccine_fields % u"pk_vaccine = %s"

	_cmds_store_payload = [
		u"""UPDATE ref.vaccine SET
				--id_route = %(pk_route)s,
				is_live = %(is_live)s,
				min_age = %(min_age)s,
				max_age = %(max_age)s,
				comment = gm.nullify_empty_string(%(comment)s),
				fk_drug_product = %(pk_drug_product)s
			WHERE
				pk = %(pk_vaccine)s
					AND
				xmin = %(xmin_vaccine)s
			RETURNING
				xmin as xmin_vaccine
		"""
	]

	_updatable_fields = [
		#u'pk_route',
		u'is_live',
		u'min_age',
		u'max_age',
		u'comment',
		u'pk_drug_product'
	]

	#--------------------------------------------------------
	def format(self, *args, **kwargs):
		lines = []
		lines.append(_(u'%s with %s %s     #%s') % (
			gmTools.bool2subst(self._payload[self._idx['is_live']], _(u'Live vaccine'), _(u'Inactive vaccine'), u'<liveness error in DB>'),
			len(self._payload[self._idx['indications']]),
			gmTools.bool2subst(len(self._payload[self._idx['indications']]) == 1, _('indication'), _('indications'), _('indication(s)')),
			self._payload[self._idx['pk_vaccine']]
		))
		lines.append(_(u' Product: "%s"     #%s') % (
			self._payload[self._idx['vaccine']],
			self._payload[self._idx['pk_drug_product']]
		))
		lines.append(_(u'  %s%s%s%s') % (
			self._payload[self._idx['l10n_preparation']],
			gmTools.coalesce(gmTools.bool2subst(self._payload[self._idx['is_fake_vaccine']], _(u'fake product'), None, None), u'', u', %s'),
			gmTools.coalesce(self._payload[self._idx['atc_code']], u'', u' [ATC:%s]'),
			gmTools.coalesce(self._payload[self._idx['external_code']], u'', u' [%s:%%s]' % self._payload[self._idx['external_code_type']])
		))
		#lines.append(_(u' %sage %s - %s') % (
		#	gmTools.coalesce(self._payload[self._idx['route_description']], u'', u'%s, '),		#route_abbreviation
		lines.append(_(u' Age %s - %s') % (
			gmTools.coalesce(self._payload[self._idx['min_age']], u'?'),
			gmTools.coalesce(self._payload[self._idx['max_age']], u'?')
		))
		if self._payload[self._idx['comment']] is not None:
			lines.extend([ u' %s' % l for l in self._payload[self._idx['comment']].split(u'\n')] )
		lines.append(_(u' Indications'))
		lines.extend( [ u'  %s [ATC:%s]' % (i['l10n_indication'], i['atc_indication']) for i in self._payload[self._idx['indications']] ])

		return lines

	#--------------------------------------------------------
	# properties
	#--------------------------------------------------------
	def _get_product(self):
		return gmMedication.cDrugProduct(aPK_obj = self._payload[self._idx['pk_drug_product']])

	product = property(_get_product, lambda x:x)

	#--------------------------------------------------------
	def _get_is_in_use(self):
		cmd = u'SELECT EXISTS(SELECT 1 FROM clin.vaccination WHERE fk_vaccine = %(pk)s)'
		args = {'pk': self._payload[self._idx['pk_vaccine']]}
		rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = False)
		return rows[0][0]

	is_in_use = property(_get_is_in_use, lambda x:x)

#------------------------------------------------------------
def create_vaccine(pk_drug_product=None, product_name=None, indications=None):

	conn = gmPG2.get_connection(readonly = False)

	if pk_drug_product is None:
		#prep = _('vaccine')
		prep = u'vaccine'
		_log.debug('creating vaccine drug product [%s %s]', product_name, prep)
		vacc_prod = gmMedication.create_drug_product (
			product_name = product_name,
			preparation = prep,
			return_existing = True,
			# indications are ref.dose rows
			doses = indications,
			link_obj = conn
		)
		#conn.commit()
		vacc_prod['atc'] = u'J07'
		vacc_prod.save(conn = conn)
		pk_drug_product = vacc_prod['pk_drug_product']

	cmd = u'INSERT INTO ref.vaccine (fk_drug_product) values (%(pk_drug_product)s) RETURNING pk'
	queries = [{'cmd': cmd, 'args': {'pk_drug_product': pk_drug_product}}]
	rows, idx = gmPG2.run_rw_queries(link_obj = conn, queries = queries, get_col_idx = False, return_data = True, end_tx = True)
	conn.close()
	return cVaccine(aPK_obj = rows[0]['pk'])

#------------------------------------------------------------
def delete_vaccine(vaccine=None):

	cmd = u'DELETE FROM ref.vaccine WHERE pk = %(pk)s'
	args = {'pk': vaccine}

	try:
		gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])
	except gmPG2.dbapi.IntegrityError:
		_log.exception('cannot delete vaccine [%s]', vaccine)
		return False

	return True

#------------------------------------------------------------
def get_vaccines(order_by=None):

	if order_by is None:
		cmd = _SQL_get_vaccine_fields % u'TRUE'
	else:
		cmd = _SQL_get_vaccine_fields % (u'TRUE\nORDER BY %s' % order_by)

	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd}], get_col_idx = True)

	return [ cVaccine(row = {'data': r, 'idx': idx, 'pk_field': 'pk_vaccine'}) for r in rows ]

#============================================================
# vaccination related classes
#============================================================
_SQL_get_vaccination_fields = u"""SELECT * FROM clin.v_vaccinations WHERE %s"""

class cVaccination(gmBusinessDBObject.cBusinessDBObject):

	_cmd_fetch_payload = _SQL_get_vaccination_fields % u"pk_vaccination = %s"

	_cmds_store_payload = [
		u"""UPDATE clin.vaccination SET
				soap_cat = %(soap_cat)s,
				clin_when = %(date_given)s,
				site = gm.nullify_empty_string(%(site)s),
				batch_no = gm.nullify_empty_string(%(batch_no)s),
				reaction = gm.nullify_empty_string(%(reaction)s),
				narrative = gm.nullify_empty_string(%(comment)s),
				fk_vaccine = %(pk_vaccine)s,
				fk_provider = %(pk_provider)s,
				fk_encounter = %(pk_encounter)s,
				fk_episode = %(pk_episode)s
			WHERE
				pk = %(pk_vaccination)s
					AND
				xmin = %(xmin_vaccination)s
			RETURNING
				xmin as xmin_vaccination
		"""
	]

	_updatable_fields = [
		u'soap_cat',
		u'date_given',
		u'site',
		u'batch_no',
		u'reaction',
		u'comment',
		u'pk_vaccine',
		u'pk_provider',
		u'pk_encounter',
		u'pk_episode'
	]

	#--------------------------------------------------------
	def format_maximum_information(self, patient=None):
		return self.format (
			with_indications = True,
			with_comment = True,
			with_reaction = True,
			date_format = '%Y %b %d'
		)

	#--------------------------------------------------------
	def format(self, with_indications=False, with_comment=False, with_reaction=False, date_format='%Y-%m-%d'):

		lines = []

		lines.append (u' %s: %s [%s]%s' % (
			self._payload[self._idx['date_given']].strftime(date_format).decode(gmI18N.get_encoding()),
			self._payload[self._idx['vaccine']],
			self._payload[self._idx['batch_no']],
			gmTools.coalesce(self._payload[self._idx['site']], u'', u' (%s)')
		))

		if with_comment:
			if self._payload[self._idx['comment']] is not None:
				lines.append(u'   %s' % self._payload[self._idx['comment']])

		if with_reaction:
			if self._payload[self._idx['reaction']] is not None:
				lines.append(u'   %s' % self._payload[self._idx['reaction']])

		if with_indications:
			lines.append(u'   %s' % u' / '.join([ i['l10n_indication'] for i in self._payload[self._idx['indications']] ]))

		return lines

	#--------------------------------------------------------
	def _get_vaccine(self):
		return cVaccine(aPK_obj = self._payload[self._idx['pk_vaccine']])

	vaccine = property(_get_vaccine, lambda x:x)

#------------------------------------------------------------
def get_vaccinations():
	cmd = _SQL_get_vaccination_fields % 'True'
	args = {}
	rows, idx = gmPG2.run_ro_queries(queries = [{'cmd': cmd}], get_col_idx = True)
	return [ cVaccination(row = {'data': r, 'idx': idx, 'pk_field': 'pk_vaccine'}) for r in rows ]

#------------------------------------------------------------
def create_vaccination(encounter=None, episode=None, vaccine=None, batch_no=None):

	cmd = u"""
		INSERT INTO clin.vaccination (
			fk_encounter,
			fk_episode,
			fk_vaccine,
			batch_no
		) VALUES (
			%(enc)s,
			%(epi)s,
			%(vacc)s,
			%(batch)s
		) RETURNING pk;
	"""
	args = {
		u'enc': encounter,
		u'epi': episode,
		u'vacc': vaccine,
		u'batch': batch_no
	}

	rows, idx = gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}], get_col_idx = False, return_data = True)

	return cVaccination(aPK_obj = rows[0][0])

#------------------------------------------------------------
def delete_vaccination(vaccination=None):
	cmd = u"""DELETE FROM clin.vaccination WHERE pk = %(pk)s"""
	args = {'pk': vaccination}

	gmPG2.run_rw_queries(queries = [{'cmd': cmd, 'args': args}])

#------------------------------------------------------------

def format_latest_vaccinations(output_format=u'latex', emr=None):

	_log.debug(u'formatting latest vaccinations into [%s]', output_format)

	vaccs = emr.get_latest_vaccinations()

	if output_format == u'latex':
		return __format_latest_vaccinations_latex(vaccinations = vaccs)

	msg = _('unknown vaccinations output format [%s]') % output_format
	_log.error(msg)
	return msg

#------------------------------------------------------------

def __format_latest_vaccinations_latex(vaccinations=None):

	if len(vaccinations) == 0:
		return u'\\noindent %s' % _('No vaccinations recorded.')

	tex =  u'\\noindent %s {\\tiny (%s)\\par}\n' % (_('Latest vaccinations'), _('per target condition'))
	tex += u'\n'
	tex += u'\\noindent \\begin{tabular}{|l|l|l|l|l|l|}\n'
	tex += u'\\hline\n'
	tex += u'%s & %s & {\\footnotesize %s} & {\\footnotesize %s} & {\\footnotesize %s\\footnotemark} & {\\footnotesize %s\\footnotemark}\\\\\n' % (
		_('Target'),
		_('Last given'),
		_('Vaccine'),
		_('Lot \#'),
		_('SoaP'),
		gmTools.u_sum
	)
	tex += u'\\hline\n'
	tex += u'\n'
	tex += u'\\hline\n'
	tex += u'%s'			# this is where the actual vaccination rows end up
	tex += u'\n'
	tex += u'\\end{tabular}\n'
	tex += u'\n'
	tex += u'\\addtocounter{footnote}{-1}\n'
	tex += u'\\footnotetext{%s}\n' % _('SoaP -- "S"ubjective: vaccination was remembered by patient. "P"lan: vaccination was administered in the practice or copied from trustworthy records.')
	tex += u'\\addtocounter{footnote}{1}\n'
	tex += u'\\footnotetext{%s -- %s}\n' % (gmTools.u_sum, _('Total number of vaccinations recorded for the corresponding target condition.'))
	tex += u'\n'

	row_template = u'%s & %s & {\\scriptsize %s} & {\\scriptsize %s} & {\\scriptsize %s} & {\\scriptsize %s}\\\\\n'
	lines = u''
	targets = sorted(vaccinations.keys())
	for target in targets:
		target_count, vacc = vaccinations[target]
		lines += row_template % (
			target,
			gmDateTime.pydt_strftime(vacc['date_given'], '%Y %b %d'),
			vacc['vaccine'],
			gmTools.tex_escape_string(vacc['batch_no'].strip()),
			vacc['soap_cat'].upper(),
			target_count
		)
		if vacc['site'] is not None:
			lines += u' & \\multicolumn{5}{l|}{\\scriptsize %s: %s\\par}\\\\\n' % (_('Injection site'), vacc['site'].strip())
		if vacc['reaction'] is not None:
			lines += u' & \\multicolumn{5}{l|}{\\scriptsize %s: %s\\par}\\\\\n' % (_('Reaction'), vacc['reaction'].strip())
		if vacc['comment'] is not None:
			lines += u' & \\multicolumn{5}{l|}{\\scriptsize %s: %s\\par}\\\\\n' % (_('Comment'), vacc['comment'].strip())
		lines += u'\\hline\n'

	return tex % lines

#============================================================
# main - unit testing
#------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != u'test':
		sys.exit()

#	from Gnumed.pycommon import gmPG
	#--------------------------------------------------------
	def test_vacc():
		vacc = cVaccination(aPK_obj=1)
		print vacc
		fields = vacc.get_fields()
		for field in fields:
			print field, ':', vacc[field]
		print "updatable:", vacc.get_updatable_fields()

	#--------------------------------------------------------
	def test_due_vacc():
		# Test for a due vaccination
		pk_args = {
			'pat_id': 12,
			'indication': 'meningococcus C',
			'seq_no': 1
		}
		missing_vacc = cMissingVaccination(aPK_obj=pk_args)
		fields = missing_vacc.get_fields()
		print "\nDue vaccination:"
		print missing_vacc
		for field in fields:
			print field, ':', missing_vacc[field]
		# Test for an overdue vaccination
		pk_args = {
			'pat_id': 12,
			'indication': 'haemophilus influenzae b',
			'seq_no': 2
		}
		missing_vacc = cMissingVaccination(aPK_obj=pk_args)
		fields = missing_vacc.get_fields()
		print "\nOverdue vaccination (?):"
		print missing_vacc
		for field in fields:
			print field, ':', missing_vacc[field]

	#--------------------------------------------------------
	def test_due_booster():
		pk_args = {
			'pat_id': 12,
			'indication': 'tetanus'
		}
		missing_booster = cMissingBooster(aPK_obj=pk_args)
		fields = missing_booster.get_fields()
		print "\nDue booster:"
		print missing_booster
		for field in fields:
			print field, ':', missing_booster[field]

	#--------------------------------------------------------
	def test_scheduled_vacc():
		scheduled_vacc = cScheduledVaccination(aPK_obj=20)
		print "\nScheduled vaccination:"
		print scheduled_vacc
		fields = scheduled_vacc.get_fields()
		for field in fields:
			print field, ':', scheduled_vacc[field]
		print "updatable:", scheduled_vacc.get_updatable_fields()

	#--------------------------------------------------------
	def test_vaccination_course():
		vaccination_course = cVaccinationCourse(aPK_obj=7)
		print "\nVaccination course:"		
		print vaccination_course
		fields = vaccination_course.get_fields()
		for field in fields:
			print field, ':', vaccination_course[field]
		print "updatable:", vaccination_course.get_updatable_fields()

	#--------------------------------------------------------
	def test_put_patient_on_schedule():
		result, msg = put_patient_on_schedule(patient_id=12, course_id=1)
		print '\nPutting patient id 12 on schedule id 1... %s (%s)' % (result, msg)

	#--------------------------------------------------------
	def test_get_vaccines():
		for vaccine in get_vaccines():
			print u'--------------------------------'
			#print u'%s' % vaccine
			print u'\n'.join(vaccine.format())

	#--------------------------------------------------------
	def test_get_vaccinations():
		for v in get_vaccinations():
			print v

	#--------------------------------------------------------
	def test_create_generic_vaccine_sql():
		print create_generic_vaccine_sql(u'22.0')

	#--------------------------------------------------------
	def test_write_generic_vaccine_sql(version, filename):
		print write_generic_vaccine_sql (
			version,
			include_indications_mapping = True,
			filename = filename
		)

	#--------------------------------------------------------
	#test_vaccination_course()
	#test_put_patient_on_schedule()
	#test_scheduled_vacc()
	#test_vacc()
	#test_due_vacc()
	#test_due_booster()

	#test_get_vaccines()
	test_get_vaccinations()
	#test_create_generic_vaccine_sql()
	#test_write_generic_vaccine_sql(sys.argv[2], sys.argv[3])
