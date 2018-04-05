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


class wxgMeasurementsReviewDlg(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgMeasurementsReviewDlg.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER | wx.STAY_ON_TOP
		wx.Dialog.__init__(self, *args, **kwds)
		self._LBL_tests = wx.StaticText(self, wx.ID_ANY, _("... test results listing goes here ..."))
		self._RBTN_confirm_abnormal = wx.RadioButton(self, wx.ID_ANY, _("Leave as is"), style=wx.RB_GROUP)
		self._RBTN_results_normal = wx.RadioButton(self, wx.ID_ANY, _("&Normal"))
		self._RBTN_results_abnormal = wx.RadioButton(self, wx.ID_ANY, _("A&bnormal"))
		self._RBTN_confirm_relevance = wx.RadioButton(self, wx.ID_ANY, _("Leave as is"), style=wx.RB_GROUP)
		self._RBTN_results_not_relevant = wx.RadioButton(self, wx.ID_ANY, _("Not relevant"))
		self._RBTN_results_relevant = wx.RadioButton(self, wx.ID_ANY, _("&Relevant"))
		self._TCTRL_comment = wx.TextCtrl(self, wx.ID_ANY, "")
		self._CHBOX_responsible = wx.CheckBox(self, wx.ID_ANY, _("&Take responsibility"))
		self._BTN_sign_off = wx.Button(self, wx.ID_APPLY, "")
		self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, "")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self._on_signoff_button_pressed, self._BTN_sign_off)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgMeasurementsReviewDlg.__set_properties
		self.SetTitle(_("Signing off test results"))
		self._RBTN_confirm_abnormal.SetToolTip(_("Select this if you want to agree with the current decision on technical abnormality of the results."))
		self._RBTN_confirm_abnormal.SetValue(1)
		self._RBTN_results_normal.SetToolTip(_("Select this if you think the selected results are normal regardless of what the result provider said."))
		self._RBTN_results_abnormal.SetToolTip(_("Select this if you think the selected results are technically abnormal - regardless of what the result provider said."))
		self._RBTN_confirm_relevance.SetToolTip(_("Select this if you want to agree with the current decision on clinical relevance of the results."))
		self._RBTN_confirm_relevance.SetValue(1)
		self._RBTN_results_not_relevant.SetToolTip(_("Select this if you think the selected results are clinically not significant."))
		self._RBTN_results_relevant.SetToolTip(_("Select this if you think the selected results are cliniccally significant."))
		self._TCTRL_comment.SetToolTip(_("Enter a comment on this review. Only available if the review applies to a single result only."))
		self._TCTRL_comment.Enable(False)
		self._CHBOX_responsible.SetToolTip(_("Check this to take over responsibility for initiating action on these results."))
		self._BTN_sign_off.SetToolTip(_("Sign off test results and save review status for all selected results."))
		self._BTN_cancel.SetToolTip(_("Cancel and discard review, that is, do NOT sign off results."))
		self._BTN_cancel.SetDefault()
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgMeasurementsReviewDlg.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
		__szr_comment = wx.BoxSizer(wx.HORIZONTAL)
		__szr_review = wx.BoxSizer(wx.HORIZONTAL)
		__szr_relevant = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Clinically relevant")), wx.HORIZONTAL)
		__szr_abnormal = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Technically abnormal")), wx.HORIZONTAL)
		__msg_top = wx.StaticText(self, wx.ID_ANY, _("This signing applies to ALL results currently selected in the viewer.\n\nIf you want to change the scope of the sign-off\nyou need to narrow or widen the selection of results."), style=wx.ALIGN_CENTER)
		__szr_main.Add(__msg_top, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		__hline_atop_tests = wx.StaticLine(self, wx.ID_ANY)
		__szr_main.Add(__hline_atop_tests, 0, wx.ALL | wx.EXPAND, 5)
		__szr_main.Add(self._LBL_tests, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		__szr_abnormal.Add(self._RBTN_confirm_abnormal, 0, wx.EXPAND, 3)
		__szr_abnormal.Add(self._RBTN_results_normal, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
		__szr_abnormal.Add(self._RBTN_results_abnormal, 0, wx.EXPAND, 0)
		__szr_review.Add(__szr_abnormal, 1, wx.EXPAND, 0)
		__szr_relevant.Add(self._RBTN_confirm_relevance, 0, wx.EXPAND | wx.RIGHT, 3)
		__szr_relevant.Add(self._RBTN_results_not_relevant, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 3)
		__szr_relevant.Add(self._RBTN_results_relevant, 0, wx.EXPAND, 3)
		__szr_review.Add(__szr_relevant, 1, wx.EXPAND, 0)
		__szr_main.Add(__szr_review, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		__lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
		__szr_comment.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_comment.Add(self._TCTRL_comment, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		__szr_comment.Add(self._CHBOX_responsible, 0, wx.EXPAND, 5)
		__szr_main.Add(__szr_comment, 0, wx.ALL | wx.EXPAND, 5)
		__szr_buttons.Add((20, 20), 2, wx.EXPAND, 5)
		__szr_buttons.Add(self._BTN_sign_off, 0, wx.EXPAND, 0)
		__szr_buttons.Add((20, 20), 1, wx.EXPAND, 5)
		__szr_buttons.Add(self._BTN_cancel, 0, wx.EXPAND, 0)
		__szr_buttons.Add((20, 20), 2, wx.EXPAND, 5)
		__szr_main.Add(__szr_buttons, 0, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		self.Centre()
		# end wxGlade

	def _on_signoff_button_pressed(self, event):  # wxGlade: wxgMeasurementsReviewDlg.<event_handler>
		print("Event handler '_on_signoff_button_pressed' not implemented!")
		event.Skip()

# end of class wxgMeasurementsReviewDlg
