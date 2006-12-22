#===========================================================================
__doc__ = (
"""GNUmed date/time handling.

This modules provides access to date/time handling.

It utilitzes

	- Python time
	- Python datetime
	- mxDateTime

Note that if you want locale-aware formatting you need to call

	locale.setlocale(locale.LC_ALL, '')

somehwere before importing this script."""
)
#===========================================================================
# $Id: gmDateTime.py,v 1.3 2006-12-22 16:54:28 ncq Exp $
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/pycommon/gmDateTime.py,v $
__version__ = "$Revision: 1.3 $"
__author__ = "K. Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL (details at http://www.gnu.org)"

# stdlib
import sys, datetime as pyDT, time, os


# 3rd party
import mx.DateTime as mxDT
import psycopg2						# this will go once datetime has timezone classes

# GNUmed libs
if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmLog

_log = gmLog.gmDefLog
_log.Log(gmLog.lInfo, __version__)

dst_currently_in_effect = None
current_utc_offset = None
current_timezone_interval = None
current_iso_timezone_string = None
cLocalTimezone = psycopg2.tz.LocalTimezone

#===========================================================================
def init():

	_log.Log(gmLog.lData, 'mx.DateTime.now(): [%s]' % mxDT.now())
	_log.Log(gmLog.lData, 'datetime.now()   : [%s]' % pyDT.datetime.now())
	_log.Log(gmLog.lData, 'time.localtime() : [%s]' % str(time.localtime()))
	_log.Log(gmLog.lData, 'time.gmtime()    : [%s]' % str(time.gmtime()))

	try:
		_log.Log(gmLog.lData, '$TZ: [%s]' % os.environ['TZ'])
	except KeyError:
		_log.Log(gmLog.lData, '$TZ not defined')

	_log.Log(gmLog.lData, 'time.daylight: [%s] (whether or not DST is locally used)' % time.daylight)
	_log.Log(gmLog.lData, 'time.timezone: [%s] seconds' % time.timezone)
	_log.Log(gmLog.lData, 'time.altzone : [%s] seconds' % time.altzone)
	_log.Log(gmLog.lData, 'time.tzname  : [%s / %s] (non-DST / DST)' % time.tzname)
	_log.Log(gmLog.lData, 'mx.DateTime.now().gmtoffset(): [%s]' % mxDT.now().gmtoffset())

	global dst_currently_in_effect
	dst_currently_in_effect = bool(time.localtime()[8])
	_log.Log(gmLog.lData, 'DST currently in effect: [%s]' % dst_currently_in_effect)

	global current_utc_offset
	msg = 'DST currently%sin effect, using UTC offset of [%s] seconds instead of [%s] seconds'
	if dst_currently_in_effect:
		current_utc_offset = time.altzone
		_log.Log(gmLog.lData, msg % (' ', time.altzone, time.timezone))
	else:
		current_utc_offset = time.timezone
		_log.Log(gmLog.lData, msg % (' not ', time.timezone, time.altzone))

	if current_utc_offset < 0:
		_log.Log(gmLog.lData, 'UTC offset is negative, assuming EAST of Greenwich')
	elif current_utc_offset > 0:
		_log.Log(gmLog.lData, 'UTC offset is positive, assuming WEST of Greenwich')
	else:
		_log.Log(gmLog.lData, 'UTC offset is ZERO, assuming Greenwich')

	global current_timezone_interval
	current_timezone_interval = mxDT.now().gmtoffset()
	_log.Log(gmLog.lData, 'ISO timezone: [%s] (taken from mx.DateTime.now().gmtoffset())' % current_timezone_interval)
	global current_iso_timezone_string
	current_iso_timezone_string = str(current_timezone_interval).replace(',', '.')

	# do some magic to convert Python's timezone to a valid ISO timezone
	# is this safe or will it return things like 13.5 hours ?
	#_default_client_timezone = "%+.1f" % (-tz / 3600.0)
	#_log.Log(gmLog.lInfo, 'assuming default client time zone of [%s]' % _default_client_timezone)

#===========================================================================
# main
#---------------------------------------------------------------------------
if __name__ == '__main__':
	_log.SetAllLogLevels(gmLog.lData)
	init()

	print "DST currently in effect:", dst_currently_in_effect
	print "current UTC offset:", current_utc_offset, "seconds"
	print "current timezone (interval):", current_timezone_interval
	print "current timezone (ISO conformant string):", current_iso_timezone_string
	print "local timezone class:", cLocalTimezone
	tz = cLocalTimezone()
	print "local timezone instance:", tz
	print " (total) UTC offset:", tz.utcoffset(pyDT.datetime.now())
	print " DST adjustment:", tz.dst(pyDT.datetime.now())
	print " timezone name:", tz.tzname(pyDT.datetime.now())

#===========================================================================
# $Log: gmDateTime.py,v $
# Revision 1.3  2006-12-22 16:54:28  ncq
# - add cLocalTimezone from psycopg2 until datetime supports it
# - better logging
# - enhanced test suite
#
# Revision 1.2  2006/12/21 17:44:26  ncq
# - differentiate between timezone as interval and as string
# - if timezone string is to be ISO aware it cannot contain ","
#
# Revision 1.1  2006/12/21 10:50:50  ncq
# - date/time handling
#
#
