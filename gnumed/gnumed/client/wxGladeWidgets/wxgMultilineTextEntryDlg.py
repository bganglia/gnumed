#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgMultilineTextEntryDlg.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgMultilineTextEntryDlg(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxgMultilineTextEntryDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._LBL_msg = wx.StaticText(self, -1, "")
        self._TCTRL_text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.HSCROLL)
        self._BTN_save = wx.Button(self, wx.ID_SAVE, "")
        self._BTN_delete = wx.Button(self, wx.ID_DELETE, "")
        self._BTN_clear = wx.Button(self, wx.ID_CLEAR, "")
        self._BTN_restore = wx.Button(self, wx.ID_REVERT_TO_SAVED, "")
        self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, self._BTN_save)
        self.Bind(wx.EVT_BUTTON, self._on_delete_button_pressed, self._BTN_delete)
        self.Bind(wx.EVT_BUTTON, self._on_clear_button_pressed, self._BTN_clear)
        self.Bind(wx.EVT_BUTTON, self._on_restore_button_pressed, self._BTN_restore)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgMultilineTextEntryDlg.__set_properties
        self.SetTitle(_("Generic multi line text entry dialog"))
        self.SetSize((600, 350))
        self._BTN_save.Enable(False)
        self._BTN_delete.Enable(False)
        self._BTN_restore.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgMultilineTextEntryDlg.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._LBL_msg, 0, wx.ALL|wx.EXPAND, 5)
        __szr_main.Add(self._TCTRL_text, 1, wx.ALL|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_save, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_delete, 0, wx.EXPAND, 3)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_clear, 0, wx.RIGHT|wx.EXPAND, 5)
        __szr_buttons.Add(self._BTN_restore, 0, wx.EXPAND, 3)
        __szr_buttons.Add((20, 20), 3, wx.EXPAND, 0)
        __szr_buttons.Add(self._BTN_cancel, 0, wx.EXPAND, 3)
        __szr_main.Add(__szr_buttons, 0, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(__szr_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_save_button_pressed(self, event): # wxGlade: wxgMultilineTextEntryDlg.<event_handler>
        print "Event handler `_on_save_button_pressed' not implemented!"
        event.Skip()

    def _on_delete_button_pressed(self, event): # wxGlade: wxgMultilineTextEntryDlg.<event_handler>
        print "Event handler `_on_delete_button_pressed' not implemented"
        event.Skip()

    def _on_clear_button_pressed(self, event): # wxGlade: wxgMultilineTextEntryDlg.<event_handler>
        print "Event handler `_on_clear_button_pressed' not implemented"
        event.Skip()

    def _on_restore_button_pressed(self, event): # wxGlade: wxgMultilineTextEntryDlg.<event_handler>
        print "Event handler `_on_restore_button_pressed' not implemented"
        event.Skip()

# end of class wxgMultilineTextEntryDlg


if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = wxgMultilineTextEntryDlg(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
