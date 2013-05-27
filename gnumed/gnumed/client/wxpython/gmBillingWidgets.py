#  coding: utf8
"""GNUmed billing handling widgets."""

#================================================================
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL v2 or later"

import logging
import sys


import wx


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDateTime
from Gnumed.pycommon import gmMatchProvider
from Gnumed.pycommon import gmDispatcher
from Gnumed.pycommon import gmPG2
from Gnumed.pycommon import gmCfg
from Gnumed.pycommon import gmPrinting
from Gnumed.pycommon import gmNetworkTools

from Gnumed.business import gmBilling
from Gnumed.business import gmPerson
from Gnumed.business import gmStaff
from Gnumed.business import gmDocuments
from Gnumed.business import gmPraxis
from Gnumed.business import gmForms
from Gnumed.business import gmDemographicRecord

from Gnumed.wxpython import gmListWidgets
from Gnumed.wxpython import gmRegetMixin
from Gnumed.wxpython import gmPhraseWheel
from Gnumed.wxpython import gmGuiHelpers
from Gnumed.wxpython import gmEditArea
from Gnumed.wxpython import gmPersonContactWidgets
from Gnumed.wxpython import gmPatSearchWidgets
from Gnumed.wxpython import gmMacro
from Gnumed.wxpython import gmFormWidgets
from Gnumed.wxpython import gmDocumentWidgets
from Gnumed.wxpython import gmDataPackWidgets


_log = logging.getLogger('gm.ui')

#================================================================
def manage_billables(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#------------------------------------------------------------
#	def edit(substance=None):
#		return edit_consumable_substance(parent = parent, substance = substance, single_entry = (substance is not None))
	#------------------------------------------------------------
	def delete(billable):
		if billable.is_in_use:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot delete this billable item. It is in use.'), beep = True)
			return False
		return gmBilling.delete_billable(pk_billable = billable['pk_billable'])
	#------------------------------------------------------------
	def get_tooltip(item):
		if item is None:
			return None
		return item.format()
	#------------------------------------------------------------
	def refresh(lctrl):
		billables = gmBilling.get_billables()
		items = [ [
			b['billable_code'],
			b['billable_description'],
			u'%(currency)s%(raw_amount)s' % b,
			u'%s (%s)' % (b['catalog_short'], b['catalog_version']),
			gmTools.coalesce(b['comment'], u''),
			b['pk_billable']
		] for b in billables ]
		lctrl.set_string_items(items)
		lctrl.set_data(billables)
	#------------------------------------------------------------
	def manage_data_packs(billable):
		gmDataPackWidgets.manage_data_packs(parent = parent)
		return True
	#------------------------------------------------------------
	def browse_catalogs(billable):
		dbcfg = gmCfg.cCfgSQL()
		url = dbcfg.get2 (
			option = 'external.urls.schedules_of_fees',
			workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
			bias = 'user',
			default = u'http://www.e-bis.de/goae/defaultFrame.htm'
		)
		gmNetworkTools.open_url_in_browser(url = url)
		return False
	#------------------------------------------------------------
	msg = _('\nThese are the items for billing registered with GNUmed.\n')

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing billable items.'),
		columns = [_('Code'), _('Description'), _('Value'), _('Catalog'), _('Comment'), u'#'],
		single_selection = True,
		#new_callback = edit,
		#edit_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		middle_extra_button = (
			_('Data packs'),
			_('Browse and install billing catalog (schedule of fees) data packs'),
			manage_data_packs
		),
		right_extra_button = (
			_('Catalogs (WWW)'),
			_('Browse billing catalogs (schedules of fees) on the web'),
			browse_catalogs
		),
		list_tooltip_callback = get_tooltip
	)

#================================================================
class cBillablePhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		query = u"""
			SELECT -- DISTINCT ON (label)
				r_vb.pk_billable
					AS data,
				r_vb.billable_code || ': ' || r_vb.billable_description || ' (' || r_vb.catalog_short || ' - ' || r_vb.catalog_version || ')'
					AS list_label,
				r_vb.billable_code || ' (' || r_vb.catalog_short || ' - ' || r_vb.catalog_version || ')'
					AS field_label
			FROM
				ref.v_billables r_vb
			WHERE
				r_vb.active
					AND (
						r_vb.billable_code %(fragment_condition)s
							OR
						r_vb.billable_description %(fragment_condition)s
					)
			ORDER BY list_label
			LIMIT 20
		"""
		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(1, 2, 4)
		self.matcher = mp
	#------------------------------------------------------------
	def _data2instance(self):
		return gmBilling.cBillable(aPK_obj = self._data.values()[0]['data'])
	#------------------------------------------------------------
	def _get_data_tooltip(self):
		if self.GetData() is None:
			return None
		billable = gmBilling.cBillable(aPK_obj = self._data.values()[0]['data'])
		return billable.format()
	#------------------------------------------------------------
	def set_from_instance(self, instance):
		val = u'%s (%s - %s)' % (
			instance['billable_code'],
			instance['catalog_short'],
			instance['catalog_version']
		)
		self.SetText(value = val, data = instance['pk_billable'])
	#------------------------------------------------------------
	def set_from_pk(self, pk):
		self.set_from_instance(gmBilling.cBillable(aPK_obj = pk))

