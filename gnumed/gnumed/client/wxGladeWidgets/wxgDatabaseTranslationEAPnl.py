#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgDatabaseTranslationEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgDatabaseTranslationEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgDatabaseTranslationEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._TCTRL_original = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.NO_BORDER)
        self._TCTRL_translation = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.NO_BORDER)
        self._TCTRL_language = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgDatabaseTranslationEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._TCTRL_original.SetToolTip(_("Original string as found in the database. Usually in English."))
        self._TCTRL_translation.SetToolTip(_("Enter your translation here."))
        self._TCTRL_language.SetToolTip(_("Enter the language code here. You need either the two letter or the four letter ISO code. When entering four letter codes use the format xx_XX, such as de_DE."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgDatabaseTranslationEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(3, 2, 1, 3)
        __lbl_string = wx.StaticText(self, -1, _("String"))
        _gszr_main.Add(__lbl_string, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_original, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_translation = wx.StaticText(self, -1, _("Translation"))
        _gszr_main.Add(__lbl_translation, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_translation, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_language = wx.StaticText(self, -1, _("Language"))
        _gszr_main.Add(__lbl_language, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_language, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableRow(0)
        _gszr_main.AddGrowableRow(1)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgDatabaseTranslationEAPnl


