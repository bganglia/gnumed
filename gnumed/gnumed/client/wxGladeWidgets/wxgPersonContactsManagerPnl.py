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


class wxgPersonContactsManagerPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgPersonContactsManagerPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		from Gnumed.wxpython.gmPersonContactWidgets import cPersonAddressesManagerPnl
		self._PNL_addresses = cPersonAddressesManagerPnl(self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TAB_TRAVERSAL)
		from Gnumed.wxpython.gmContactWidgets import cCommChannelsManagerPnl
		self._PNL_comms = cCommChannelsManagerPnl(self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TAB_TRAVERSAL)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgPersonContactsManagerPnl.__set_properties
		self.SetFocus()
		self.SetScrollRate(10, 10)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgPersonContactsManagerPnl.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_main.Add(self._PNL_addresses, 1, wx.ALL | wx.EXPAND, 5)
		__szr_main.Add(self._PNL_comms, 1, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		# end wxGlade

# end of class wxgPersonContactsManagerPnl