#================================================================
# invoice related widgets
#----------------------------------------------------------------
def configure_invoice_template(parent=None, with_vat=True):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	template = gmFormWidgets.manage_form_templates (
		parent = parent,
		template_types = ['invoice']
	)

	if template is None:
		gmDispatcher.send(signal = 'statustext', msg = _('No invoice template configured.'), beep = True)
		return None

	if template['engine'] not in [u'L', u'X']:
		gmDispatcher.send(signal = 'statustext', msg = _('No invoice template configured.'), beep = True)
		return None

	if with_vat:
		option = u'form_templates.invoice_with_vat'
	else:
		option = u'form_templates.invoice_no_vat'

	dbcfg = gmCfg.cCfgSQL()
	dbcfg.set (
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		option = option,
		value = u'%s - %s' % (template['name_long'], template['external_version'])
	)

	return template
#----------------------------------------------------------------
def get_invoice_template(parent=None, with_vat=True):

	dbcfg = gmCfg.cCfgSQL()
	if with_vat:
		option = u'form_templates.invoice_with_vat'
	else:
		option = u'form_templates.invoice_no_vat'

	template = dbcfg.get2 (
		option = option,
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		bias = 'user'
	)

	if template is None:
		template = configure_invoice_template(parent = parent, with_vat = with_vat)
		if template is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('There is no invoice template configured.'),
				aTitle = _('Getting invoice template')
			)
			return None
	else:
		try:
			name, ver = template.split(u' - ')
		except:
			_log.exception('problem splitting invoice template name [%s]', template)
			gmDispatcher.send(signal = 'statustext', msg = _('Problem loading invoice template.'), beep = True)
			return None
		template = gmForms.get_form_template(name_long = name, external_version = ver)
		if template is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot load invoice template [%s - %s]') % (name, ver),
				aTitle = _('Getting invoice template')
			)
			return None

	return template

