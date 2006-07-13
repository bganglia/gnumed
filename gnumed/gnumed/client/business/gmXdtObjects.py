"""GnuMed German XDT parsing objects.

This encapsulates some of the XDT data into
objects for easy access.
"""
#==============================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/business/gmXdtObjects.py,v $
# $Id: gmXdtObjects.py,v 1.11 2006-07-13 21:00:32 ncq Exp $
__version__ = "$Revision: 1.11 $"
__author__ = "K.Hilbert, S.Hilbert"
__license__ = "GPL"

import os.path, sys, fileinput, string, md5, time, linecache, tempfile

from Gnumed.pycommon import gmLog
_log = gmLog.gmDefLog
_log.Log(gmLog.lData, __version__)

from Gnumed.pycommon import gmExceptions
from Gnumed.business import gmXdtMappings
#==============================================================
class cXDTPatient:
	"""Handle patient demographics in xDT files.

	- these files are used for inter-application communication in Germany
	"""
	_map_id2name = {
		'3101': 'lastname',
		'3102': 'firstname',
		'3103': 'dob',
		'3110': 'gender'
	}
	_wanted_fields = (
		'3101', 
		'3102',
		'3103',
		'3110'
	)

	#-----------------------------------
	def __init__(self, filename = None):

		self.filename = filename
		self.__parsed = False
	#-----------------------------------
	def __str__(self):
		if self.__parsed:
			return '<%s @ %s: %s parsed from file [%s]>' % (self.__class__.__name__, id(self), str(self.__data), self.filename)
		else:
			return '<%s @ %s: unparsed file [%s]>' % (self.__class__.__name__, id(self), self.filename)
	#-----------------------------------
	def __parse(self):
		"""Read the _first_ patient from an xDT compatible file."""

		self.__data = {}
		data = {}

		# xDT line format: aaabbbbcccccccccccCRLF where aaa = length, bbbb = record type, cccc... = content
		for line in fileinput.input(self.filename):

			# found all data by now ?
			if len(data) == len(cXDTPatient._wanted_fields):
				break

			line = string.replace(line,'\015','')
			line = string.replace(line,'\012','')

			# do we care about this line ?
			field = line[3:7]
			if field in cXDTPatient._wanted_fields:
				field_name = cXDTPatient._map_id2name[field]
				data[field_name] = line[7:]

		# cleanup
		fileinput.close()

		# found all data ?
		if len(data) != len(cXDTPatient._wanted_fields):
			_log.Log(gmLog.lErr, "did not find sufficient patient data in XDT file [%s]" % self.filename)
			_log.Log(gmLog.lErr, 'found: %s' % data)
			return False

		# normalize DOB
		data['dob_day'] = int(data['dob'][:2])
		data['dob_month'] = int(data['dob'][2:4])
		data['dob_year'] = int(data['dob'][4:])

		#  mangle gender
		data['gender'] = gmXdtMappings.map_gender_xdt2gm[data['gender']]

		self.__data = data
		self.__parsed = True
		return True
	#--------------------------------------------------------
	# attribute handler
	#--------------------------------------------------------
	def __getitem__(self, item):

		if item == 'filename':
			return self.filename

		if not self.__parsed:
			self.__parse()

		return self.__data[item]
#==============================================================
# FIXME: the following *should* get wrapped in class XdtFile ...
#--------------------------------------------------------------
def xdt_get_pats(aFile):
	pat_ids = []
	pat_names = []
	pats = {}
	# xDT line format: aaabbbbcccccccccccCRLF where aaa = length, bbbb = record type, cccc... = content
	# read patient dat
	for line in fileinput.input(aFile):
		# remove trailing CR and/or LF
		line = string.replace(line,'\015','')
		line = string.replace(line,'\012','')
		# do we care about this line ?
		field = line[3:7]
		# yes, if type = patient id
		if field == '3000':
			pat_id = line[7:]
			if pat_id not in pat_ids:
				pat_ids.append(pat_id)
			continue
		# yes, if type = patient name
		if field == '3101':
			pat_name = line [7:]
			if pat_name not in pat_names:
				pat_names.append(pat_name)
				pats[pat_id] = pat_name
			continue
	fileinput.close()

	_log.Log(gmLog.lData, "patients found: %s" % len(pat_ids))
	return pats
#==============================================================
def get_pat_files(aFile, ID, name, patdir = None, patlst = None):
	_log.Log(gmLog.lData, "getting files for patient [%s:%s]" % (ID, name))
	files = patlst.get(aGroup = "%s:%s" % (ID, name), anOption = "files")
	_log.Log(gmLog.lData, "%s => %s" % (patdir, files))
	return [patdir, files]
