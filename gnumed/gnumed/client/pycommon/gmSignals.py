"""gmSignals - factory functions returning GnuMed internal signal strings. 

This helps to avoid that  simple typographic mistakes result in messages
not being dispatched. It would allow to do messenging house keeping as well.

@copyright: author
@license: GPL (details at http://www.gnu.org)
"""
# This source code is protected by the GPL licensing scheme.
# Details regarding the GPL are available at http://www.gnu.org
# You may use and share it as long as you don't deny this right
# to anybody else.
#=============================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/pycommon/Attic/gmSignals.py,v $
__version__ = "$Revision: 1.20 $"
__author__  = "H. Herb <hherb@gnumed.net>"


import inspect, os

def getimporter():
    """ Placing this inside a module X, return a 7-tuple representing
        the module that is importing X:

        ( modulename,  frame, filepath, lineno, name, codetext, somenumber )

        The items starting from the 2nd one are the 6-tuple frame info.
        For example, when a file 'importer.py' imports a module 'imported.py'
        in which this function "getimporter" is placed, getimporter will
        report:

        ('importer',
        <frame object at 0x014C7A80>, 'E:\\py\\src\\importer.py',
        2, 'importer', ['import imported\n'], 0)        

        This function is useful when users intend to do different things
        with a module X according to the properties/attributes of a module
        that is importing X. That is, an 'importer-specific 
        module initialization'.
        
        Usage:
        ------
        
        importer = getimporter()
        if importer[0] == 'mytools': (do something)
        else: (do something else)

        or, it might be helpful in avoiding recursive importing:

        importer = getimporter()
        if importer[0] == 'mytools': import some module
        else: import another module
        
        How it works:
        -------------

        The inspect.stack() returns a list of 6-tuples for the execution
        stack. Each 6-tuple is a frame info:

        (frame, filepath, lineno, name, codetext, somenumber)

        When an inspect.stack() is placed in a module X, and X is
        imported by Y, then one of the 6-tuples will look like:        
        
        info= (<frame object at 0x00BA04A0>, 'C:\\pan\\py\\src\\Y.py',
        2, '?', ['import X\n'], 0)

        in which the 1st item of the info[4] is a string starting with
        either 'import X' or 'from X' or ' import pantools.X' or
        ' from pantools.X'. This will serve as the criteria for finding Y.
    """

    # First find the name of module containing this (getimporter)
    frame, path, lineno, name, codetext, somenumber= inspect.stack()[1]
    module =  os.path.split(path)[1].split('.')[0]   # get the module name only
    
    # Then get the calling stack       
    for frame, file, lineno, name, codetext, somenumber in inspect.stack():
        codetexts = codetext[0].split() # The first will be either 'from' or 'import'

        # Possibilities:
        #
        # import X
        # form   X import blah
        # import tools.X
        # from   tools.X import blah
        
        if codetexts[0] in ('from', 'import') and \
           codetexts[1].split('.')[-1] == module:
            name = os.path.split(file)[1].split('.')[0]
            return name, frame, file, lineno, name, codetext, somenumber
    return (None, )

print "*** gmSignals.py deprecated ***"
print "imported by:", getimporter()
print ""


#=============================================================
def popup_notice():
	"a notice of general interest has been received"
	return 'popup_notice'

def popup_alert():
	"an important notice of general ineterest has been received"
	return 'popup_alert'

#-------------------------------------------------------------
# clinical signals
#-------------------------------------------------------------
# vaccinations
def vacc_mod_db():
	"""table vaccination"""
	return 'vacc_mod_db'

def vaccinations_updated():
	"""Announce vaccination cache update to interested parties."""
	return 'vaccinations_updated'

#------------------------------------------
def health_issue_change_db():
	"""Announce health issue row insert/update/delete in backend.

	- there's only very few health issue rows per patient and they
	  are rarely accessed so efficiency does not make it necessary to
	  have separate signals for insert/delete and update
	"""
	return 'health_issue_change_db'

def health_issue_updated():
	"""Announce health issue cache update within frontend."""
	return 'health_issue_updated'

#------------------------------------------
def episode_change_db():
	"""Announce episode row insert/update/delete in backend.

	- there's only a few episode rows per patient and they
	  are rarely accessed so efficiency does not make it necessary to
	  have separate signals for insert/delete and update
	"""
	return 'episode_change_db'

def episodes_modified():
	"""Announce episode cache update within frontend."""
	return 'episodes_modified'

#------------------------------------------
def item_change_db():
	"""Backend modification to clin_root_item.

	- directly or indirectly
	- the actual signal name is appended with the relevant patient ID
	"""
	return 'item_change_db'

def clin_history_updated():
	"""Frontend signal for clin_history  update."""
	return "clin_history_updated"

def clin_item_updated():
	"""Frontend signal for clin_root_item cache update."""
	return 'clin_item_updated'
#-------------------------------------------------------------
# patient_locked, patient_unlocked

def pre_patient_selection():
	"""the currently active patient is about to be changed"""
	return 'pre_patient_selection'

def post_patient_selection():
	"""another patient has been selected to be the currently active patient"""
	return 'post_patient_selection'

def patient_modified():
	"the current patients demographic data has been modified"
	return 'patient_modified'
	
def medication_modified():
	"the current patient's medication has been modified"
	return 'medication_modified'
#-------------------------------------------------------------
def waitingroom_added():
	"a patient has been added to the waiting room"
	return 'waitingroom_added'
	
def waitingroom_incons():
	"a patient has started his consultation with the doctor"
	return 'waitingroom_incons'
	
def waitingroom_left():
	"a aptient has left the waiting room, finished his consultation"
	return 'waitingroom_left'

#-------------------------------------------------------------
def application_closing():
	"""The main application is intentionally closing down."""
	return "application_closing"

def application_init():
	"an application is starting"
	return "application_init"
#-------------------------------------------------------------
def user_error ():
	"an error of interest to the user"
	return "user_error"

def new_notebook ():
	"""a new notebook page creation event
It should carry a dictionary:
- name: the unique name (for unloading)
- widget: the wxWindow to display
- label: the notebook label
- icon: the notebook icon (which may or may not be used, can be None)
	"""
	return "new_notebook"

def unload_plugin ():
	"""
	Requested that the named plugin be unloaded
	- name: the plugin name
	"""
	return "unload_notebook"

def display_plugin ():
	"""
	Requested that the named plugin be displayed
	- name: the unique name of the plugin

	If the plugin doesn't want to be displayed, it should listen for this event and
	return the string 'veto'
	"""
	return "display_plugin"


def wish_display_plugin ():
	"""
	This event expressed the desire that a plugin be displayed
	I.e the plugin manger *receives* this event, it generates the above
	- name: plugin unique name
	"""
	return "wish_display_plugin"

def search_result ():
	"""
	The results of a patient search
	- ids: a list of gmPerson.cIdentity objects
	- display_fields: a list of fields to display
	"""
	return "search_result"


def pg_users_changed():
	"""
		when the pg_user list is modified , or a user perms changed
	
	"""
	return "pg_users_changed" 

def provider_identity_selected():
	"""
		when a provider selection widget selects a existing potential identity provider 
	"""
	return "provider_identity_selected"
#=============================================================	
if __name__ == "__main__":

	import gmDispatcher
	
	def callback(id):
		print "\nSignal received, id = %s" % str(id)
		
	class TestWidget:
		def __init__(self):
			gmDispatcher.connect(self.Update, patient_selected())
		def Update(self, id):
			print "widget updates itself with id=%s" % str(id)
		
	the_id =100
	print "Registering interest in signal %s" % popup_notice()
	gmDispatcher.connect(callback, popup_notice())
	print "Sending signal %s with parameter %d" % (popup_notice(), the_id)
	gmDispatcher.send(popup_notice(), id=the_id)
	print "\nCreating an instance of a widget updating itself on signal %s" % patient_selected()
	tw = TestWidget()
	print "Sending signal %s with parameter %d" % (patient_selected(), the_id+1)
	gmDispatcher.send(patient_selected(), id=the_id+1)

#======================================================================
# $Log: gmSignals.py,v $
# Revision 1.20  2007-12-23 11:59:15  ncq
# - show importers
#
# Revision 1.19  2007/12/11 14:31:59  ncq
# - show depreciation warning
#
# Revision 1.18  2007/10/25 12:26:47  ncq
# - allergy signals are gone
#
# Revision 1.17  2007/08/12 00:06:38  ncq
# - remove signals that aren't used from here anymore
#
# Revision 1.16  2007/07/13 12:09:16  ncq
# - add comment
#
# Revision 1.15  2007/03/02 15:30:46  ncq
# - add statustext()
#
# Revision 1.14  2006/05/15 13:25:55  ncq
# - remove signals "activating_patient" and "patient_selected"
#
# Revision 1.13  2006/05/12 21:58:30  ncq
# - add display_widget() signal
#
# Revision 1.12  2006/01/18 14:16:01  sjtan
#
# extra signals for provider mgmt
#
# Revision 1.11  2005/09/11 17:29:16  ncq
# - pre/post_patient_selection() make much more sense than activating_patient()
#   and patient_selected()
#
# Revision 1.10  2005/05/06 15:29:47  ncq
# - cleanup
#
# Revision 1.9  2005/04/14 08:51:51  ncq
# - cIdentity has moved
#
# Revision 1.8  2005/02/23 19:39:37  ncq
# - episodes_updated -> episodes_modified
#
# Revision 1.7  2005/02/01 10:16:07  ihaywood
# refactoring of gmDemographicRecord and follow-on changes as discussed.
#
# gmTopPanel moves to gmHorstSpace
# gmRichardSpace added -- example code at present, haven't even run it myself
# (waiting on some icon .pngs from Richard)
#
# Revision 1.6  2005/01/31 20:25:37  ncq
# - add episode change signals
#
# Revision 1.5  2004/07/15 07:57:20  ihaywood
# This adds function-key bindings to select notebook tabs
# (Okay, it's a bit more than that, I've changed the interaction
# between gmGuiMain and gmPlugin to be event-based.)
#
# Oh, and SOAPTextCtrl allows Ctrl-Enter
#
# Revision 1.4  2004/05/22 11:48:16  ncq
# - allergy signal handling cleanup
#
# Revision 1.3  2004/03/28 11:50:16  ncq
# - cleanup
#
# Revision 1.2  2004/03/03 23:53:22  ihaywood
# GUI now supports external IDs,
# Demographics GUI now ALPHA (feature-complete w.r.t. version 1.0)
# but happy to consider cosmetic changes
#
# Revision 1.1  2004/02/25 09:30:13  ncq
# - moved here from python-common
#
# Revision 1.14  2003/12/29 16:33:59  uid66147
# - vaccinations related signals
#
# Revision 1.13  2003/12/02 01:59:19  ncq
# - cleanup, add vaccination_updated()
#
# Revision 1.12  2003/11/17 10:56:37  sjtan
#
# synced and commiting.
#
# Revision 1.4  2003/10/26 00:58:52  sjtan
#
# use pre-existing signalling
#
# Revision 1.3  2003/10/25 16:13:26  sjtan
#
# past history , can add  after selecting patient.
#
# Revision 1.2  2003/10/25 08:29:40  sjtan
#
# uses gmDispatcher to send new currentPatient objects to toplevel gmGP_ widgets. Proprosal to use
# yaml serializer to store editarea data in  narrative text field of clin_root_item until
# clin_root_item schema stabilizes.
#
# Revision 1.1  2003/10/23 06:02:39  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.11  2003/07/19 20:19:19  ncq
# - add clin_root_item signals
#
# Revision 1.10  2003/07/09 16:22:04  ncq
# - add health issue signals
#
# Revision 1.9  2003/06/25 22:47:23  ncq
# - added application_closing() (I seem to keep adding stuff Sian proposed earlier)
#
# Revision 1.8  2003/06/22 16:19:09  ncq
# - add pre-selection signal
#
# Revision 1.7  2003/05/01 15:01:42  ncq
# - add allergy signals
#
# Revision 1.6  2003/02/12 23:39:12  sjtan
#
# new signals for initialization and teardown of other modules less dependent on gui.
#
# Revision 1.5  2003/01/16 14:45:04  ncq
# - debianized
#
# Revision 1.4  2002/11/30 11:07:50  ncq
# - just a bit of cleanup
#
# Revision 1.3  2002/09/10 07:41:27  ncq
# - added changelog keyword
#
# @change log:
#	08.09.2002 hherb first draft, untested