#================================================================
# per-patient bill related widgets
#----------------------------------------------------------------
def edit_bill(parent=None, bill=None, single_entry=False):

	if bill is None:
		# manually creating bills is not yet supported
		return

	ea = cBillEAPnl(parent = parent, id = -1)
	ea.data = bill
	ea.mode = gmTools.coalesce(bill, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(bill, _('Adding new bill'), _('Editing bill')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False
#----------------------------------------------------------------
def create_bill_from_items(bill_items=None):

	if len(bill_items) == 0:
		return None

	item = bill_items[0]
	currency = item['currency']
	vat = item['vat_multiplier']
	pat = item['pk_patient']

	# check item consistency
	has_errors = False
	for item in bill_items:
		if	(item['currency'] != currency) or (
			 item['vat_multiplier'] != vat) or (
			 item['pk_patient'] != pat
			):
			msg = _(
				'All items to be included with a bill must\n'
				'coincide on currency, VAT, and patient.\n'
				'\n'
				'This item does not:\n'
				'\n'
				'%s\n'
			) % item.format()
			has_errors = True

		if item['pk_bill'] is not None:
			msg = _(
				'This item is already invoiced:\n'
				'\n'
				'%s\n'
				'\n'
				'Cannot put it on a second bill.'
			) % item.format()
			has_errors = True

		if has_errors:
			gmGuiHelpers.gm_show_warning(aTitle = _('Checking invoice items'), aMessage = msg)
			return None

	# create bill
	bill = gmBilling.create_bill(invoice_id = gmBilling.get_invoice_id(pk_patient = pat))
	_log.info('created bill [%s]', bill['invoice_id'])
	bill.add_items(items = bill_items)
	bill.set_missing_address_from_default()

	return bill
#----------------------------------------------------------------
def create_invoice_from_bill(parent = None, bill=None, print_it=False, keep_a_copy=True):

	bill_patient_not_active = False
	# do we have a current patient ?
	curr_pat = gmPerson.gmCurrentPatient()
	if curr_pat.connected:
		# is the bill about the current patient, too ?
		# (because that's what the new invoice would get
		#  created for and attached to)
		if curr_pat.ID != bill['pk_patient']:
			bill_patient_not_active = True
	else:
		bill_patient_not_active = True

	# FIXME: could ask whether to set fk_receiver_identity
	# FIXME: but this would need enabling the bill EA to edit same
	if bill_patient_not_active:
		activate_patient = gmGuiHelpers.gm_show_question (
			title = _('Creating invoice'),
			question = _(
				'Cannot find an existing invoice PDF for this bill.\n'
				'\n'
				'Active patient: %s\n'
				'Patient on bill: #%s\n'
				'\n'
				'Activate patient on bill so invoice PDF can be created ?'
			) % (
				gmTools.coalesce(curr_pat.ID, u'', u'#%s'),
				bill['pk_patient']
			)
		)
		if not activate_patient:
			return False
		if not gmPatSearchWidgets.set_active_patient(patient = bill['pk_patient']):
			gmGuiHelpers.gm_show_error (
				aTitle = _('Creating invoice'),
				aMessage = _('Cannot activate patient #%s.') % bill['pk_patient']
			)
			return False

	if None in [ bill['close_date'], bill['pk_receiver_address'] ]:
		edit_bill(parent = parent, bill = bill, single_entry = True)
		# cannot invoice open bills
		if bill['close_date'] is None:
			_log.error('cannot create invoice from bill, bill not closed')
			gmGuiHelpers.gm_show_warning (
				aTitle = _('Creating invoice'),
				aMessage = _(
					'Cannot create invoice from bill.\n'
					'\n'
					'The bill is not closed.'
				)
			)
			return False
		# cannot create invoice if no receiver address
		if bill['pk_receiver_address'] is None:
			_log.error('cannot create invoice from bill, lacking receiver address')
			gmGuiHelpers.gm_show_warning (
				aTitle = _('Creating invoice'),
				aMessage = _(
					'Cannot create invoice from bill.\n'
					'\n'
					'There is no receiver address.'
				)
			)
			return False

	# find template
	template = get_invoice_template(parent = parent, with_vat = bill['apply_vat'])
	if template is None:
		gmGuiHelpers.gm_show_warning (
			aTitle = _('Creating invoice'),
			aMessage = _(
				'Cannot create invoice from bill\n'
				'without an invoice template.'
			)
		)
		return False

	# process template
	try:
		invoice = template.instantiate()
	except KeyError:
		_log.exception('cannot instantiate invoice template [%s]', template)
		gmGuiHelpers.gm_show_error (
			aMessage = _('Invalid invoice template [%s - %s (%s)]') % (name, ver, template['engine']),
			aTitle = _('Printing medication list')
		)
		return False

	ph = gmMacro.gmPlaceholderHandler()
	#ph.debug = True
	ph.set_cache_value('bill', bill)
	invoice.substitute_placeholders(data_source = ph)
	ph.unset_cache_value('bill')
	pdf_name = invoice.generate_output()
	if pdf_name is None:
		gmGuiHelpers.gm_show_error (
			aMessage = _('Error generating invoice PDF.'),
			aTitle = _('Creating invoice')
		)
		return False

	# keep a copy
	if keep_a_copy:
		files2import = []
		files2import.extend(invoice.final_output_filenames)
		files2import.extend(invoice.re_editable_filenames)
		doc = gmDocumentWidgets.save_files_as_new_document (
			parent = parent,
			filenames = files2import,
			document_type = template['instance_type'],
			review_as_normal = True,
			reference = bill['invoice_id']
		)
		bill['pk_doc'] = doc['pk_doc']
		bill.save()

	if not print_it:
		return True

	# print template
	printed = gmPrinting.print_files(filenames = [pdf_name], jobtype = 'invoice')
	if not printed:
		gmGuiHelpers.gm_show_error (
			aMessage = _('Error printing the invoice.'),
			aTitle = _('Printing invoice')
		)
		return True

	return True

#----------------------------------------------------------------
def delete_bill(parent=None, bill=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	dlg = gmGuiHelpers.c3ButtonQuestionDlg (
		parent,	-1,
		caption = _('Deleting bill'),
		question = _(
			'When deleting the bill [%s]\n'
			'do you want to keep its items (effectively \"unbilling\" them)\n'
			'or do you want to also delete the bill items from the patient ?\n'
		) % bill['invoice_id'],
		button_defs = [
			{'label': _('Delete + keep'), 'tooltip': _('Delete the bill but keep ("unbill") its items.'), 'default': True},
			{'label': _('Delete all'), 'tooltip': _('Delete both the bill and its items from the patient.')}
		],
		show_checkbox = True,
		checkbox_msg = _('Also remove invoice PDF'),
		checkbox_tooltip = _('Also remove the invoice PDF from the document archive (because it will not correspond to the bill anymore).')
	)
	button_pressed = dlg.ShowModal()
	delete_invoice = dlg.checkbox_is_checked()
	dlg.Destroy()

	if button_pressed == wx.ID_CANCEL:
		return False

	if button_pressed == wx.ID_YES:
		for item in bill.bill_items:
			item['pk_bill'] = None
			item.save()

	if button_pressed == wx.ID_NO:
		for item in bill.bill_items:
			item['pk_bill'] = None
			item.save()
			gmBilling.delete_bill_item(pk_bill_item = item['pk_bill_item'])

	if delete_invoice:
		if bill['pk_doc'] is not None:
			gmDocuments.delete_document (
				document_id = bill['pk_doc'],
				encounter_id = gmPerson.cPatient(aPK_obj = bill['pk_patient']).emr.active_encounter['pk_encounter']
			)

	return gmBilling.delete_bill(pk_bill = bill['pk_bill'])

#----------------------------------------------------------------
def remove_items_from_bill(parent=None, bill=None):

	if bill is None:
		return False

	list_data = bill.bill_items
	if len(list_data) == 0:
		return False

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	list_items = [ [
		gmDateTime.pydt_strftime(b['date_to_bill'], '%Y %b %d', accuracy = gmDateTime.acc_days),
		b['unit_count'],
		u'%s: %s%s' % (b['billable_code'], b['billable_description'], gmTools.coalesce(b['item_detail'], u'', u' - %s')),
		u'%(curr)s %(total_val)s (%(count)s %(x)s %(unit_val)s%(x)s%(val_multiplier)s)' % {
			'curr': b['currency'],
			'total_val': b['total_amount'],
			'count': b['unit_count'],
			'x': gmTools.u_multiply,
			'unit_val': b['net_amount_per_unit'],
			'val_multiplier': b['amount_multiplier']
		},
		u'%(curr)s%(vat)s (%(perc_vat)s%%)' % {
			'vat': b['vat'],
			'curr': b['currency'],
			'perc_vat': b['vat_multiplier'] * 100
		},
		u'%s (%s)' % (b['catalog_short'], b['catalog_version']),
		b['pk_bill_item']
	] for b in list_data ]

	msg = _('Select the items you want to remove from bill [%s]:\n') % bill['invoice_id']
	items2remove = gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Removing items from bill'),
		columns = [_('Date'), _('Count'), _('Description'), _('Value'), _('VAT'), _('Catalog'), u'#'],
		single_selection = False,
		choices = list_items,
		data = list_data
	)

	if items2remove is None:
		return False

	dlg = gmGuiHelpers.c3ButtonQuestionDlg (
		parent,	-1,
		caption = _('Removing items from bill'),
		question = _(
			'%s items selected from bill [%s]\n'
			'\n'
			'Do you want to only remove the selected items\n'
			'from the bill ("unbill" them) or do you want\n'
			'to delete them entirely from the patient ?\n'
			'\n'
			'Note that neither action is reversible.'
		) % (
			len(items2remove),
			bill['invoice_id']
		),
		button_defs = [
			{'label': _('"Unbill"'), 'tooltip': _('Only "unbill" items (remove from bill but do not delete from patient).'), 'default': True},
			{'label': _('Delete'), 'tooltip': _('Completely delete items from the patient.')}
		],
		show_checkbox = True,
		checkbox_msg = _('Also remove invoice PDF'),
		checkbox_tooltip = _('Also remove the invoice PDF from the document archive (because it will not correspond to the bill anymore).')
	)
	button_pressed = dlg.ShowModal()
	delete_invoice = dlg.checkbox_is_checked()
	dlg.Destroy()

	if button_pressed == wx.ID_CANCEL:
		return False

	# remember this because unlinking/deleting the items
	# will remove the patient PK from the bill
	pk_patient = bill['pk_patient']

	for item in items2remove:
		item['pk_bill'] = None
		item.save()
		if button_pressed == wx.ID_NO:
			gmBilling.delete_bill_item(pk_bill_item = item['pk_bill_item'])

	if delete_invoice:
		if bill['pk_doc'] is not None:
			gmDocuments.delete_document (
				document_id = bill['pk_doc'],
				encounter_id = gmPerson.cPatient(aPK_obj = pk_patient).emr.active_encounter['pk_encounter']
			)

	# delete bill, too, if empty
	if len(bill.bill_items) == 0:
		gmBilling.delete_bill(pk_bill = bill['pk_bill'])

	return True
#----------------------------------------------------------------
def manage_bills(parent=None, patient=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#------------------------------------------------------------
	def show_pdf(bill):
		if bill is None:
			return False

		# find invoice
		invoice = bill.invoice
		if invoice is not None:
			success, msg = invoice.parts[-1].display_via_mime()
			if not success:
				gmGuiHelpers.gm_show_error(aMessage = msg, aTitle = _('Displaying invoice'))
			return False

		# create it ?
		create_it = gmGuiHelpers.gm_show_question (
			title = _('Displaying invoice'),
			question = _(
				'Cannot find an existing\n'
				'invoice PDF for this bill.\n'
				'\n'
				'Do you want to create one ?'
			),
		)
		if not create_it:
			return False

		# prepare invoicing
		if not bill.set_missing_address_from_default():
			gmGuiHelpers.gm_show_warning (
				aTitle = _('Creating invoice'),
				aMessage = _(
					'There is no pre-configured billing address.\n'
					'\n'
					'Select the address you want to send the bill to.'
				)
			)
			edit_bill(parent = parent, bill = bill, single_entry = True)
			if bill['pk_receiver_address'] is None:
				return False
		if bill['close_date'] is None:
			bill['close_date'] = gmDateTime.pydt_now_here()
			bill.save()

		return create_invoice_from_bill(parent = parent, bill = bill, print_it = True, keep_a_copy = True)
	#------------------------------------------------------------
	def edit(bill):
		return edit_bill(parent = parent, bill = bill, single_entry = True)
	#------------------------------------------------------------
	def delete(bill):
		return delete_bill(parent = parent, bill = bill)
	#------------------------------------------------------------
	def remove_items(bill):
		return remove_items_from_bill(parent = parent, bill = bill)
	#------------------------------------------------------------
	def get_tooltip(item):
		if item is None:
			return None
		return item.format()
	#------------------------------------------------------------
	def refresh(lctrl):
		if patient is None:
			bills = gmBilling.get_bills()
		else:
			bills = gmBilling.get_bills(pk_patient = patient.ID)
		items = []
		for b in bills:
			if b['close_date'] is None:
				close_date = _('<open>')
			else:
				close_date = gmDateTime.pydt_strftime(b['close_date'], '%Y %b %d')
			if b['total_amount'] is None:
				amount = _('no items on bill')
			else:
				amount = gmTools.bool2subst (
					b['apply_vat'],
					_('%(currency)s%(total_amount_with_vat)s (with %(percent_vat)s%% VAT)') % b,
					u'%(currency)s%(total_amount)s' % b
				)
			items.append ([
				close_date,
				b['invoice_id'],
				amount,
				gmTools.coalesce(b['comment'], u'')
			])
		lctrl.set_string_items(items)
		lctrl.set_data(bills)
	#------------------------------------------------------------
	return gmListWidgets.get_choices_from_list (
		parent = parent,
		caption = _('Showing bills.'),
		columns = [_('Close date'), _('Invoice ID'), _('Value'), _('Comment')],
		single_selection = True,
		edit_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		middle_extra_button = (
			u'PDF',
			_('Create if necessary, and show the corresponding invoice PDF'),
			show_pdf
		),
		right_extra_button = (
			_('Unbill'),
			_('Select and remove items from a bill.'),
			remove_items
		),
		list_tooltip_callback = get_tooltip
	)

#----------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgBillEAPnl

class cBillEAPnl(wxgBillEAPnl.wxgBillEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['bill']
			del kwargs['bill']
		except KeyError:
			data = None

		wxgBillEAPnl.wxgBillEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

#		self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):
		validity = True

		# flag but do not count as wrong
		if not self._PRW_close_date.is_valid_timestamp(allow_empty = False):
			self._PRW_close_date.SetFocus()

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):
		# not intended to be used
		return False
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['close_date'] = self._PRW_close_date.GetData()
		self.data['apply_vat'] = self._CHBOX_vat_applies.GetValue()
		self.data['comment'] = self._TCTRL_comment.GetValue()
		self.data.save()
		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		pass # not used
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._TCTRL_invoice_id.SetValue(self.data['invoice_id'])
		self._PRW_close_date.SetText(data = self.data['close_date'])

		self.data.set_missing_address_from_default()
		if self.data['pk_receiver_address'] is None:
			self._TCTRL_address.SetValue(u'')
		else:
			adr = self.data.address
			self._TCTRL_address.SetValue(adr.format(single_line = True, show_type = False))

		self._TCTRL_value.SetValue(u'%(currency)s%(total_amount)s' % self.data)
		self._CHBOX_vat_applies.SetValue(self.data['apply_vat'])
		self._CHBOX_vat_applies.SetLabel(_('&VAT applies (%s%%)') % self.data['percent_vat'])
		if self.data['apply_vat']:
			tmp = u'%s %%(currency)s%%(total_vat)s %s %s %%(currency)s%%(total_amount_with_vat)s' % (
				gmTools.u_corresponds_to,
				gmTools.u_right_arrow,
				gmTools.u_sum,
			)
			self._TCTRL_value_with_vat.SetValue(tmp % self.data)
		else:
			self._TCTRL_value_with_vat.SetValue(u'')

		self._TCTRL_comment.SetValue(gmTools.coalesce(self.data['comment'], u''))

		self._PRW_close_date.SetFocus()
	#----------------------------------------------------------------
	# event handling
	#----------------------------------------------------------------
	def _on_vat_applies_box_checked(self, event):
		if self._CHBOX_vat_applies.GetValue():
			tmp = u'%s %%(currency)s%%(total_vat)s %s %s %%(currency)s%%(total_amount_with_vat)s' % (
				gmTools.u_corresponds_to,
				gmTools.u_right_arrow,
				gmTools.u_sum,
			)
			self._TCTRL_value_with_vat.SetValue(tmp % self.data)
			return
		self._TCTRL_value_with_vat.SetValue(u'')
	#----------------------------------------------------------------
	def _on_select_address_button_pressed(self, event):
		adr = gmPersonContactWidgets.select_address (
			missing = _('billing'),
			person = gmPerson.cIdentity(aPK_obj = self.data['pk_patient'])
		)
		if adr is None:
			gmGuiHelpers.gm_show_info (
				aTitle = _('Selecting address'),
				aMessage = _('GNUmed does not know any addresses for this patient.')
			)
			return
		self.data['pk_receiver_address'] = adr['pk_lnk_person_org_address']
		self.data.save()
		self._TCTRL_address.SetValue(adr.format(single_line = True, show_type = False))

#================================================================
# per-patient bill items related widgets
#----------------------------------------------------------------
def edit_bill_item(parent=None, bill_item=None, single_entry=False):

	if bill_item is not None:
		if bill_item.is_in_use:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot edit already invoiced bill item.'), beep = True)
			return False

	ea = cBillItemEAPnl(parent = parent, id = -1)
	ea.data = bill_item
	ea.mode = gmTools.coalesce(bill_item, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(bill_item, _('Adding new bill item'), _('Editing bill item')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False
#----------------------------------------------------------------
def manage_bill_items(parent=None, pk_patient=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#------------------------------------------------------------
	def edit(item=None):
		return edit_bill_item(parent = parent, bill_item = item, single_entry = (item is not None))
	#------------------------------------------------------------
	def delete(item):
		if item.is_in_use is not None:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot delete already invoiced bill items.'), beep = True)
			return False
		gmBilling.delete_bill_item(pk_bill_item = item['pk_bill_item'])
		return True
	#------------------------------------------------------------
	def get_tooltip(item):
		if item is None:
			return None
		return item.format()
	#------------------------------------------------------------
	def refresh(lctrl):
		b_items = gmBilling.get_bill_items(pk_patient = pk_patient)
		items = [ [
			gmDateTime.pydt_strftime(b['date_to_bill'], '%Y %b %d', accuracy = gmDateTime.acc_days),
			b['unit_count'],
			u'%s: %s%s' % (b['billable_code'], b['billable_description'], gmTools.coalesce(b['item_detail'], u'', u' - %s')),
			b['currency'],
			u'%s (%s %s %s%s%s)' % (
				b['total_amount'],
				b['unit_count'],
				gmTools.u_multiply,
				b['net_amount_per_unit'],
				gmTools.u_multiply,
				b['amount_multiplier']
			),
			u'%s (%s%%)' % (
				b['vat'],
				b['vat_multiplier'] * 100
			),
			u'%s (%s)' % (b['catalog_short'], b['catalog_version']),
			b['pk_bill_item']
		] for b in b_items ]
		lctrl.set_string_items(items)
		lctrl.set_data(b_items)
	#------------------------------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		#msg = msg,
		caption = _('Showing bill items.'),
		columns = [_('Date'), _('Count'), _('Description'), _('$__replace_by_your_currency_symbol')[:-len('__replace_by_your_currency_symbol')], _('Value'), _('VAT'), _('Catalog'), u'#'],
		single_selection = True,
		new_callback = edit,
		edit_callback = edit,
		delete_callback = delete,
		refresh_callback = refresh,
		list_tooltip_callback = get_tooltip
	)

#------------------------------------------------------------
class cPersonBillItemsManagerPnl(gmListWidgets.cGenericListManagerPnl):
	"""A list for managing a patient's bill items.

	Does NOT act on/listen to the current patient.
	"""
	def __init__(self, *args, **kwargs):

		try:
			self.__identity = kwargs['identity']
			del kwargs['identity']
		except KeyError:
			self.__identity = None

		gmListWidgets.cGenericListManagerPnl.__init__(self, *args, **kwargs)

		self.new_callback = self._add_item
		self.edit_callback = self._edit_item
		self.delete_callback = self._del_item
		self.refresh_callback = self.refresh

		self.__show_non_invoiced_only = True

		self.__init_ui()
		self.refresh()
	#--------------------------------------------------------
	# external API
	#--------------------------------------------------------
	def refresh(self, *args, **kwargs):
		if self.__identity is None:
			self._LCTRL_items.set_string_items()
			return

		b_items = gmBilling.get_bill_items(pk_patient = self.__identity.ID, non_invoiced_only = self.__show_non_invoiced_only)
		items = [ [
			gmDateTime.pydt_strftime(b['date_to_bill'], '%Y %b %d', accuracy = gmDateTime.acc_days),
			b['unit_count'],
			u'%s: %s%s' % (b['billable_code'], b['billable_description'], gmTools.coalesce(b['item_detail'], u'', u' - %s')),
			b['currency'],
			b['total_amount'],
			u'%s (%s%%)' % (
				b['vat'],
				b['vat_multiplier'] * 100
			),
			u'%s (%s)' % (b['catalog_short'], b['catalog_version']),
			u'%s %s %s %s %s' % (
				b['unit_count'],
				gmTools.u_multiply,
				b['net_amount_per_unit'],
				gmTools.u_multiply,
				b['amount_multiplier']
			),
			gmTools.coalesce(b['pk_bill'], gmTools.u_diameter),
			b['pk_encounter_to_bill'],
			b['pk_bill_item']
		] for b in b_items ]

		self._LCTRL_items.set_string_items(items = items)
		self._LCTRL_items.set_column_widths()
		self._LCTRL_items.set_data(data = b_items)
	#--------------------------------------------------------
	# internal helpers
	#--------------------------------------------------------
	def __init_ui(self):
		self._LCTRL_items.set_columns(columns = [
			_('Charge date'),
			_('Count'),
			_('Description'),
			_('$__replace_by_your_currency_symbol')[:-len('__replace_by_your_currency_symbol')],
			_('Value'),
			_('VAT'),
			_('Catalog'),
			_('Count %s Value %s Factor') % (gmTools.u_multiply, gmTools.u_multiply),
			_('Invoice'),
			_('Encounter'),
			u'#'
		])
		self._LCTRL_items.item_tooltip_callback = self._get_item_tooltip
#		self.left_extra_button = (
#			_('Select pending'),
#			_('Select non-invoiced (pending) items.'),
#			self._select_pending_items
#		)
		self.left_extra_button = (
			_('Invoice selected items'),
			_('Create invoice from selected items.'),
			self._invoice_selected_items
		)
		self.middle_extra_button = (
			_('Bills'),
			_('Browse bills of this patient.'),
			self._browse_bills
		)
		self.right_extra_button = (
			_('Billables'),
			_('Browse list of billables.'),
			self._browse_billables
		)
	#--------------------------------------------------------
	def _add_item(self):
		return edit_bill_item(parent = self, bill_item = None, single_entry = False)
	#--------------------------------------------------------
	def _edit_item(self, bill_item):
		return edit_bill_item(parent = self, bill_item = bill_item, single_entry = True)
	#--------------------------------------------------------
	def _del_item(self, item):
		if item['pk_bill'] is not None:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot delete already invoiced bill items.'), beep = True)
			return False
		go_ahead = gmGuiHelpers.gm_show_question (
			_(	'Do you really want to delete this\n'
				'bill item from the patient ?'),
			_('Deleting bill item')
		)
		if not go_ahead:
			return False
		gmBilling.delete_bill_item(pk_bill_item = item['pk_bill_item'])
		return True
	#--------------------------------------------------------
	def _get_item_tooltip(self, item):
		if item is None:
			return None
		return item.format()
	#--------------------------------------------------------
	def _select_pending_items(self, item):
		pass
	#--------------------------------------------------------
	def _invoice_selected_items(self, item):
		bill_items = self._LCTRL_items.get_selected_item_data()
		bill = create_bill_from_items(bill_items)
		if bill is None:
			return
		if bill['pk_receiver_address'] is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _(
					'Cannot create invoice.\n'
					'\n'
					'No receiver address selected.'
				),
				aTitle = _('Creating invoice')
			)
			return
		if bill['close_date'] is None:
			bill['close_date'] = gmDateTime.pydt_now_here()
			bill.save()
		create_invoice_from_bill(parent = self, bill = bill, print_it = True, keep_a_copy = True)
	#--------------------------------------------------------
	def _browse_billables(self, item):
		manage_billables(parent = self)
		return False
	#--------------------------------------------------------
	def _browse_bills(self, item):
		manage_bills(parent = self, patient = self.__identity)
	#--------------------------------------------------------
	# properties
	#--------------------------------------------------------
	def _get_identity(self):
		return self.__identity

	def _set_identity(self, identity):
		self.__identity = identity
		self.refresh()

	identity = property(_get_identity, _set_identity)
	#--------------------------------------------------------
	def _get_show_non_invoiced_only(self):
		return self.__show_non_invoiced_only

	def _set_show_non_invoiced_only(self, value):
		self.__show_non_invoiced_only = value
		self.refresh()

	show_non_invoiced_only = property(_get_show_non_invoiced_only, _set_show_non_invoiced_only)

#------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgBillItemEAPnl

class cBillItemEAPnl(wxgBillItemEAPnl.wxgBillItemEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['bill_item']
			del kwargs['bill_item']
		except KeyError:
			data = None

		wxgBillItemEAPnl.wxgBillItemEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		self.__init_ui()
	#----------------------------------------------------------------
	def __init_ui(self):
		self._PRW_encounter.set_context(context = 'patient', val = gmPerson.gmCurrentPatient().ID)
		self._PRW_billable.add_callback_on_selection(self._on_billable_selected)
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		validity = True

		if self._TCTRL_factor.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_factor, valid = False)
			self._TCTRL_factor.SetFocus()
		else:
			converted, factor = gmTools.input2decimal(self._TCTRL_factor.GetValue())
			if not converted:
				validity = False
				self.display_tctrl_as_valid(tctrl = self._TCTRL_factor, valid = False)
				self._TCTRL_factor.SetFocus()
			else:
				self.display_tctrl_as_valid(tctrl = self._TCTRL_factor, valid = True)

		if self._TCTRL_amount.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = False)
			self._TCTRL_amount.SetFocus()
		else:
			converted, factor = gmTools.input2decimal(self._TCTRL_amount.GetValue())
			if not converted:
				validity = False
				self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = False)
				self._TCTRL_amount.SetFocus()
			else:
				self.display_tctrl_as_valid(tctrl = self._TCTRL_amount, valid = True)

		if self._TCTRL_count.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_count, valid = False)
			self._TCTRL_count.SetFocus()
		else:
			converted, factor = gmTools.input2decimal(self._TCTRL_count.GetValue())
			if not converted:
				validity = False
				self.display_tctrl_as_valid(tctrl = self._TCTRL_count, valid = False)
				self._TCTRL_count.SetFocus()
			else:
				self.display_tctrl_as_valid(tctrl = self._TCTRL_count, valid = True)

		if self._PRW_date.is_valid_timestamp(allow_empty = True):
			self._PRW_date.display_as_valid(True)
		else:
			validity = False
			self._PRW_date.display_as_valid(False)
			self._PRW_date.SetFocus()

		if self._PRW_encounter.GetData() is None:
			validity = False
			self._PRW_encounter.display_as_valid(False)
			self._PRW_encounter.SetFocus()
		else:
			self._PRW_encounter.display_as_valid(True)

		if self._PRW_billable.GetData() is None:
			validity = False
			self._PRW_billable.display_as_valid(False)
			self._PRW_billable.SetFocus()
		else:
			self._PRW_billable.display_as_valid(True)

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):
		data = gmBilling.create_bill_item (
			pk_encounter = self._PRW_encounter.GetData(),
			pk_billable = self._PRW_billable.GetData(),
			pk_staff = gmStaff.gmCurrentProvider()['pk_staff']		# should be settable !
		)
		data['raw_date_to_bill'] = self._PRW_date.GetData()
		converted, data['unit_count'] = gmTools.input2decimal(self._TCTRL_count.GetValue())
		converted, data['net_amount_per_unit'] = gmTools.input2decimal(self._TCTRL_amount.GetValue())
		converted, data['amount_multiplier'] = gmTools.input2decimal(self._TCTRL_factor.GetValue())
		data['item_detail'] = self._TCTRL_comment.GetValue().strip()
		data.save()

		self.data = data
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['pk_encounter_to_bill'] = self._PRW_encounter.GetData()
		self.data['raw_date_to_bill'] = self._PRW_date.GetData()
		converted, self.data['unit_count'] = gmTools.input2decimal(self._TCTRL_count.GetValue())
		converted, self.data['net_amount_per_unit'] = gmTools.input2decimal(self._TCTRL_amount.GetValue())
		converted, self.data['amount_multiplier'] = gmTools.input2decimal(self._TCTRL_factor.GetValue())
		self.data['item_detail'] = self._TCTRL_comment.GetValue().strip()
		return self.data.save()
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_billable.SetText()
		self._PRW_encounter.set_from_instance(gmPerson.gmCurrentPatient().emr.active_encounter)
		self._PRW_date.SetData()
		self._TCTRL_count.SetValue(u'1')
		self._TCTRL_amount.SetValue(u'')
		self._LBL_currency.SetLabel(gmTools.u_euro)
		self._TCTRL_factor.SetValue(u'1')
		self._TCTRL_comment.SetValue(u'')

		self._PRW_billable.Enable()
		self._PRW_billable.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._PRW_billable.SetText()
		self._TCTRL_count.SetValue(u'1')
		self._TCTRL_amount.SetValue(u'')
		self._TCTRL_comment.SetValue(u'')

		self._PRW_billable.Enable()
		self._PRW_billable.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_billable.set_from_pk(self.data['pk_billable'])
		self._PRW_encounter.SetData(self.data['pk_encounter_to_bill'])
		self._PRW_date.SetData(data = self.data['raw_date_to_bill'])
		self._TCTRL_count.SetValue(u'%s' % self.data['unit_count'])
		self._TCTRL_amount.SetValue(u'%s' % self.data['net_amount_per_unit'])
		self._LBL_currency.SetLabel(self.data['currency'])
		self._TCTRL_factor.SetValue(u'%s' % self.data['amount_multiplier'])
		self._TCTRL_comment.SetValue(gmTools.coalesce(self.data['item_detail'], u''))

		self._PRW_billable.Disable()
		self._PRW_date.SetFocus()
	#----------------------------------------------------------------
	def _on_billable_selected(self, item):
		if item is None:
			return
		if self._TCTRL_amount.GetValue().strip() != u'':
			return
		val = u'%s' % self._PRW_billable.GetData(as_instance = True)['raw_amount']
		wx.CallAfter(self._TCTRL_amount.SetValue, val)

