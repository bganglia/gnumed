# a simple wrapper for the Manual class

"""GNUMed manuals in a HTML browser window

A very basic HTML browser with back/forward history buttons
with  the main pourpose of browsing the gnumed manuals
The manuals should reside where the manual_path points to

@author: Dr. Horst Herb
@version: 0.2
@copyright: GPL
@thanks: this code has been heavily "borrowed" from
         Robin Dunn's extraordinary wxPython sample
"""

import sys, os

from   wxPython.wx         import *
from   wxPython.html       import *
import wxPython.lib.wxpTag
import gmGuiBroker, gmPlugin, gmLog

manual_path = 'doc/gnumed/book1.html'


import images_for_gnumed_browser16_16
import images_gnuMedGP_Toolbar

ID_MANUALCONTENTS = wxNewId()
ID_MANUALBACK = wxNewId()
ID_MANUALFORWARD = wxNewId()
ID_MANUALHOME = wxNewId()
ID_MANUALBABELFISH = wxNewId()
ID_MANUALPRINTER  = wxNewId()
ID_MANUALOPENFILE = wxNewId()
ID_MANUALBOOKMARKS = wxNewId()
ID_MANUALADDBOOKMARK = wxNewId()
ID_MANUALVIEWSOURCE = wxNewId()
ID_MANUALRELOAD = wxNewId()
ID_VIEWSOURCE  = wxNewId()

#----------------------------------------------------------------------


class ManualHtmlWindow(wxHtmlWindow):
    def __init__(self, parent, id):
        wxHtmlWindow.__init__(self, parent, id)
        self.parent = parent

    def OnSetTitle(self, title):
        self.parent.ShowTitle(title)


class ManualHtmlPanel(wxPanel):
    def __init__(self, parent, frame):
        wxPanel.__init__(self, parent, -1)
        self.frame = frame
        # CHANGED CODE Haywood 26/2/02
        # get base directory for manuals from broker
        # Ideally this should be something like "/usr/doc/gnumed/"
        self.docdir = gmGuiBroker.GuiBroker ()['gnumed_dir']
        self.printer = wxHtmlEasyPrinting()

        self.box = wxBoxSizer(wxVERTICAL)

        infobox = wxBoxSizer(wxHORIZONTAL)
        n = wxNewId()
        self.infoline = wxTextCtrl(self, n, style=wxTE_READONLY)
        self.infoline.SetBackgroundColour(wxLIGHT_GREY)
        infobox.Add(self.infoline, 1, wxGROW|wxALL)
        self.box.Add(infobox, 0, wxGROW)

        self.html = ManualHtmlWindow(self, -1)
        self.html.SetRelatedFrame(frame, "")
        self.html.SetRelatedStatusBar(0)
        self.box.Add(self.html, 1, wxGROW)

        self.SetSizer(self.box)
        self.SetAutoLayout(true)

        self.OnShowDefault(None)

##     def __del__(self):
##         print 'ManualHtmlPanel.__del__'

    def ShowTitle(self, title):
        self.infoline.Clear()
        self.infoline.WriteText(title)

    def OnShowDefault(self, event):
        name = os.path.join(self.docdir, manual_path)
        if os.access (name, os.F_OK):
            self.html.LoadPage(name)
        else:
            gmLog.gmDefLog.Log (gmLog.lErr, "cannot load document %s" % name)


    def OnLoadFile(self, event):
        dlg = wxFileDialog(self, wildcard = '*.htm*', style=wxOPEN)
        if dlg.ShowModal():
            path = dlg.GetPath()
            self.html.LoadPage(path)
        dlg.Destroy()


    def OnBack(self, event):
        if not self.html.HistoryBack():
            gmLog.gmDefLog.Log (gmLog.lInfo, _("ManualHtmlWindow: No more items in history!\n"))


    def OnForward(self, event):
        if not self.html.HistoryForward():
            gmLog.gmDefLog.Log (gmLog.lInfo, _("ManualHtmlWindow: No more items in history!\n"))


    def OnViewSource(self, event):
        from wxPython.lib.dialogs import wxScrolledMessageDialog
        source = self.html.GetParser().GetSource()
        dlg = wxScrolledMessageDialog(self, source, _('HTML Source'))
        dlg.ShowModal()
        dlg.Destroy()


    def OnPrint(self, event):
        self.printer.PrintFile(self.html.GetOpenedPage())


