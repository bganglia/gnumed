# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class wxgHealthIssueEditAreaPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgHealthIssueEditAreaPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		from Gnumed.wxpython.gmPhraseWheel import cPhraseWheel
		self._PRW_condition = cPhraseWheel(self, wx.ID_ANY, "")
		self._ChBOX_left = wx.CheckBox(self, wx.ID_ANY, _("left"))
		self._ChBOX_right = wx.CheckBox(self, wx.ID_ANY, _("right"))
		from Gnumed.wxpython.gmEMRStructWidgets import cDiagnosticCertaintyClassificationPhraseWheel
		self._PRW_certainty = cDiagnosticCertaintyClassificationPhraseWheel(self, wx.ID_ANY, "")
		self._PRW_grouping = cPhraseWheel(self, wx.ID_ANY, "")
		self._PRW_age_noted = cPhraseWheel(self, wx.ID_ANY, "")
		from Gnumed.wxpython.gmDateTimeInput import cFuzzyTimestampInput
		self._PRW_year_noted = cFuzzyTimestampInput(self, wx.ID_ANY, "")
		self._TCTRL_status = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
		self._ChBOX_active = wx.CheckBox(self, wx.ID_ANY, _("Active"))
		self._ChBOX_relevant = wx.CheckBox(self, wx.ID_ANY, _("Relevant"))
		self._ChBOX_confidential = wx.CheckBox(self, wx.ID_ANY, _("Confidential"))
		self._ChBOX_caused_death = wx.CheckBox(self, wx.ID_ANY, _("Caused death"))
		from Gnumed.wxpython.gmCodingWidgets import cGenericCodesPhraseWheel
		self._PRW_codes = cGenericCodesPhraseWheel(self, wx.ID_ANY, "")
		self._TCTRL_code_details = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgHealthIssueEditAreaPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._PRW_condition.SetToolTip(_("Enter the condition (health issue/past history item) here. Keep it short but precise."))
		self._PRW_grouping.SetToolTip(_("Here you can add arbitrary text which will be used for sorting health issues in the tree."))
		self._PRW_age_noted.SetToolTip(_("Enter the age in years when this condition was diagnosed. Setting this will adjust the \"in the year\" field accordingly."))
		self._PRW_year_noted.SetToolTip(_("Enter the year when this condition was diagnosed. Setting this will adjust the \"at age\" field accordingly."))
		self._TCTRL_status.SetToolTip(_("A summary of the state of this issue."))
		self._ChBOX_active.SetToolTip(_("Check if this is an active, ongoing problem."))
		self._ChBOX_active.SetValue(1)
		self._ChBOX_relevant.SetToolTip(_("Check if this is a clinically relevant problem."))
		self._ChBOX_relevant.SetValue(1)
		self._ChBOX_confidential.SetToolTip(_("Check if this condition is to be kept confidential and not disclosed to anyone else."))
		self._ChBOX_caused_death.SetToolTip(_("Check if this condition contributed to causing death of the patient."))
		self._PRW_codes.SetToolTip(_("Codes relevant to this health issue\nseparated by \";\"."))
		self._TCTRL_code_details.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgHealthIssueEditAreaPnl.__do_layout
		__gszr_main = wx.FlexGridSizer(7, 2, 3, 10)
		__szr_options = wx.BoxSizer(wx.HORIZONTAL)
		__szr_diagnosed = wx.BoxSizer(wx.HORIZONTAL)
		__szr_certainty_grouping = wx.BoxSizer(wx.HORIZONTAL)
		__szr_condition = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_condition = wx.StaticText(self, wx.ID_ANY, _("Condition"))
		__lbl_condition.SetForegroundColour(wx.Colour(255, 0, 0))
		__gszr_main.Add(__lbl_condition, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_condition.Add(self._PRW_condition, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 10)
		__szr_condition.Add(self._ChBOX_left, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__szr_condition.Add(self._ChBOX_right, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 5)
		__gszr_main.Add(__szr_condition, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_certainty = wx.StaticText(self, wx.ID_ANY, _("Certainty"))
		__gszr_main.Add(__lbl_certainty, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_certainty_grouping.Add(self._PRW_certainty, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 10)
		__lbl_group = wx.StaticText(self, wx.ID_ANY, _("Grouping:"))
		__szr_certainty_grouping.Add(__lbl_group, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_certainty_grouping.Add(self._PRW_grouping, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 10)
		__gszr_main.Add(__szr_certainty_grouping, 1, wx.EXPAND, 0)
		__lbl_noted = wx.StaticText(self, wx.ID_ANY, _("When Noted"))
		__gszr_main.Add(__lbl_noted, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_age = wx.StaticText(self, wx.ID_ANY, _("Age:"), style=wx.ALIGN_RIGHT)
		__szr_diagnosed.Add(__lbl_age, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_diagnosed.Add(self._PRW_age_noted, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__lbl_year = wx.StaticText(self, wx.ID_ANY, _("Or year:"), style=wx.ALIGN_RIGHT)
		__szr_diagnosed.Add(__lbl_year, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_diagnosed.Add(self._PRW_year_noted, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__gszr_main.Add(__szr_diagnosed, 1, wx.EXPAND, 0)
		__lbl_status = wx.StaticText(self, wx.ID_ANY, _("Synopsis"))
		__gszr_main.Add(__lbl_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(self._TCTRL_status, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__gszr_main.Add((1, 1), 0, wx.EXPAND, 0)
		__szr_options.Add(self._ChBOX_active, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__szr_options.Add(self._ChBOX_relevant, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT, 5)
		__szr_options.Add(self._ChBOX_confidential, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT, 5)
		__szr_options.Add(self._ChBOX_caused_death, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT, 5)
		__gszr_main.Add(__szr_options, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_codes = wx.StaticText(self, wx.ID_ANY, _("Codes"))
		__gszr_main.Add(__lbl_codes, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(self._PRW_codes, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__gszr_main.Add((20, 20), 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__gszr_main.Add(self._TCTRL_code_details, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		self.SetSizer(__gszr_main)
		__gszr_main.Fit(self)
		__gszr_main.AddGrowableRow(3)
		__gszr_main.AddGrowableRow(6)
		__gszr_main.AddGrowableCol(1)
		self.Layout()
		# end wxGlade

# end of class wxgHealthIssueEditAreaPnl
