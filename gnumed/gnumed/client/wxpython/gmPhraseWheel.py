"""
A class, extending wxTextCtrl, which has a drop-down pick list,
automatically filled based on the inital letters typed. Based on the
interface of Richard Terry's Visual Basic client

This is based on seminal work by Ian Haywood <ihaywood@gnu.org>
"""
#@copyright: GPL

############################################################################
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmPhraseWheel.py,v $
# $Id: gmPhraseWheel.py,v 1.29 2003-11-19 23:42:00 ncq Exp $
__version__ = "$Revision: 1.29 $"
__author__  = "K.Hilbert <Karsten.Hilbert@gmx.net>, I.Haywood, S.J.Tan <sjtan@bigpond.com>"

import string, types, time, sys, re

if __name__ == "__main__":
	sys.path.append ("../python-common/")

import gmLog
_log = gmLog.gmDefLog
if __name__ == "__main__":
	_log.SetAllLogLevels(gmLog.lData)

import gmExceptions, gmPG, gmMatchProvider

from wxPython.wx import *

_true = (1==1)
_false = (1==0)

#============================================================
class cWheelTimer(wxTimer):
	"""Timer for delayed fetching of matches.

	It would be quite useful to tune the delay
	according to current network speed either at
	application startup or even during runtime.

	No logging in here as this should be as fast as possible.
	"""
	def __init__(self, aCallback = None, aDelay = 300):
		"""Set up our timer with reasonable defaults.

		- delay default is 300ms as per Richard Terry's experience
		- delay should be tailored to network speed/user speed
		"""
		# sanity check
		if aCallback is None:
			_log.Log(gmLog.lErr, "No use setting up a timer without a callback function.")
			return None
		else:
			self.__callback = aCallback
		self.__delay = aDelay
		wxTimer.__init__(self)

	def Notify(self):
		self.__callback()
#============================================================
class cPickList(wxListBox):
	def __init__(self, parent, id = -1):
		wxListBox.__init__(self, parent, -1, style=wxLB_SINGLE | wxLB_NEEDED_SB)
#============================================================
class cPickListWin(wxWindow):
	def __init__(self, *kwds, **kwargs):
		wxWindow.__init__(self, *kwds, **kwargs)
		self.panel = wxPanel(self, -1)
		self._picklist = cPickList(self.panel)
#============================================================
class cPhraseWheel (wxTextCtrl):
	"""Widget for smart guessing of user fields, after Richard Terry's interface."""

	default_phrase_separators = re.compile('[;/|]+')

	def __init__ (
		self,
		aMatchProvider = None,
		aDelay = 300,
		selection_only = _false,
		*args,
		**kwargs):

		if not isinstance(aMatchProvider, gmMatchProvider.cMatchProvider):
			_log.Log(gmLog.lErr, "aMatchProvider must be a match provider object")
			return None
		self.__matcher = aMatchProvider
		self.__real_matcher = None
		
		self.__currMatches = []
		self.phrase_separators = cPhraseWheel.default_phrase_separators
		self.__timer = cWheelTimer(self._on_timer_fired, aDelay)
		self.allow_multiple_phrases()
		self.relevant_input = ''
		self.data = None
		self.input_was_selected = _false
		self.selection_only = selection_only
		self._has_focus = _false

		self.listener_callbacks = []
		self.notified_listeners = _false

		if kwargs.has_key('id_callback'):
			self.addCallback(kwargs['id_callback'])
			del kwargs['id_callback']

		wxTextCtrl.__init__ (self, *args, **kwargs)
		# unnecessary as we are using styles
		#self.SetBackgroundColour (wxColour (200, 100, 100))

		# set event handlers
		# 1) entered text changed
		EVT_TEXT (self, self.GetId(), self.__on_text_update)
		# - user pressed <enter>
		EVT_TEXT_ENTER	(self, self.GetId(), self.__on_enter)
		# 2) a key was pressed
		EVT_KEY_DOWN (self, self.__on_key_pressed)
		# 3) evil user wants to resize widget
		EVT_SIZE (self, self.on_resize)
		EVT_SET_FOCUS (self, self.on_set_focus)
		EVT_KILL_FOCUS (self, self.on_kill_focus)

		tmp = kwargs.copy()
		width, height = kwargs['size']
		x, y = kwargs['pos']
		tmp['pos'] = (x, y + height)
		tmp['size'] = (width, height*6)
		tmp['id'] = -1
		self.__picklist_win = wxWindow(*args, **tmp)
		self.panel = wxPanel(self.__picklist_win, -1)
		self._picklist = wxListBox(self.panel, -1, style=wxLB_SINGLE | wxLB_NEEDED_SB)
		self._picklist.Clear()
		self.__picklist_win.Hide ()
		self.__picklist_visible = _false

		self.left_part = ''
		self.right_part = ''
	#--------------------------------------------------------
	def allow_multiple_phrases(self, state = _true):
		self.__handle_multiple_phrases = state
	#-------------------------------------------------------
	def addCallback (self, callback_func):
		"""Add a callback for a listener.

		The callback will be invoked whenever an item is selected
		from the picklist. The associated data is passed in as
		a single parameter. Callbacks must be able to cope with
		None as the data parameter as that is sent whenever the
		user changes a previously selected value.
		"""
		self.listener_callbacks.append(callback_func)
	#--------------------------------------------------------
	def getData (self):
		return self.data
	#--------------------------------------------------------
	def setContext (self, context, val):
		if self.__real_matcher:
			# forget any caching, as it's now invalid
			self.__matcher = self.__real_matcher
			self.__real_matcher = None
		self.__matcher.setContext (context, val)
	#---------------------------------------------------------
#	def snap (self):
#		"""
#		This is called when the context is rich enough that
#		it is likely matching will return one or only
#		a few values. If there is only one value,
#		the phrasewheel will 'snap' to that value
#		"""
#		if self.__real_matcher:
			# this should never happen, just in case
#			self.__matcher = self.__real_matcher
#			self.__real_matcher = None
#		matches = self.__matcher.getAllMatches ()
#		if len (matches) == 1:
#			self.data = matches[0]['data']
#			self.SetValue (matches[0]['label'])
#			self.input_was_selected = _true
#			for notify_listener in self.listener_callbacks:
				# get data associated with selected item
#				notify_listener(self.data)
#			self.notified_listeners = 1
#		if len (matches) > 1:
			# cache these results
#			self.__real_matcher = self.__matcher
#			self.__matcher = gmMatchProvider.cMatchProvider_FixedList(matches)
	#---------------------------------------------------------
	def setNextFocus (self, aWidget):
		"""
		sets the next widget that recieves the focus
		Can be any object with a method SetFocus ()
		"""
		self.addCallback (lambda x: x and aWidget.SetFocus ()) 
	#--------------------------------------------------------
	def setDependent (self, wheel, context_var):
		"""
		Convience function to make one phrasewheel's match context
		dependent upon another's value
		"""
		self.addCallback (lambda x: wheel.setContext (context_var, x))
	#---------------------------------------------------------------------
	def _updateMatches(self):
		"""Get the matches for the currently typed input fragment."""

		# get current(ly relevant part of) input
		if self.__handle_multiple_phrases:
			entire_input = self.GetValue()
#			print "---------------------"
#			print "phrase wheel content:", entire_input
			cursor_pos = self.GetInsertionPoint()
#			print "cursor at position:", cursor_pos
			left_of_cursor = entire_input[:cursor_pos]
			right_of_cursor = entire_input[cursor_pos:]
#			print "cursor in input: %s>>>CURSOR<<<%s" % (left_of_cursor, right_of_cursor)
				# find last phrase separator before cursor position
			left_boundary = self.phrase_separators.search(left_of_cursor)
			if left_boundary is not None:
#				print "left boundary span:", left_boundary.span()
				phrase_start = left_boundary.end()
			else:
				phrase_start = 0
			self.left_part = entire_input[:phrase_start]
#			print "phrase start:", phrase_start
			# find next phrase separator after cursor position
			right_boundary = self.phrase_separators.search(right_of_cursor)
			if right_boundary is not None:
#				print "right boundary span:", right_boundary.span()
				phrase_end = cursor_pos + (right_boundary.start() - 1)
			else:
				phrase_end = len(entire_input) - 1
			self.right_part = entire_input[phrase_end+1:]
#			print "phrase end:", phrase_end

			self.relevant_input = entire_input[phrase_start:phrase_end+1]
		else:
			self.relevant_input = self.GetValue()
#		print "relevant input:", self.relevant_input

		# get all currently matching items
		(matched, self.__currMatches) = self.__matcher.getMatches(self.relevant_input)
		# and refill our picklist with them
		self._picklist.Clear()
		if matched:
			for item in self.__currMatches:
				self._picklist.Append(item['label'], clientData = item['data'])
	#--------------------------------------------------------
	def __show_picklist(self):
		"""Display the pick list."""

		# this helps if the current input was already selected from the
		# list but still is the substring of another pick list item
		if self.input_was_selected:
			return 1

		if not self._has_focus:
			return 1

		# if only one match and text == match
		if len(self.__currMatches) == 1:
			if self.__currMatches[0]['label'] == self.relevant_input:
				# don't display drop down list
				self._hide_picklist()
				return 1

		# recalculate position
		# FiXME: check for number of entries - shrink list windows
		(x,y) = self.ClientToScreenXY(0,0)
		win = self
		while not win.IsTopLevel():
			win = win.GetParent()
		(toplevel_x, toplevel_y) = win.ClientToScreenXY(0,0)

		dim = self.GetSize()
		self.__picklist_win.MoveXY(x - toplevel_x, y - toplevel_y + dim.height)

		# select first value
		self._picklist.SetSelection(0)

		# remember that we have a list window
		self.__picklist_visible = _true

		# and show it
		# FIXME: we should _update_ the list window instead of redisplaying it
		self.__picklist_win.Show()
		self._picklist.Show()
	#--------------------------------------------------------
	def _hide_picklist(self):
		"""Hide the pick list."""
		if self.__picklist_visible:
			self.__picklist_win.Hide()		# dismiss the dropdown list window
		self.__picklist_visible = _false
	#--------------------------------------------------------
	# specific event handlers
	#--------------------------------------------------------
	def on_list_item_selected (self):
		"""Gets called when user selected a list item."""
		self._hide_picklist()

		# update our display
		selection_idx = self._picklist.GetSelection()
		if self.__handle_multiple_phrases:
			self.SetValue('%s%s%s' % (self.left_part, self._picklist.GetString(selection_idx), self.right_part))
		else:
			self.SetValue(self._picklist.GetString(selection_idx))

		# get data associated with selected item
		self.data = self._picklist.GetClientData(selection_idx)
		# and tell the listeners about the user's selection
		for call_listener in self.listener_callbacks:
			call_listener(self.data)
		# remember that we did so
		self.notified_listeners = 1
		# remember that the current value was selected from the list
		self.input_was_selected = _true
	#--------------------------------------------------------
	# individual key handlers
	#--------------------------------------------------------
	def __on_enter (self):
		"""Called when the user pressed <ENTER>.

		FIXME: this might be exploitable for some nice statistics ...
		"""
		# if we have a pick list
		if self.__picklist_visible:
			# tell the input field about it
			self.on_list_item_selected()
	#--------------------------------------------------------
	def __on_down_arrow(self, key):
		# if we already have a pick list go to next item
		if self.__picklist_visible:
#			self._picklist.ProcessEvent (key)
			selected = self._picklist.GetSelection()
			if selected < (len(self.__currMatches) - 1):
				self._picklist.SetSelection(selected+1)

		# if we don't yet have a pick list
		# - open new pick list
		# (this can happen when we TAB into a field pre-filled
		#  with the top-weighted contextual data but want to
		#  select another contextual item)
		else:
			# don't need timer anymore since user explicitely requested list
			self.__timer.Stop()
			# update matches according to current input
			self._updateMatches()
			# if we do have matches now show list
			if len(self.__currMatches) > 0:
				self.__show_picklist()
	#--------------------------------------------------------
	def __on_up_arrow(self, key):
		if self.__picklist_visible:
			selected = self._picklist.GetSelection()
			# select previous item if available
			if selected > 0:
				self._picklist.SetSelection(selected-1)
			else:
				# FIXME: return to input field and close pick list ?
				pass
		else:
			# FIXME: input history ?
			pass
	#--------------------------------------------------------
	# event handlers
	#--------------------------------------------------------
	def __on_key_pressed (self, key):
		"""Is called when a key is pressed."""
		key.Skip()

		# user moved down
		if key.GetKeyCode() == WXK_DOWN:
			self.__on_down_arrow(key)
			return
		# user moved up
		if key.GetKeyCode() == WXK_UP:
			self.__on_up_arrow(key)
			return

		# FIXME: need PAGE UP/DOWN//POS1/END here

		# user pressed <ENTER>
		if key.GetKeyCode() == WXK_RETURN:
			self.__on_enter()
			return
	#--------------------------------------------------------
	def __on_text_update (self, event):
		"""Internal handler for EVT_TEXT (called when text has changed)"""

		# dirty "selected" flag
		self.input_was_selected = _false

		# if empty string then kill list dropdown window
		# we also don't need a timer event then
		if len(self.GetValue()) == 0:
			self._hide_picklist()
			self.__timer.Stop()
		else:
			# start timer for delayed match retrieval
			self.__timer.Start(oneShot = _true)

		if self.notified_listeners:
			# Aargh! we told the listeners that we selected "foo"
			# but now the user is typing again !
			self.data = None
			for notify_listener in self.listener_callbacks:
				notify_listener(None)
			self.notified_listeners = _false
	#--------------------------------------------------------
	def on_resize (self, event):
		sz = self.GetSize()
		rows = len (self.__currMatches)
		if rows == 0:
			rows = 1
		if rows > 10:
			rows = 10
		self._picklist.SetSize ((sz.width, sz.height*rows))
		# as wide as the textctrl, and 6 times the height
		self.panel.SetSize (self._picklist.GetSize ())
		self.__picklist_win.SetSize (self.panel.GetSize())
	#--------------------------------------------------------
	def _on_timer_fired (self):
		"""Callback for delayed match retrieval timer.

		if we end up here:
		 - delay has passed without user input
		 - the value in the input field has not changed since the timer started
		"""
		# update matches according to current input
		self._updateMatches()
		# we now have either:
		# - all possible items (within reasonable limits) if input was '*'
		# - all matching items
		# - an empty match list if no matches were found
		# also, our picklist is refilled and sorted according to weight

		# display list - but only if we have more than one match
		if len(self.__currMatches) > 0:
			# show it
			self.on_resize (None)
			self.__show_picklist()
		else:
			# we may have had a pick list window so we
			# need to dismiss that since we don't have
			# more than one item anymore
			self._hide_picklist()
	#--------------------------------------------------------
	def on_set_focus(self, event):
		self._has_focus = _true
		event.Skip()
	#--------------------------------------------------------
	def on_kill_focus(self, event):
		# don't need timer and pick list anymore
		self.__timer.Stop()
		self._hide_picklist()
		# don't allow invalid input
		if self.selection_only:
			if not self.input_was_selected:
				# FIXME: if len(matches) == 1 -> select
				self.Clear()
		self._has_focus = _false
		event.Skip()
#--------------------------------------------------------
# MAIN
#--------------------------------------------------------
if __name__ == '__main__':
	import gmI18N
	#----------------------------------------------------
	def clicked (data):
		print "Selected :%s" % data
	#----------------------------------------------------
	class TestApp (wxApp):
		def OnInit (self):

			frame = wxFrame (
				None,
				-4,
				"phrase wheel test for GNUmed",
				size=wxSize(300, 350),
				style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE
			)

			items = [	{'data':1, 'label':"Bloggs", 	'weight':5},
						{'data':2, 'label':"Baker",  	'weight':4},
						{'data':3, 'label':"Jones",  	'weight':3},
						{'data':4, 'label':"Judson", 	'weight':2},
						{'data':5, 'label':"Jacobs", 	'weight':1},
						{'data':6, 'label':"Judson-Jacobs",'weight':5}
					]
			mp1 = gmMatchProvider.cMatchProvider_FixedList(items)
			# do NOT treat "-" as a word separator here as there are names like "asa-sismussen"
			mp1.setWordSeparators(separators = '[ \t=+&:@]+')
			ww1 = cPhraseWheel(
				parent = frame,
				id = -1,
				#id_callback = clicked,
				pos = (50, 50),
				size = (180, 30),
				aMatchProvider = mp1
			)
			ww1.on_resize (None)

			print "Do you want to test the database connected phrase wheel ?"
			yes_no = raw_input('y/n: ')
			if yes_no == 'y':
				src = {
					'service': 'default',
					'table': 'gmpw_sql_test',
					'column': 'phrase',
					'limit': 25
				}
				score = {
					'service': 'default',
					'table': 'score_gmpw_sql_test',
					'column': 'fk_gmpw_sql_test'
				}
				mp2 = cMatchProvider_SQL([src], score)
				ww2 = cPhraseWheel(
					parent = frame,
					id = -1,
					pos = (50, 250),
					size = (180, 30),
					aMatchProvider = mp2
				)
				ww2.on_resize (None)

			frame.Show (1)
			return 1
	#--------------------------------------------------------
	app = TestApp ()
	app.MainLoop ()

#==================================================
# $Log: gmPhraseWheel.py,v $
# Revision 1.29  2003-11-19 23:42:00  ncq
# - cleanup, comment out snap()
#
# Revision 1.28  2003/11/18 23:17:47  ncq
# - cleanup, fixed variable names
#
# Revision 1.27  2003/11/17 10:56:38  sjtan
#
# synced and commiting.
#
# Revision 1.26  2003/11/09 14:28:30  ncq
# - cleanup
#
# Revision 1.25  2003/11/09 02:24:42  ncq
# - added Syans "input was selected from list" state flag to avoid unnecessary list
#   drop downs
# - variable name cleanup
#
# Revision 1.24  2003/11/07 20:48:04  ncq
# - place comments where they belong
#
# Revision 1.23  2003/11/05 22:21:06  sjtan
#
# let's gmDateInput specify id_callback in constructor list.
#
# Revision 1.22  2003/11/04 10:35:23  ihaywood
# match providers in gmDemographicRecord
#
# Revision 1.21  2003/11/04 01:40:27  ihaywood
# match providers moved to python-common
#
# Revision 1.20  2003/10/26 11:27:10  ihaywood
# gmPatient is now the "patient stub", all demographics stuff in gmDemographics.
#
# Ergregious breakages are fixed, but needs more work
#
# Revision 1.19  2003/10/09 15:45:16  ncq
# - validate cookie column in score tables, too
#
# Revision 1.18  2003/10/07 22:20:50  ncq
# - ported Syan's extra_sql_condition extension
# - make SQL match provider aware of separate scoring tables
#
# Revision 1.17  2003/10/03 00:20:25  ncq
# - handle case where matches = 1 and match = input -> don't show picklist
#
# Revision 1.16  2003/10/02 20:51:12  ncq
# - add alt-XX shortcuts, move __* to _*
#
# Revision 1.15  2003/09/30 18:52:40  ncq
# - factored out date input wheel
#
# Revision 1.14  2003/09/29 23:11:58  ncq
# - add __explicit_offset() date expander
#
# Revision 1.13  2003/09/29 00:16:55  ncq
# - added date match provider
#
# Revision 1.12  2003/09/21 10:55:04  ncq
# - coalesce merge conflicts due to optional SQL phrase wheel testing
#
# Revision 1.11  2003/09/21 07:52:57  ihaywood
# those bloody umlauts killed by python interpreter!
#
# Revision 1.10  2003/09/17 05:54:32  ihaywood
# phrasewheel box size now approximate to length of search results
#
# Revision 1.8  2003/09/16 22:25:45  ncq
# - cleanup
# - added first draft of single-column-per-table SQL match provider
# - added module test for SQL matcher
#
# Revision 1.7  2003/09/15 16:05:30  ncq
# - allow several phrases to be typed in and only try to match
#   the one the cursor is in at the moment
#
# Revision 1.6  2003/09/13 17:46:29  ncq
# - pattern match word separators
# - pattern match ignore characters as per Richard's suggestion
# - start work on phrase separator pattern matching with extraction of
#   relevant input part (where the cursor is at currently)
#
# Revision 1.5  2003/09/10 01:50:25  ncq
# - cleanup
#
#
#==================================================

#----------------------------------------------------------
# ideas
#----------------------------------------------------------
#- display possible completion but highlighted for deletion
#(- cycle through possible completions)
#- pre-fill selection with SELECT ... LIMIT 25
#- weighing by incrementing counter - if rollover, reset all counters to percentage of self.value()
#- ageing of item weight
#- async threads for match retrieval instead of timer
#  - on truncated results return item "..." -> selection forcefully retrieves all matches

#- plugin for pattern matching/validation of input

#- generators/yield()
#- OnChar() - process a char event

# split input into words and match components against known phrases
# -> accumulate weights into total item weight

# - case insensitive by default but
# - make case sensitive matching possible
#   - if no matches found revert to case _insensitive_ matching
# - maybe _sensitive_ by default + auto-revert if too few matches ?

# make special list window:
# - deletion of items
# - highlight matched parts
# - faster scrolling
# - wxEditableListBox ?

# - press down only once to get into list
# - moving between list members is too slow

# - if non-learning (i.e. fast select only): autocomplete with match
#   and move cursor to end of match
#-----------------------------------------------------------------------------------------------
# darn ! this clever hack won't work since we may have crossed a search location threshold
#----
#	#self.__prevFragment = "XXXXXXXXXXXXXXXXXX-very-unlikely--------------XXXXXXXXXXXXXXX"
#	#self.__prevMatches = []		# a list of tuples (ID, listbox name, weight)
#
#	# is the current fragment just a longer version of the previous fragment ?
#	if string.find(aFragment, self.__prevFragment) == 0:
#	    # we then need to search in the previous matches only
#	    for prevMatch in self.__prevMatches:
#		if string.find(prevMatch[1], aFragment) == 0:
#		    matches.append(prevMatch)
#	    # remember current matches
#	    self.__prefMatches = matches
#	    # no matches found
#	    if len(matches) == 0:
#		return [(1,_('*no matching items found*'),1)]
#	    else:
#		return matches
#----
#TODO:
# - see spincontrol for list box handling
# stop list (list of negatives): "an" -> "animal" but not "and"

# maybe store fixed list matches as balanced tree if otherwise to slow
#-----
#> > remember, you should be searching on  either weighted data, or in some
#> > situations a start string search on indexed data
#>
#> Can you be a bit more specific on this ?

#seaching ones own previous text entered  would usually be instring but
#weighted (ie the phrases you use the most auto filter to the top)

#Searching a drug database for a   drug brand name is usually more
#functional if it does a start string search, not an instring search which is
#much slower and usually unecesary.  There are many other examples but trust
#me one needs both
#-----