class gmManual (gmPlugin.wxNotebookPlugin):
    """
    Plugin to encapsulate the manual window
    """
    def name (self):
        return 'Manual'

    def MenuInfo (self):
        return ('help', '&Manual')

    def GetWidget (self, parent):
        return ManualHtmlPanel (parent, self.gb['main.frame'])

    def DoToolbar (self, tb, widget):
	tool1 = tb.AddTool(ID_MANUALCONTENTS, images_for_gnumed_browser16_16.getcontentsBitmap(),
			   shortHelpString="Gnumed Manual Contents", isToggle=true)
	EVT_TOOL (tb, ID_MANUALCONTENTS, widget.OnShowDefault)
      	tool1 = tb.AddTool(ID_MANUALOPENFILE, images_for_gnumed_browser16_16.getfileopenBitmap(),
				shortHelpString="Open File", isToggle=true)
	EVT_TOOL (tb, ID_MANUALOPENFILE, widget.OnLoadFile)
	tool1 = tb.AddTool(ID_MANUALBACK, images_for_gnumed_browser16_16.get1leftarrowBitmap(),
				shortHelpString="Back", isToggle=false)
	EVT_TOOL (tb, ID_MANUALBACK, widget.OnBack)
	tool1 = tb.AddTool(ID_MANUALFORWARD, images_for_gnumed_browser16_16.get1rightarrowBitmap(),
				shortHelpString="Forward", isToggle=true)
	EVT_TOOL (tb, ID_MANUALFORWARD, widget.OnForward)
	tool1 = tb.AddTool(ID_MANUALRELOAD, images_for_gnumed_browser16_16.getreloadBitmap(),
				shortHelpString="Re-load", isToggle=true)
	tb.AddSeparator()
	tool1 = tb.AddTool(ID_MANUALHOME, images_for_gnumed_browser16_16.getgohomeBitmap(),
				shortHelpString="Home", isToggle=true)
	EVT_TOOL (tb, ID_MANUALHOME, widget.OnShowDefault)
	tb.AddSeparator()
	tool1 = tb.AddTool(ID_MANUALBABELFISH, images_for_gnumed_browser16_16.getbabelfishBitmap(),
				shortHelpString="Translate text", isToggle=false)
	#EVT_TOOL (tb, ID_MANUALBABELFISH, widget.OnBabelFish )
	tb.AddSeparator()
	tool1 = tb.AddTool(ID_MANUALBOOKMARKS, images_for_gnumed_browser16_16.getbookmarkBitmap(),
				shortHelpString="Bookmarks", isToggle=true)
	#EVT_TOOL (tb, ID_MANUALBOOKMARKS, widget.OnBookmarks)
	tool1 = tb.AddTool(ID_MANUALADDBOOKMARK, images_for_gnumed_browser16_16.getbookmark_addBitmap(),
				shortHelpString="Add Bookmark", isToggle=true)
	#EVT_TOOL (tb, ID_MANUALADDBOOKMARK, widget.OnAddBookmark)
	tool1 = tb.AddTool(ID_VIEWSOURCE, images_for_gnumed_browser16_16.getviewsourceBitmap(),
				shortHelpString="View Source", isToggle=true)
	EVT_TOOL (tb, ID_VIEWSOURCE, widget.OnViewSource)
	tool1=tb.AddTool(ID_MANUALPRINTER, images_for_gnumed_browser16_16.getprinterBitmap(),
				shortHelpString="Print Page", isToggle=true)
	EVT_TOOL (tb, ID_MANUALPRINTER, widget.OnPrint)	