#==============================================================
def split_xdt_file(aFile,patlst,cfg):
	content=[]
	lineno = []

	# xDT line format: aaabbbbcccccccccccCRLF where aaa = length, bbbb = record type, cccc... = content

	content = []
	record_start_lines = []

	# find record starts
	for line in fileinput.input(aFile):
		strippedline = string.replace(line,'\015','')
		strippedline = string.replace(strippedline,'\012','')
		# do we care about this line ? (records start with 8000)
		if strippedline[3:7] == '8000':
			record_start_lines.append(fileinput.filelineno())

	# loop over patient records
	for aline in record_start_lines:
		# WHY +2 ?!? 
		line = linecache.getline(aFile,aline+2) 
		# remove trailing CR and/or LF
		strippedline = string.replace(line,'\015','')
		strippedline = string.replace(strippedline,'\012','')
		# do we care about this line ?
		field = strippedline[3:7]
		# extract patient id
		if field == '3000': 
			ID = strippedline[7:]
			line = linecache.getline(aFile,aline+3)
			# remove trailing CR and/or LF
			strippedline = string.replace(line,'\015','')
			strippedline = string.replace(strippedline,'\012','')
			# do we care about this line ?
			field = strippedline[3:7]
			if field == '3101':
				name = strippedline [7:]
			startline=aline
			endline=record_start_lines[record_start_lines.index(aline)+1]
			_log.Log(gmLog.lData, "reading from%s" %str(startline)+' '+str(endline) )
			for tmp in range(startline,endline):							
				content.append(linecache.getline(aFile,tmp))
				_log.Log(gmLog.lData, "reading %s"%tmp )
			hashes = check_for_previous_records(ID,name,patlst)
			# is this new content ?
			data_hash = md5.new()
			map(data_hash.update, content)
			digest = data_hash.hexdigest()
			if digest not in hashes:
				pat_dir = cfg.get("xdt-viewer", "export-dir")
				file = write_xdt_pat_data(content, pat_dir)
				add_file_to_patlst(ID, name, patlst, file, ahash)
			content = []
		else:
			continue
	# cleanup
	fileinput.close()
	patlst.store()
	return 1
#==============================================================
def get_rand_fname(aDir):
	# set up temp file environment for creating unique random directory
	tempfile.tempdir = aDir
	tempfile.template = ""
	# create temp filename
	tmpname = tempfile.mktemp(suffix = time.strftime(".%Y%m%d-%H%M%S", time.localtime()))
	# extract name for dir
	path, fname = os.path.split(tmpname)
	return fname
#==============================================================
def write_xdt_pat_data(data, aDir):
	"""write record for this patient to new file"""
	pat_file = open(os.path.join(aDir, get_rand_fname(aDir)), "w")
	map(pat_file.write, data)
	pat_file.close()
	return fname
#==============================================================
def check_for_previous_records(ID, name, patlst):
	anIdentity = "%s:%s" % (ID, name)
	hashes = []
	# patient not listed yet
	if anIdentity not in patlst.getGroups():
		_log.Log(gmLog.lData, "identity not yet in list" )
		patlst.set(aGroup = anIdentity, anOption = 'files', aValue = [], aComment = '')
	# file already listed ?
	file_defs = patlst.get(aGroup = anIdentity, anOption = "files")
	for line in file_defs:
		file, ahash = string.split(line,':')
		hashes.append(ahash)

	return hashes
#==============================================================
def add_file_to_patlst(ID, name, patlst, new_file, ahash):
	anIdentity = "%s:%s" % (ID, name)
	files = patlst.get(aGroup = anIdentity, anOption = "files")
	for file in new_files:
		files.append("%s:%s" % (file, ahash))
	_log.Log(gmLog.lData, "files now there : %s" % files)
	patlst.set(aGroup=anIdentity, anOption="files", aValue = files, aComment="")
#==============================================================
# main
#--------------------------------------------------------------
if __name__ == "__main__":
	# test framework if run by itself
	_log.SetAllLogLevels(gmLog.lData)
	_log.Log(gmLog.lInfo, __version__)

	patfile = sys.argv[1]
	print "reading patient data from xDT file [%s]" % patfile

	pat = cXDTPatient(filename = patfile)
	print pat

	print '%s %s (%s)' % (pat['firstname'], pat['lastname'], pat['gender'])
	print 'dob:', pat['dob']
	print '%s.%s.%s' % (pat['dob_day'], pat['dob_month'], pat['dob_year'])

	print pat

#==============================================================
# $Log: gmXdtObjects.py,v $
# Revision 1.11  2006-07-13 21:00:32  ncq
# - cleanup gender mappings
# - streamline cXdtPatient and improve test harness
#
# Revision 1.10  2006/05/12 12:05:04  ncq
# - cleanup
#
# Revision 1.9	2004/03/20 19:45:49  ncq
# - rename gender map
#
# Revision 1.8	2004/03/18 11:05:00  shilbert
# - fixed xDT-parsing in standalone mode
#
# Revision 1.7	2004/02/25 09:46:20  ncq
# - import from pycommon now, not python-common
#
# Revision 1.6	2003/11/17 10:56:35  sjtan
#
# synced and commiting.
#
# Revision 1.1	2003/10/23 06:02:38  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.5	2003/08/28 18:54:32  shilbert
# - corrected some minor glitches
#
# Revision 1.4	2003/08/27 14:58:58  ncq
# - added helpers written by shilbert for XdtViewer
#
# Revision 1.3	2003/04/19 22:56:03  ncq
# - speed up __load_data(), better encapsulate xdt file maps
#
# Revision 1.2	2003/02/18 02:43:16  ncq
# - rearranged __getitem__ to check self.__data last
#
# Revision 1.1	2003/02/17 23:33:14  ncq
# - first version
#
