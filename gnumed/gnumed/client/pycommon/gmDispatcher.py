"""GnuMed client internal signal handling.

# this code has been written by Patrick O'Brien <pobrien@orbtech.com>
# downloaded from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/87056
"""
import exceptions
import types
import sys
import weakref
import traceback

connections = {}
senders = {}

_boundMethods = weakref.WeakKeyDictionary()
#=====================================================================
class _Any:
	pass

Any = _Any()
#=====================================================================
class DispatcherError(exceptions.Exception):
	def __init__(self, args=None):
		self.args = args
#=====================================================================
# external API
#---------------------------------------------------------------------
def connect(receiver, signal=Any, sender=Any, weak=1):
	"""Connect receiver to sender for signal.
	
	If sender is Any, receiver will receive signal from any sender.
	If signal is Any, receiver will receive any signal from sender.
	If sender is None, receiver will receive signal from anonymous.
	If signal is Any and sender is None, receiver will receive any 
		signal from anonymous.
	If signal is Any and sender is Any, receiver will receive any 
		signal from any sender.
	If weak is true, weak references will be used.
	
	ADDITIONAL gnumed specific documentation:
			this dispatcher is not designed with a gui single threaded event
			loop in mind.
			when connecting to a receiver that may eventually make calls to			gui objects	 such as wxWindows objects, it is highly recommended that any
	such calls be wrapped in wxCallAfter() e.g.
		def receiveSignal(self, **args):
				self._callsThatDoNotTriggerGuiUpdates()
				self.data = processArgs(args)
				wxCallAfter( self._callsThatTriggerGuiUpdates() )
		
		since it is likely data change occurs before the signalling,
		it would probably look more simply like:
		
		def receiveSignal(self, **args):
				wxCallAfter(self._updateUI() )
		
		def _updateUI(self):
				# your code that reads data
		
		Especially if the widget can get a reference to updated data through
		a global reference, such as via gmCurrentPatient.
"""
	if signal is None:
		raise DispatcherError, 'signal cannot be None'
	if signal is not Any:
		signal = str(signal)
	if weak: receiver = safeRef(receiver)
	senderkey = id(sender)
	signals = {}
	if connections.has_key(senderkey):
		signals = connections[senderkey]
	else:
		connections[senderkey] = signals
		# Keep track of senders for cleanup.
		if sender not in (None, Any):
			def remove(object, senderkey=senderkey):
				_removeSender(senderkey=senderkey)
			# Skip objects that can not be weakly referenced, which means
			# they won't be automatically cleaned up, but that's too bad.
			try:
				weakSender = weakref.ref(sender, remove)
				senders[senderkey] = weakSender
			except:
				pass
	receivers = []
	if signals.has_key(signal):
		receivers = signals[signal]
	else:
		signals[signal] = receivers
	try: receivers.remove(receiver)
	except ValueError: pass
	receivers.append(receiver)
#---------------------------------------------------------------------
def disconnect(receiver, signal=Any, sender=Any, weak=1):
	"""Disconnect receiver from sender for signal.
	
	Disconnecting is not required. The use of disconnect is the same as for
	connect, only in reverse. Think of it as undoing a previous connection."""
	if signal is None:
		raise DispatcherError, 'signal cannot be None'
	if signal is not Any:
		signal = str(signal)
	if weak: receiver = safeRef(receiver)
	senderkey = id(sender)
	try:
		receivers = connections[senderkey][signal]
	except KeyError:
		print 'DISPATCHER ERROR: no receivers for signal %s from sender %s' % (repr(signal), sender)
		return
	try:
		receivers.remove(receiver)
	except ValueError:
		print "DISPATCHER ERROR: receiver [%s] not connected to signal [%s] from [%s]" % (receiver, repr(signal), sender)
	_cleanupConnections(senderkey, signal)
#---------------------------------------------------------------------
def send(signal, sender=None, **kwds):
	"""Send signal from sender to all connected receivers.
	
	Return a list of tuple pairs [(receiver, response), ... ].
	If sender is None, signal is sent anonymously."""
	signal = str(signal)
	senderkey = id(sender)
	anykey = id(Any)
	# Get receivers that receive *this* signal from *this* sender.
	receivers = []
	try: receivers.extend(connections[senderkey][signal])
	except KeyError: pass
	# Add receivers that receive *any* signal from *this* sender.
	anyreceivers = []
	try: anyreceivers = connections[senderkey][Any]
	except KeyError: pass
	for receiver in anyreceivers:
		if receivers.count(receiver) == 0:
			receivers.append(receiver)
	# Add receivers that receive *this* signal from *any* sender.
	anyreceivers = []
	try: anyreceivers = connections[anykey][signal]
	except KeyError: pass
	for receiver in anyreceivers:
		if receivers.count(receiver) == 0:
			receivers.append(receiver)
	# Add receivers that receive *any* signal from *any* sender.
	anyreceivers = []
	try: anyreceivers = connections[anykey][Any]
	except KeyError: pass
	for receiver in anyreceivers:
		if receivers.count(receiver) == 0:
			receivers.append(receiver)
	# Call each receiver with whatever arguments it can accept.
	# Return a list of tuple pairs [(receiver, response), ... ].
	responses = []
	for receiver in receivers:
		if type(receiver) is weakref.ReferenceType \
		or isinstance(receiver, BoundMethodWeakref):
			# Dereference the weak reference.
			receiver = receiver()
			if receiver is None:
				# This receiver is dead, so skip it.
				continue
		try:
			response = _call(receiver, signal=signal, sender=sender, **kwds)
			responses += [(receiver, response)]
		except:
			# this seems such a fundamental error that it appears reasonable
			# to print directly to the console instead of making the whole
			# module depend on gmLog.py
			typ, val, tb = sys.exc_info()
			print 'DISPATCHER ERROR: %s <%s>' % (typ, val)
			print 'DISPATCHER ERROR: calling <%s> failed' % str(receiver)
			traceback.print_tb(tb)
	return responses
#---------------------------------------------------------------------
def safeRef(object):
	"""Return a *safe* weak reference to a callable object."""
	if hasattr(object, 'im_self'):
		if object.im_self is not None:
			# Turn a bound method into a BoundMethodWeakref instance.
			# Keep track of these instances for lookup by disconnect().
			selfkey = object.im_self
			funckey = object.im_func
			if not _boundMethods.has_key(selfkey):
				_boundMethods[selfkey] = weakref.WeakKeyDictionary()
			if not _boundMethods[selfkey].has_key(funckey):
				_boundMethods[selfkey][funckey] = \
				BoundMethodWeakref(boundMethod=object)
			return _boundMethods[selfkey][funckey]
	return weakref.ref(object, _removeReceiver)
#=====================================================================
class BoundMethodWeakref:
	"""BoundMethodWeakref class."""

	def __init__(self, boundMethod):
		"""Return a weak-reference-like instance for a bound method."""
		self.isDead = 0
		def remove(object, self=self):
			"""Set self.isDead to true when method or instance is destroyed."""
			self.isDead = 1
			_removeReceiver(receiver=self)
		self.weakSelf = weakref.ref(boundMethod.im_self, remove)
		self.weakFunc = weakref.ref(boundMethod.im_func, remove)
	#------------------------------------------------------------------
	def __repr__(self):
		"""Return the closest representation."""
		return repr(self.weakFunc)
	#------------------------------------------------------------------
	def __call__(self):
		"""Return a strong reference to the bound method."""
		if self.isDead:
			return None
		else:
			object = self.weakSelf()
			method = self.weakFunc().__name__
			return getattr(object, method)
#=====================================================================
# internal API
#---------------------------------------------------------------------
def _call(receiver, **kwds):
	"""Call receiver with only arguments it can accept."""
	if type(receiver) is types.InstanceType:
		# receiver is a class instance; assume it is callable.
		# Reassign receiver to the actual method that will be called.
		receiver = receiver.__call__
	if hasattr(receiver, 'im_func'):
		# receiver is a method. Drop the first argument, usually 'self'.
		fc = receiver.im_func.func_code
		acceptable = fc.co_varnames[1:fc.co_argcount]
	elif hasattr(receiver, 'func_code'):
		# receiver is a function.
		fc = receiver.func_code
		acceptable = fc.co_varnames[0:fc.co_argcount]
	else:
		print 'DISPATCHER ERROR: <%s> must be instance, method or function' % str(receiver)
	if not (fc.co_flags & 8):
		# fc does not have a **kwds type parameter, therefore 
		# remove unacceptable arguments.
		for arg in kwds.keys():
			if arg not in acceptable:
				del kwds[arg]
	return receiver(**kwds)
#---------------------------------------------------------------------
def _removeReceiver(receiver):
	"""Remove receiver from connections."""
	for senderkey in connections.keys():
		for signal in connections[senderkey].keys():
			receivers = connections[senderkey][signal]
			try: receivers.remove(receiver)
			except: pass
			_cleanupConnections(senderkey, signal)
#---------------------------------------------------------------------
def _cleanupConnections(senderkey, signal):
	"""Delete any empty signals for senderkey. Delete senderkey if empty."""
	receivers = connections[senderkey][signal]
	if not receivers:
		# No more connected receivers. Therefore, remove the signal.
		signals = connections[senderkey]
		del signals[signal]
		if not signals:
			# No more signal connections. Therefore, remove the sender.
			_removeSender(senderkey)
#---------------------------------------------------------------------
def _removeSender(senderkey):
	"""Remove senderkey from connections."""
	del connections[senderkey]
	# Senderkey will only be in senders dictionary if sender 
	# could be weakly referenced.
	try: del senders[senderkey]
	except: pass

#=====================================================================
# $Log: gmDispatcher.py,v $
# Revision 1.7.2.1  2006-09-06 10:25:43  shilbert
# - removed some weird DOS/Windows EOL via dos2unix
#
# Revision 1.7  2005/10/10 18:10:33  ncq
# - ever so slightly beautify debugging
#
# Revision 1.6  2005/10/08 12:33:08  sjtan
# tree can be updated now without refetching entire cache; done by passing emr object to create_xxxx methods and calling emr.update_cache(key,obj);refresh_historical_tree non-destructively checks for changes and removes removed nodes and adds them if cache mismatch.
#
# Revision 1.5  2005/04/03 20:09:20  ncq
# - it's rather stupid to try to remove a signal that we just tested to not exist,
#   hence refrain from doing so
#
# Revision 1.4  2005/03/23 19:02:27  ncq
# - improved error handling
#
# Revision 1.3  2005/03/17 12:59:16  ncq
# - if an event receiver fails we should not fail all other receivers, too
# - so report and continue
# - but do not make us depend on gmLog just because of one fundamental,
#   low level failure - may be the wrong choice in the long term, however
#
# Revision 1.2  2004/06/21 17:05:20  ncq
# - whitespace cleanup
# - it's a bit harsh to throw an exception when trying
#   to disconnect an unconnected signal, reporting and
#   succeeding should do
#
# Revision 1.1	2004/02/25 09:30:13	 ncq
# - moved here from python-common
#
