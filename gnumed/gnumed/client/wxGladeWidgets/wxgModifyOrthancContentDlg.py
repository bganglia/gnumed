#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.0
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmTextCtrl import cTextCtrl
from Gnumed.wxpython.gmListWidgets import cReportListCtrl
# end wxGlade


class wxgModifyOrthancContentDlg(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgModifyOrthancContentDlg.__init__
		kwds["style"] = wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
		wx.Dialog.__init__(self, *args, **kwds)
		self._TCTRL_search_term = cTextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._BTN_search_patients = wx.Button(self, wx.ID_ANY, _("&Search"), style=wx.BU_EXACTFIT)
		self._LCTRL_patients = cReportListCtrl(self, wx.ID_ANY, style=wx.BORDER_NONE | wx.LC_REPORT)
		self._TCTRL_new_patient_id = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._BTN_suggest_patient_id = wx.Button(self, wx.ID_ANY, _("Suggest"), style=wx.BU_EXACTFIT)
		self._BTN_set_patient_id = wx.Button(self, wx.ID_ANY, _("Set"), style=wx.BU_EXACTFIT)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self._on_search_patients_button_pressed, self._BTN_search_patients)
		self.Bind(wx.EVT_BUTTON, self._on_suggest_patient_id_button_pressed, self._BTN_suggest_patient_id)
		self.Bind(wx.EVT_BUTTON, self._on_set_patient_id_button_pressed, self._BTN_set_patient_id)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgModifyOrthancContentDlg.__set_properties
		self.SetTitle(_("dialog_1"))
		self._BTN_search_patients.SetToolTip(_("Search patients in Orthanc DICOM store."))
		self._BTN_suggest_patient_id.SetToolTip(_("Suggest a patient ID based on the active patient."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgModifyOrthancContentDlg.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_patient_id = wx.BoxSizer(wx.HORIZONTAL)
		__szr_search = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_search_term = wx.StaticText(self, wx.ID_ANY, _("Search term:"))
		__szr_search.Add(__lbl_search_term, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_search.Add(self._TCTRL_search_term, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_search.Add(self._BTN_search_patients, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_main.Add(__szr_search, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__szr_main.Add(self._LCTRL_patients, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 3)
		__lbl_new_patient_id = wx.StaticText(self, wx.ID_ANY, _("New patient ID:"))
		__szr_patient_id.Add(__lbl_new_patient_id, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_patient_id.Add(self._TCTRL_new_patient_id, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_patient_id.Add(self._BTN_suggest_patient_id, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_patient_id.Add(self._BTN_set_patient_id, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_main.Add(__szr_patient_id, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 0)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		# end wxGlade

	def _on_search_patients_button_pressed(self, event):  # wxGlade: wxgModifyOrthancContentDlg.<event_handler>
		print "Event handler '_on_search_patients_button_pressed' not implemented!"
		event.Skip()

	def _on_suggest_patient_id_button_pressed(self, event):  # wxGlade: wxgModifyOrthancContentDlg.<event_handler>
		print "Event handler '_on_suggest_patient_id_button_pressed' not implemented!"
		event.Skip()

	def _on_set_patient_id_button_pressed(self, event):  # wxGlade: wxgModifyOrthancContentDlg.<event_handler>
		print "Event handler '_on_set_patient_id_button_pressed' not implemented!"
		event.Skip()

# end of class wxgModifyOrthancContentDlg
