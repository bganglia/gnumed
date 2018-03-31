#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgOrganizationEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgOrganizationEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmOrganizationWidgets import cOrganizationPhraseWheel
        from Gnumed.wxpython.gmOrganizationWidgets import cOrgCategoryPhraseWheel

        # begin wxGlade: wxgOrganizationEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_org = cOrganizationPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_category = cOrgCategoryPhraseWheel(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgOrganizationEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_org.SetToolTip(_("The name of the organization."))
        self._PRW_category.SetToolTip(_("The category of the organizational unit."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgOrganizationEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(2, 2, 1, 3)
        __lbl_org = wx.StaticText(self, -1, _("Organization"))
        __lbl_org.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_org, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_org, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_category = wx.StaticText(self, -1, _("Category"))
        __lbl_category.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_category, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_category, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgOrganizationEAPnl


