#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgGenericAddressEditAreaPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgGenericAddressEditAreaPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmAddressWidgets

        # begin wxGlade: wxgGenericAddressEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._LBL_type = wx.StaticText(self, -1, _("Type"))
        self._PRW_type = gmAddressWidgets.cAddressTypePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._LBL_search = wx.StaticText(self, -1, _("Search"))
        self._PRW_address_searcher = gmAddressWidgets.cAddressPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_zip = gmAddressWidgets.cZipcodePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_street = gmAddressWidgets.cStreetPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_notes_street = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_number = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_subunit = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_urb = gmAddressWidgets.cUrbPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_suburb = gmAddressWidgets.cSuburbPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_state = gmAddressWidgets.cStateSelectionPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_country = gmAddressWidgets.cCountryPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_notes_subunit = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgGenericAddressEditAreaPnl.__set_properties
        self.SetToolTipString(_("Select the type of address here."))
        self.SetScrollRate(10, 10)
        self._LBL_type.SetForegroundColour(wx.Colour(255, 0, 0))
        self._PRW_type.SetToolTipString(_("The category under which to store this address."))
        self._PRW_address_searcher.SetToolTipString(_("Here you can enter a postal code or street name fragment to search for an existing address.\n\nThe fields below will be filled with the details of that address which you can edit to create a new address.\n\nYou can also just enter the relevant information into the corresponding fields without searching for an existing address."))
        self._TCTRL_notes_street.SetToolTipString(_("Enter any additional street level instructions and notes, such as postal box or driving directions."))
        self._TCTRL_number.SetToolTipString(_("Enter the house number for this address."))
        self._TCTRL_subunit.SetToolTipString(_("Enter the subunit / apartment / room / level / entrance for this address."))
        self._TCTRL_notes_subunit.SetToolTipString(_("Enter any additional notes and comments on this address which didn't fit anywhere else."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgGenericAddressEditAreaPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(10, 2, 3, 5)
        __szr_urb = wx.BoxSizer(wx.HORIZONTAL)
        _szr_number = wx.BoxSizer(wx.HORIZONTAL)
        _gszr_main.Add(self._LBL_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_type, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._LBL_search, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_address_searcher, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_zip = wx.StaticText(self, -1, _("Zip code"))
        __LBL_zip.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__LBL_zip, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_zip, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_street = wx.StaticText(self, -1, _("Street"))
        __LBL_street.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__LBL_street, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_street, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_street_notes = wx.StaticText(self, -1, _("... Notes"), style=wx.ALIGN_RIGHT)
        _gszr_main.Add(__LBL_street_notes, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_notes_street, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_number = wx.StaticText(self, -1, _("Number"))
        __LBL_number.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__LBL_number, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _szr_number.Add(self._TCTRL_number, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_subunit = wx.StaticText(self, -1, _("Unit:"))
        _szr_number.Add(__LBL_subunit, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        _szr_number.Add(self._TCTRL_subunit, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(_szr_number, 1, wx.EXPAND, 0)
        __LBL_urb = wx.StaticText(self, -1, _("Place"))
        __LBL_urb.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__LBL_urb, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_urb.Add(self._PRW_urb, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_suburb = wx.StaticText(self, -1, _("Suburb:"))
        __szr_urb.Add(__LBL_suburb, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_urb.Add(self._PRW_suburb, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_urb, 1, wx.EXPAND, 0)
        __LBL_state = wx.StaticText(self, -1, _("Region"))
        __LBL_state.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__LBL_state, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_state, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_country = wx.StaticText(self, -1, _("Country"))
        __LBL_country.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__LBL_country, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_country, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_notes_subunit = wx.StaticText(self, -1, _("Comment"))
        _gszr_main.Add(__LBL_notes_subunit, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_notes_subunit, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgGenericAddressEditAreaPnl


