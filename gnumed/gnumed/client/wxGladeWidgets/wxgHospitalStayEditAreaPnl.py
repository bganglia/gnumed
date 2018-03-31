#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgHospitalStayEditAreaPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgHospitalStayEditAreaPnl(wx.Panel):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmEMRStructWidgets import cEpisodeSelectionPhraseWheel
        from Gnumed.wxpython.gmHospitalStayWidgets import cHospitalWardPhraseWheel
        from Gnumed.wxpython import gmDateTimeInput

        # begin wxGlade: wxgHospitalStayEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self._PRW_hospital = cHospitalWardPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_episode = cEpisodeSelectionPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_admission = gmDateTimeInput.cDateInputPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._PRW_discharge = gmDateTimeInput.cDateInputPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgHospitalStayEditAreaPnl.__set_properties
        self._PRW_hospital.SetToolTip(_("Mandatory: Which hospital the patient was admitted to."))
        self._PRW_episode.SetToolTip(_("Mandatory: Select, or enter for creation, the episode (reason, condition) of this hospitalization."))
        self._PRW_admission.SetToolTip(_("Mandatory: When was the patient admitted ?"))
        self._PRW_discharge.SetToolTip(_("Optional: When was the Patient discharged ?"))
        self._TCTRL_comment.SetToolTip(_("Optional: An arbitrary comment on this hospital stay."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgHospitalStayEditAreaPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(5, 2, 3, 5)
        __lbl_hospital = wx.StaticText(self, wx.ID_ANY, _("Hospital"))
        __lbl_hospital.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_hospital, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_hospital, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_episode = wx.StaticText(self, wx.ID_ANY, _("Episode"))
        __lbl_episode.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_episode, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_episode, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_admission = wx.StaticText(self, wx.ID_ANY, _("Admitted"))
        __lbl_admission.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_admission, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_admission, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_discharge = wx.StaticText(self, wx.ID_ANY, _("Discharged"))
        _gszr_main.Add(__lbl_discharge, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_discharge, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
        _gszr_main.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgHospitalStayEditAreaPnl


