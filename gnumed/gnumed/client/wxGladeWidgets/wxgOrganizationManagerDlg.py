#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-git/gnumed/gnumed/client/wxg/wxgOrganizationManagerDlg.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgOrganizationManagerDlg(wx.Dialog):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython.gmOrganizationWidgets import cOrganizationsManagerPnl
        from Gnumed.wxpython.gmOrganizationWidgets import cOrgUnitsManagerPnl
        from Gnumed.wxpython.gmPersonContactWidgets import cAddressEditAreaPnl
        from Gnumed.wxpython.gmOrganizationWidgets import cOrgUnitAddressPnl
        from Gnumed.wxpython.gmContactWidgets import cCommChannelsManagerPnl

        # begin wxGlade: wxgOrganizationManagerDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._PNL_orgs = cOrganizationsManagerPnl(self, -1)
        self._PNL_units = cOrgUnitsManagerPnl(self, -1)
        self._PNL_address = cOrgUnitAddressPnl(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._PNL_comms = cCommChannelsManagerPnl(self, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgOrganizationManagerDlg.__set_properties
        self.SetTitle(_("Managing Organizations and their units."))
        self.SetSize((875, 519))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgOrganizationManagerDlg.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_units = wx.BoxSizer(wx.HORIZONTAL)
        __szr_unit_details = wx.BoxSizer(wx.VERTICAL)
        __szr_main.Add(self._PNL_orgs, 1, wx.ALL|wx.EXPAND, 5)
        __szr_units.Add(self._PNL_units, 2, wx.LEFT|wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        __lbl_pusher = wx.StaticText(self, -1, "")
        __szr_unit_details.Add(__lbl_pusher, 0, wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 3)
        __hline_middle = wx.StaticLine(self, -1)
        __szr_unit_details.Add(__hline_middle, 0, wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 20)
        __szr_unit_details.Add(self._PNL_address, 1, wx.LEFT|wx.EXPAND, 5)
        __szr_unit_details.Add(self._PNL_comms, 2, wx.LEFT|wx.EXPAND, 1)
        __szr_units.Add(__szr_unit_details, 3, wx.RIGHT|wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
        __szr_main.Add(__szr_units, 1, wx.EXPAND, 0)
        self.SetSizer(__szr_main)
        self.Layout()
        # end wxGlade

# end of class wxgOrganizationManagerDlg


if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dlg = (None, -1, "")
    app.SetTopWindow(dlg)
    dlg.Show()
    app.MainLoop()