#============================================================
# a plugin for billing
#------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgBillingPluginPnl

class cBillingPluginPnl(wxgBillingPluginPnl.wxgBillingPluginPnl, gmRegetMixin.cRegetOnPaintMixin):
	def __init__(self, *args, **kwargs):

		wxgBillingPluginPnl.wxgBillingPluginPnl.__init__(self, *args, **kwargs)
		gmRegetMixin.cRegetOnPaintMixin.__init__(self)
		self.__register_interests()
	#-----------------------------------------------------
	def __reset_ui(self):
		self._PNL_bill_items.identity = None
		self._CHBOX_show_non_invoiced_only.SetValue(1)
		self._PRW_billable.SetText(u'', None)
		self._TCTRL_factor.SetValue(u'1.0')
		self._TCTRL_factor.Disable()
		self._TCTRL_details.SetValue(u'')
		self._TCTRL_details.Disable()
	#-----------------------------------------------------
	# event handling
	#-----------------------------------------------------
	def __register_interests(self):
		gmDispatcher.connect(signal = u'pre_patient_selection', receiver = self._on_pre_patient_selection)
		gmDispatcher.connect(signal = u'post_patient_selection', receiver = self._on_post_patient_selection)

		gmDispatcher.connect(signal = u'bill_item_mod_db', receiver = self._on_bill_item_modified)

		self._PRW_billable.add_callback_on_selection(self._on_billable_selected_in_prw)
	#-----------------------------------------------------
	def _on_pre_patient_selection(self):
		wx.CallAfter(self.__reset_ui)
	#-----------------------------------------------------
	def _on_post_patient_selection(self):
		wx.CallAfter(self._schedule_data_reget)
	#-----------------------------------------------------
	def _on_bill_item_modified(self):
		wx.CallAfter(self._schedule_data_reget)
	#-----------------------------------------------------
	def _on_non_invoiced_only_checkbox_toggled(self, event):
		self._PNL_bill_items.show_non_invoiced_only = self._CHBOX_show_non_invoiced_only.GetValue()
	#--------------------------------------------------------
	def _on_insert_bill_item_button_pressed(self, event):
		val = self._TCTRL_factor.GetValue().strip()
		if val == u'':
			factor = 1.0
		else:
			converted, factor = gmTools.input2decimal(val)
			if not converted:
				gmGuiHelpers.gm_show_warning (
					_('"Factor" must be a number\n\nCannot insert bill item.'),
					_('Inserting bill item')
				)
				return False
		bill_item = gmBilling.create_bill_item (
			pk_encounter = gmPerson.gmCurrentPatient().emr.active_encounter['pk_encounter'],
			pk_billable = self._PRW_billable.GetData(),
			pk_staff = gmStaff.gmCurrentProvider()['pk_staff']
		)
		bill_item['amount_multiplier'] = factor
		bill_item['item_detail'] = self._TCTRL_details.GetValue()
		bill_item.save()

		self._TCTRL_details.SetValue(u'')

		return True
	#--------------------------------------------------------
	def _on_billable_selected_in_prw(self, billable):
		if billable is None:
			self._TCTRL_factor.Disable()
			self._TCTRL_details.Disable()
			self._BTN_insert_item.Disable()
		else:
			self._TCTRL_factor.Enable()
			self._TCTRL_details.Enable()
			self._BTN_insert_item.Enable()
	#-----------------------------------------------------
	# reget-on-paint mixin API
	#-----------------------------------------------------
	def _populate_with_data(self):
		self._PNL_bill_items.identity = gmPerson.gmCurrentPatient()
		return True
#============================================================
# main
#------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit()

	if sys.argv[1] != 'test':
		sys.exit()

	from Gnumed.pycommon import gmI18N
	gmI18N.activate_locale()
	gmI18N.install_domain(domain = 'gnumed')

	#----------------------------------------
	app = wx.PyWidgetTester(size = (600, 600))
	#app.SetWidget(cATCPhraseWheel, -1)
	#app.SetWidget(cSubstancePhraseWheel, -1)
	app.MainLoop()
