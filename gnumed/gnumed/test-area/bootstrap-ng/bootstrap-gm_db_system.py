#!/usr/bin/env python

"""GnuMed user/group installation.

This script installs all the users and groups needed for
proper GnuMed usage. It will also set proper access rights.

Theory of operation:

Rights will be granted to users via groups. Effectively, groups
are granted certain access rights and users are added to the
appropriate groups as needed.

There's a special user called "gmdb-owner" who owns all the
database objects.

Normal users are represented twice in the database:
 1) under their normal user name with read-only rights
 2) under their user name prepended by "_" for write access

For all this to work you must be able to access the database
server as the standard "postgres" superuser.

This script does NOT set up user specific configuration options.

All definitions are loaded from a config file.

Please consult the Developer's Guide in the GnuMed CVS for
further details.
"""
#==================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/test-area/bootstrap-ng/Attic/bootstrap-gm_db_system.py,v $
__version__ = "$Revision: 1.1 $"
__author__ = "Karsten.Hilbert@gmx.net"
__license__ = "GPL"

import sys, string, os.path, fileinput, os, time

# location of our modules
sys.path.append(os.path.join('.', 'modules'))

import gmLog
_log = gmLog.gmDefLog
_log.SetAllLogLevels(gmLog.lData)

import gmCfg
_cfg = gmCfg.gmDefCfgFile

import gmUserSetup

dbapi = None
try:
	from pyPgSQL import PgSQL
	dbapi = PgSQL
except ImportError:
	_log.Log(gmLog.lErr, "Cannot load pyPgSQL.PgSQL database adapter module.")
	try:
		import psycopg
		dbapi = psycopg
	except ImportError:
		_log.Log(gmLog.lErr, "Cannot load psycopg database adapter module.")
		try:
			import pgdb
			dbapi = pgdb
		except ImportError:
			print "Cannot find Python module for connecting to the database server. Program halted."
			_log.Log(gmLog.lErr, "Cannot load pgdb database adapter module.")
			raise

from gmExceptions import ConstructorError

_interactive = 0
_bootstrapped_servers = {}
_bootstrapped_dbs = {}
#==================================================================
class db_server:
	def __init__(self, aSrv_alias, aCfg):
		_log.Log(gmLog.lInfo, "bootstrapping server [%s]" % aSrv_alias)

		if _bootstrapped_servers.has_key(aSrv_alias):
			return None

		self.cfg = aCfg
		self.alias = aSrv_alias
		self.server_group = "server %s" % self.alias
		self.dbowner_password = None

		if not self.__bootstrap():
			raise ConstructorError, "db_server.__init__(): Cannot bootstrap db server."

		global _bootstrapped_servers
		_bootstrapped_servers[self.alias] = self

		return None
	#--------------------------------------------------------------
	def __bootstrap(self):
		# sanity checks
		self.template_db = self.cfg.get(self.server_group, "template database")
		if self.template_db is None:
			_log.Log(gmLog.lErr, "Need to know the template database name.")
			return None

		self.super_user = self.cfg.get(self.server_group, "super user")
		if self.super_user is None:
			_log.Log(gmLog.lErr, "Need to know the super user name.")
			return None

		self.super_user_password = self.cfg.get(self.server_group, "super user password")
		if self.super_user_password is None:
			if _interactive:
				print "I need the password for the database super user."
				print "(user [%s] in db [%s] on [%s:%s])" % (self.super_user, self.template_db, self.alias, self.cfg.get(self.server_group, "port"))
				self.super_user_password = raw_input("Please type password: ")
			else:
				_log.Log(gmLog.lErr, "Need to know the super user password.")
				return None

		# connect to template
		if not self.__connect(self.template_db, self.super_user, self.super_user_password):
			_log.Log(gmLog.lErr, "Cannot connect to template db [%s@%s] on [%s:%s]." % (self.super_user, self.template_db, self.alias, self.cfg.get(self.server_group, "port")))
			return None

		# add users/groups
		if not self.__bootstrap_db_users():
			_log.Log(gmLog.lErr, "Cannot bootstrap database users.")
			return None

		# add languages
		if not self.__bootstrap_proc_langs():
			_log.Log(gmLog.lErr, "Cannot bootstrap procedural languages.")
			return None

		# FIXME: test for features (eg. dblink)

		self.conn.close()
		return 1
	#--------------------------------------------------------------
	def __connect(self, aDB, aUser, aPW):
		_log.Log(gmLog.lInfo, "connecting to database [%s]" % aDB)
		dsn = "%s:%s:%s:%s:%s" % (
			self.cfg.get(self.server_group, "name"),
			self.cfg.get(self.server_group, "port"),
			aDB,
			aUser,
			aPW
		)
		try:
			self.conn = dbapi.connect(dsn)
		except:
			_log.LogException("Cannot connect (user [%s] with pwd [%s] in db [%s] on [%s:%s])." % (
				self.cfg.get(self.server_group, "name"),
				self.cfg.get(self.server_group, "port"),
				aDB,
				aUser,
				aPW),
				sys.exc_info(),
				fatal=1
			)
			return None
		_log.Log(gmLog.lInfo, "successfully connected to database")
		return 1
	#--------------------------------------------------------------
	# procedural languages related
	#--------------------------------------------------------------
	def __lang_exists(self, aLanguage):
		cmd = "SELECT lanname FROM pg_language WHERE lanname='%s';" % aLanguage
		aCursor = self.conn.cursor()
		try:
			aCursor.execute(cmd)
		except:
			_log.LogException(">>>[%s]<<< failed." % cmd, sys.exc_info(), fatal=1)
			return None

		res = aCursor.fetchone()
		tmp = aCursor.rowcount
		aCursor.close()
		if tmp == 1:
			_log.Log(gmLog.lInfo, "Language %s exists." % aLanguage)
			return 1

		_log.Log(gmLog.lInfo, "Language %s does not exist." % aLanguage)
		return None
	#--------------------------------------------------------------
	def __install_lang(self, aDirList = None, aLanguage = None):
		_log.Log(gmLog.lInfo, "installing procedural language [%s]" % aLanguage)

		if aLanguage is None:
			_log.Log(gmLog.lErr, "Need language name to install it !")
			return None

		lib_name = self.cfg.get(aLanguage, "library name")
		if lib_name is None:
			_log.Log(gmLog.lErr, "no language library name specified in config file")
			return None

		# FIXME: what about *.so.1.3.5 ?
		if self.__lang_exists(lib_name.replace(".so", "", 1)):
			return 1

		if aDirList is None:
			_log.Log(gmLog.lErr, "Need dir list to search for language library !")
			return None

		# FIXME: this logically fails in remote installs !!!
		lib_path = None
		for lib_dir in aDirList:
			tmp = os.path.join(lib_dir, lib_name)
			if os.path.exists(tmp):
				lib_path = tmp
				break

		if lib_path is None:
			_log.Log(gmLog.lErr, "cannot find language library file in any of %s" % aDirList)
			return None

		tmp = self.cfg.get(aLanguage, "call handler")
		if tmp is None:
			_log.Log(gmLog.lErr, "no call handler cmd specified in config file")
			return None
		call_handler_cmd = tmp[0] % lib_path

		tmp = self.cfg.get(aLanguage, "language activation")
		if tmp is None:
			_log.Log(gmLog.lErr, "no language activation cmd specified in config file")
			return None
		activate_lang_cmd = tmp[0]

		cursor = self.conn.cursor()
		try:
			cursor.execute(call_handler_cmd)
			cursor.execute(activate_lang_cmd)
		except:
			_log.LogException("cannot install procedural language [%s]" % aLanguage, sys.exc_info(), fatal=1)
			cursor.close()
			return None

		self.conn.commit()
		cursor.close()

		if not self.__lang_exists(lib_name.replace(".so", "", 1)):
			return None

		_log.Log(gmLog.lInfo, "procedural language [%s] successfully installed" % aLanguage)
		return 1
	#--------------------------------------------------------------
	def __bootstrap_proc_langs(self):
		_log.Log(gmLog.lInfo, "bootstrapping procedural")

		lang_aliases = self.cfg.get("GnuMed defaults", "procedural languages")
		# FIXME: better separation
		if (lang_aliases is None) or (len(lang_aliases) == 0):
			_log.Log(gmLog.lWarn, "No procedural languages to activate or error loading language list.")
			return 1

		lib_dirs = _cfg.get("installation", "language library dirs")
		if lib_dirs is None:
			_log.Log(gmLog.lErr, "Error loading procedural language library directories list.")
			return None

		for lang in lang_aliases:
			if not self.__install_lang(lib_dirs, lang):
				_log.Log(gmLog.lErr, "Error installing procedural language [%s]." % lang)
				return None

		return 1
	#--------------------------------------------------------------
	# user and group related
	#--------------------------------------------------------------
	def __bootstrap_db_users(self):
		_log.Log(gmLog.lInfo, "bootstrapping database users and groups")

		# create GnuMed owner
		if self.__create_dbowner() is None:
			_log.Log(gmLog.lErr, "Cannot install GnuMed database owner.")
			return None

		# insert standard groups
		if self.__create_groups() is None:
			_log.Log(gmLog.lErr, "Cannot create GnuMed standard groups.")
			return None

		# NOTE! those should be added via some standard sql script in the schema !

		# insert test users
#		if not self.__create_test_users():
#			_log.Log(gmLog.lErr, "Cannot bootstrap test database users.")

		# insert site-specific users
		#if not gmUserSetup.create_local_structure(dbconn):
		#	print "Cannot create site-specific GnuMed user/group structure.\nPlease see log file for details."

		return 1
	#--------------------------------------------------------------
	def __user_exists(self, aCursor, aUser):
		cmd = "SELECT usename FROM pg_user WHERE usename='%s';" % aUser
		try:
			aCursor.execute(cmd)
		except:
			_log.LogException(">>>[%s]<<< failed." % cmd, sys.exc_info(), fatal=1)
			return None
		res = aCursor.fetchone()
		if aCursor.rowcount == 1:
			_log.Log(gmLog.lInfo, "User [%s] exists." % aUser)
			return 1
		_log.Log(gmLog.lInfo, "User [%s] does not exist." % aUser)
		return None
	#--------------------------------------------------------------
	def get_dbowner_password(self):
		if self.dbowner_password is None:
			self.dbowner_password = self.cfg.get("GnuMed defaults", "database owner password")
			if self.dbowner_password is None:
				if _interactive:
					print "I need the password for the GnuMed database owner."
					print "(user [%s] on [%s:%s])" % (dbowner, self.alias, self.cfg.get(self.server_group, "port"))
					self.dbowner_password = raw_input("Please type password: ")
				else:
					_log.Log(gmLog.lErr, "Cannot load GnuMed database owner password from config file.")
					return None
		return self.dbowner_password
	#--------------------------------------------------------------
	def __create_dbowner(self):

		dbowner = self.cfg.get("GnuMed defaults", "database owner")
		if dbowner is None:
			_log.Log(gmLog.lErr, "Cannot load GnuMed database owner name from config file.")
			return None

		cursor = self.conn.cursor()
		# does this user already exist ?
		if self.__user_exists(cursor, dbowner):
			cursor.close()
			return 1

		self.get_dbowner_password()

		cmd = "CREATE USER \"%s\" WITH PASSWORD '%s' CREATEDB;" % (dbowner, self.dbowner_password)
		try:
			cursor.execute(cmd)
		except:
			_log.Log(gmLog.lErr, ">>>[%s]<<< failed." % cmd)
			_log.LogException("Cannot create GnuMed database owner [%s]." % dbowner, sys.exc_info(), fatal=1)
			cursor.close()
			return None

		# paranoia is good
		if not self.__user_exists(cursor, dbowner):
			cursor.close()
			return None

		self.conn.commit()
		cursor.close()
		return 1
	#--------------------------------------------------------------
	def __group_exists(self, aCursor, aGroup):
		cmd = "SELECT groname FROM pg_group WHERE groname='%s';" % aGroup
		try:
			aCursor.execute(cmd)
		except:
			_log.LogException(">>>[%s]<<< failed." % cmd, sys.exc_info(), fatal=1)
			return None
		res = aCursor.fetchone()
		if aCursor.rowcount == 1:
			_log.Log(gmLog.lInfo, "Group %s exists." % aGroup)
			return 1
		_log.Log(gmLog.lInfo, "Group %s does not exist." % aGroup)
		return None
	#--------------------------------------------------------------
	def __create_group(self, aCursor, aGroup):
		# does this group already exist ?
		if self.__group_exists(aCursor, aGroup):
			return 1

		cmd = "CREATE GROUP \"%s\";" % aGroup
		try:
			aCursor.execute(cmd)
		except:
			_log.LogException(">>>[%s]<<< failed." % cmd, sys.exc_info(), fatal=1)
			return None

		# paranoia is good
		if not self.__group_exists(aCursor, aGroup):
			return None

		return 1
	#--------------------------------------------------------------
	def __create_groups(self, aCfg = None, aSection = None):
		if aCfg is None:
			cfg = self.cfg
		else:
			cfg = aCfg

		if aSection is None:
			section = "GnuMed defaults"
		else:
			section = aSection

		groups = cfg.get(section, "groups")
		if groups is None:
			_log.Log(gmLog.lErr, "Cannot load GnuMed group names from config file (section [%s])." % section)
			return None

		cursor = self.conn.cursor()

		for group in groups:
			if not self.__create_group(cursor, group):
				cursor.close()
				return None

		self.conn.commit()
		cursor.close()
		return 1
#==================================================================
class database:
	def __init__(self, aDB_alias, aCfg):
		_log.Log(gmLog.lInfo, "bootstrapping database [%s]" % aDB_alias)

		self.conn = None
		self.cfg = aCfg
		self.alias = aDB_alias
		self.db_group = "database %s" % self.alias

		self.server_alias = self.cfg.get(self.db_group, "server alias")
		if self.server_alias is None:
			_log.Log(gmLog.lErr, "Server alias missing.")
			raise ConstructorError, "database.__init__(): Cannot bootstrap database."

		# make sure server is bootstrapped
		db_server(self.server_alias, self.cfg)

		if not self.__bootstrap():
			raise ConstructorError, "database.__init__(): Cannot bootstrap database."

		global _bootstrapped_dbs
		_bootstrapped_dbs[self.alias] = self

		return None
	#--------------------------------------------------------------
	def connect(self, aServer):
		try:
			dsn = "%s:%s:%s:%s:%s" % (aServer.server, aServer.port, aServer.template_db, aServer.super_user, aServer.super_user_password)
		except:
			_log.LogException("Cannot construct DSN !", sys.exc_info(), fatal=1)
			return None

		try:
			self.conn = dbapi.connect(dsn)
		except:
			_log.LogException("Cannot connect (user [%s] with pwd [%s] in db [%s] on [%s:%s])." % (aServer.server, aServer.port, aServer.template_db, aServer.super_user, aServer.super_user_password), sys.exc_info(), fatal=1)
			return None
		_log.Log(gmLog.lInfo, "successfully connected to database (user [%s] in db [%s] on [%s:%s])" % (gmUserSetup.dbowner["name"], aDB, core_server["host name"], core_server["port"]))
	#--------------------------------------------------------------
	def __bootstrap(self):
		owner = self.cfg.get("GnuMed defaults", "database owner")		

		srv = _bootstrapped_servers[self.server_alias]
		passwd = srv.get_dbowner_password()

		srv_group = "server %s" % server_alias
		db = self.cfg.get(srv_group, "template database")

		# connect as owner to template

		# check if db already exists

		# create db

		# reconnect to db as owner

		# import schema

		return 1
	#--------------------------------------------------------------
	def __db_exists(aDatabase):
		cmd = "SELECT datname FROM pg_database WHERE datname='%s';" % aDatabase

		aCursor = self.conn.cursor()
		try:
			aCursor.execute(cmd)
		except:
			_log.LogException(">>>[%s]<<< failed." % cmd, sys.exc_info(), fatal=1)
			return None

		res = aCursor.fetchone()
		tmp = aCursor.rowcount
		aCursor.close()
		if tmp == 1:
			_log.Log(gmLog.lInfo, "Database %s exists." % aDatabase)
			return 1

		_log.Log(gmLog.lInfo, "Database %s does not exist." % aDatabase)
		return None
#==================================================================
def dummy2():
	
	
	if server_alias is None:
		_log.Log(gmLog.lErr, "Need to know server name to connect to database [%s]." % aDatabaseAlias)
		return None

	# get db server object
	if __servers.has_key('server_alias'):
		server = __servers['server_alias']
	else:
		try:
			server = db_server(server_alias, _cfg)
			__servers['server_alias'] = server
		except:
			_log.Log(gmLog.lErr, "Cannot init server [%s] object." % server_alias)
			return None

#==================================================================
def connect_to_db():
	print "Connecting to PostgreSQL server as initial user ..."

	# load database adapter


	# load authentication information
	global core_server
	tmp = _cfg.get("core server", "name")
	if not tmp:
		_log.Log(gmLog.lErr, "Cannot load database host name from config file.")
		tmp = "localhost"
	core_server["host name"] = ""
	if _cfg.get("installation", "interactive") == "yes":
		core_server["host name"] = raw_input("host [%s]: " % tmp)
	if core_server["host name"] == "":
		core_server["host name"] = tmp

	tmp = _cfg.get("core server", "port")
	if not tmp.isdigit():
		_log.Log(gmLog.lErr, "Cannot load database API port number from config file.")
		tmp = 5432
	core_server["port"] = raw_input("port [%s]: " % tmp)
	if core_server["port"] == "":
		core_server["port"] = tmp

	global initial_database
	tmp = _cfg.get("core server", "initial database")
	if not tmp:
		_log.Log(gmLog.lErr, "Cannot load initial database name from config file.")
		tmp = "template1"
	initial_database = raw_input("database [%s]: " % tmp)
	if initial_database == "":
		initial_database = tmp

	global initial_user
	tmp = _cfg.get("core server", "initial user")
	if not tmp:
		_log.Log(gmLog.lErr, "Cannot load database super-user from config file.")
		tmp = "postgres"
	initial_user["name"] = raw_input("user [%s]: " % tmp)
	if initial_user["name"] == "":
		initial_user["name"] = tmp

	# get password from user
	print "We still need a password to actually access the database."
	print "(user [%s] in db [%s] on [%s:%s])" % (initial_user["name"], initial_database, core_server["host name"], core_server["port"])
	initial_user["password"] = raw_input("Please type password: ")

	# log in
	dsn = "%s:%s:%s:%s:%s" % (core_server["host name"], core_server["port"], initial_database, initial_user["name"], initial_user["password"])
	try:
		conn = dbapi.connect(dsn)
	except:
		exc = sys.exc_info()
		_log.LogException("Cannot connect (user [%s] with pwd [%s] in db [%s] on [%s:%s])." % (initial_user["name"], initial_user["password"], initial_database, core_server["host name"], core_server["port"]), exc, fatal=1)
		return None
	_log.Log(gmLog.lInfo, "successfully connected to database (user [%s] in db [%s] on [%s:%s])" % (initial_user["name"], initial_database, core_server["host name"], core_server["port"]))

	print "Successfully connected."
	return conn
#------------------------------------------------------------------
def reconnect_as_gm_owner():
	print "Reconnecting to PostgreSQL server as GnuMed database owner ..."

	global core_server
	global initial_database

	if not gmUserSetup.dbowner.has_key("name"):
		_log.Log(gmLog.lErr, "Cannot connect without GnuMed database owner name.")
		return None

	if not gmUserSetup.dbowner.has_key("password"):
		# get password from user
		print "We need the password for the GnuMed database owner."
		print "(user [%s] in db [%s] on [%s:%s])" % (gmUserSetup.dbowner["name"], initial_database, core_server["host name"], core_server["port"])
		gmUserSetup.dbowner["password"] = raw_input("Please type password: ")

	# log in
	try:
		dsn = "%s:%s:%s:%s:%s" % (core_server["host name"], core_server["port"], initial_database, gmUserSetup.dbowner["name"], gmUserSetup.dbowner["password"])
	except:
		_log.LogException("Cannot construct DSN !", sys.exc_info(), fatal=1)
		return None

	try:
		conn = dbapi.connect(dsn)
	except:
		_log.LogException("Cannot connect (user [%s] with pwd [%s] in db [%s] on [%s:%s])." % (gmUserSetup.dbowner["name"], gmUserSetup.dbowner["password"], initial_database, core_server["host name"], core_server["port"]), sys.exc_info(), fatal=1)
		return None
	_log.Log(gmLog.lInfo, "successfully connected to database (user [%s] in db [%s] on [%s:%s])" % (gmUserSetup.dbowner["name"], initial_database, core_server["host name"], core_server["port"]))

	print "Successfully connected."
	return conn
#------------------------------------------------------------------
def connect_to_core_db(aDB):
	print "Connecting to GnuMed core database ..."

	global core_server

	if not gmUserSetup.dbowner.has_key("name"):
		_log.Log(gmLog.lErr, "Cannot connect without GnuMed database owner name.")
		return None

	if not gmUserSetup.dbowner.has_key("password"):
		# get password from user
		print "We need the password for the GnuMed database owner."
		print "(user [%s] in db [%s] on [%s:%s])" % (gmUserSetup.dbowner["name"], aDB, core_server["host name"], core_server["port"])
		gmUserSetup.dbowner["password"] = raw_input("Please type password: ")

	# log in
	try:
		dsn = "%s:%s:%s:%s:%s" % (core_server["host name"], core_server["port"], aDB, gmUserSetup.dbowner["name"], gmUserSetup.dbowner["password"])
	except:
		_log.LogException("Cannot construct DSN !", sys.exc_info(), fatal=1)
		return None

	try:
		conn = dbapi.connect(dsn)
	except:
		_log.LogException("Cannot connect (user [%s] with pwd [%s] in db [%s] on [%s:%s])." % (gmUserSetup.dbowner["name"], gmUserSetup.dbowner["password"], aDB, core_server["host name"], core_server["port"]), sys.exc_info(), fatal=1)
		return None
	_log.Log(gmLog.lInfo, "successfully connected to database (user [%s] in db [%s] on [%s:%s])" % (gmUserSetup.dbowner["name"], aDB, core_server["host name"], core_server["port"]))

	print "Successfully connected."
	return conn
#==================================================================
#==================================================================
#------------------------------------------------------------------
#------------------------------------------------------------------
#------------------------------------------------------------------
def create_db(aConn, aDB):
	if db_exists(aDB):
		return 1

	# create main database
	cursor = aConn.cursor()
	# FIXME: we need to pull this nasty trick of ending and restarting
	# the current transaction to work around pgSQL automatically associating
	# cursors with transactions
	cmd = 'commit; create database "%s"; begin' % aDB
	try:
		cursor.execute(cmd)
	except:
		_log.LogException(">>>[%s]<<< failed." % cmd, sys.exc_info(), fatal=1)
		return None
	aConn.commit()
	cursor.close()

	if not db_exists(aDB):
		return None
	_log.Log(gmLog.lInfo, "Successfully created GnuMed core database [%s]." % aDB)
	return 1
#------------------------------------------------------------------
def import_schema_file(anSQL_file = None, aDB = None, aHost = None, aUser = None, aPassword = None):
	# sanity checks
	if anSQL_file is None:
		_log.Log(gmLog.lErr, "Cannot import schema without schema file.")
		return None
	SQL_file = os.path.abspath(anSQL_file)
	if not os.path.exists(SQL_file):
		_log.Log(gmLog.lErr, "Schema file [%s] does not exist." % SQL_file)
		return None
	path = os.path.dirname(SQL_file)
	os.chdir(path)
	if aDB is None:
		_log.Log(gmLog.lErr, "Cannot import schema without knowing the database.")
		return None
	if aHost is None:
		_log.Log(gmLog.lErr, "Cannot import schema without knowing the database host.")
		return None
	if aUser is None:
		_log.Log(gmLog.lErr, "Cannot import schema without knowing the database user.")
		return None
	if aPassword is None:
		_log.Log(gmLog.lErr, "Cannot import schema without knowing the database user password.")
		return None

	# -W = force password prompt
	# -q = quiet
	#cmd = 'psql -a -E -h "%s" -d "%s" -U "%s" -f "%s" >> /tmp/psql-import.log 2>&1' % (aHost, aDB, aUser, SQL_file)
	cmd = 'psql -q -h "%s" -d "%s" -U "%s" -f "%s"' % (aHost, aDB, aUser, SQL_file)
	_log.Log(gmLog.lInfo, "running >>>%s<<<" % cmd)

	result = os.system(cmd)

	#cmd = 'psql -q -W -h "%s" -d "%s" -U "%s" -f "%s"' % (aHost, aDB, aUser, SQL_file)
	#cmd = 'psql -a -E -W -h "%s" -d "%s" -U "%s" -f "%s"' % (aHost, aDB, aUser, SQL_file)
#	pipe = popen2.Popen3(cmd, 1==1)
#	pipe.tochild.write("%s\n" % aPassword)
#	pipe.tochild.flush()
#	pipe.tochild.close()

#	result = pipe.wait()
#	print result

	# read any leftovers
#	pipe.fromchild.flush()
#	pipe.childerr.flush()
#	tmp = pipe.fromchild.read()
#	lines = tmp.split("\n")
#	for line in lines:
#		_log.Log(gmLog.lData, "child stdout: [%s]" % line, gmLog.lCooked)
#	tmp = pipe.childerr.read()
#	lines = tmp.split("\n")
#	for line in lines:
#		_log.Log(gmLog.lErr, "child stderr: [%s]" % line, gmLog.lCooked)

#	pipe.fromchild.close()
#	pipe.childerr.close()
#	del pipe

	_log.Log(gmLog.lInfo, "raw result: %s" % result)

	if os.WIFEXITED(result):
		exitcode = os.WEXITSTATUS(result)
		_log.Log(gmLog.lInfo, "shell level exit code: %s" % exitcode)
		if exitcode == 0:
			_log.Log(gmLog.lInfo, "success")
			return 1

		if exitcode == 1:
			_log.Log(gmLog.lErr, "failed: psql internal error")
		elif exitcode == 2:
			_log.Log(gmLog.lErr, "failed: database connection error")
		elif exitcode == 3:
			_log.Log(gmLog.lErr, "failed: pSQL script error")
	else:
		_log.Log(gmLog.lWarn, "aborted by signal")
		return None
#------------------------------------------------------------------
def push_schema_into_db(sql_cmds = None):
	if sql_cmds is None:
		_log.Log(gmLog.lErr, "cannot import schema without a schema definition")
		return None
	_log.Log(gmLog.lData, sql_cmds)
	cursor = dbconn.cursor()
	for cmd in sql_cmds:
		try:
			cursor.execute("%s;" % cmd)
		except:
			_log.LogException(">>>[%s;]<<< failed." % cmd, sys.exc_info(), fatal=1)
			cursor.close()
			return None
	dbconn.commit()
	cursor.close()
	return 1
#------------------------------------------------------------------
def bootstrap_core_database():
	print "\nDo you want to create a GnuMed core database on this server ?"
	print "You will usually want to do this unless you are only\nrunning one particular service on this machine."
	answer = None
	while answer not in ["y", "n", "yes", "no"]:
		answer = raw_input("Create GnuMed core database ? [y/n]: ")

	if answer not in ["y", "yes"]:
		_log.Log(gmLog.lInfo, "User did not want to create GnuMed core database on this machine.")
		return 1

	print "Bootstrapping GnuMed core database..."

	global dbconn

	# reconnect as GnuMed database owner
	dbconn.close()
	tmp = reconnect_as_gm_owner()
	if tmp is None:
		exit_with_msg("Cannot reconnect to database as GnuMed database owner.")
	dbconn = tmp

	# actually create the new core database
	database = _cfg.get("GnuMed defaults", "core database name")
	if not database:
		_log.Log(gmLog.lErr, "Cannot load name of core GnuMed database from config file.")
		database = "gnumed"
	if not create_db(dbconn, database):
		exit_with_msg("Cannot create GnuMed core database [%s] on this machine." % database)

	# reconnect to new core database
#	dbconn.close()
#	tmp = connect_to_core_db(database)
#	if tmp is None:
#		exit_with_msg("Cannot connect to GnuMed core database.")
#	dbconn = tmp

	# get schema files
	sql_files = _cfg.get("GnuMed defaults", "core database schema")
	if sql_files is None:
		_log.Log(gmLog.lWarn, "No schema definition files specified in config file !")
		exit_with_msg("No schema files defined for GnuMed core database [%s]." % database)

	# and import them
	for file in sql_files:

		if not import_schema_file(
			anSQL_file = file,
			aHost = core_server["host name"],
			aDB = database,
			aUser = gmUserSetup.dbowner["name"],
			aPassword = gmUserSetup.dbowner["password"]
		):
			exit_with_msg("Cannot import SQL schema into GnuMed core database [%s]." % database)

	print "Successfully bootstrapped GnuMed core database [%s]." % database
	return 1
#==================================================================
def dummy():


	db_name = _cfg.get(db_group, "database name")


#==================================================================
def bootstrap_database(db_alias):
	if _bootstrapped_dbs.has_key(db_alias):
		return 1
	else:
		_bootstrapped_dbs[db_alias] = database(aDB_alias = db_alias, aCfg = _cfg)
#------------------------------------------------------------------
def get_db_conn(db_alias):
	db_group = "database %s" % db_alias
	server_alias = _cfg.get(db_group, "server alias")
	if server_alias is None:
		_log.Log(gmLog.lErr, "Need to know server name to connect to database [%s]." % db_alias)
		return None

	conn_key = "%s-%s"
	if __db_conns.has_key(db_alias):
		return __db_conns[db_alias]
	else:
		bootstrap_database(db_alias)

	if __db_conns.has_key(db_alias):
		return __db_conns[db_alias]
	else:
		_log.Log(gmLog.lErr, "Cannot connect to database [%s]." % db_alias)
		return None
#==================================================================
def verify_pg_version(aServiceGroup = None, aConn = None):
	"""Verify database version information."""

	required_version = _cfg.get(aServiceGroup, "postgres version")
	if required_version is None:
		_log.Log(gmLog.lErr, "Cannot load minimum required PostgreSQL version from config file.")
		return None

	if aConn.version < required_version:
		_log.Log(gmLog.lErr, "Reported live PostgreSQL version [%s] is smaller than the required minimum version [%s]." % (aConn.version, required_version))
		return None

	_log.Log(gmLog.lInfo, "installed PostgreSQL version: [%s] - this is fine with me" % aConn.version)
	return 1
#------------------------------------------------------------------
def bootstrap_service(aService = None):
	_log.Log(gmLog.lInfo, "bootstrapping service [%s]" % aService)

	# sanity check
	if aService is None:
		_log.Log(gmLog.lErr, "Need to know service name to install it.")
		return None
	service_group = "service %s" % aService

	# load service definition
	database_alias = _cfg.get(service_group, "database alias")
	if database_alias is None:
		_log.Log(gmLog.lErr, "Need to know database name to install service [%s]." % aService)
		return None

	# bootstrap database
	try:
		db = database(database_alias, _cfg)
	except:
		_log.LogException("Cannot bootstrap service [%s]." % aService, sys.exc_info(), fatal = 1)
		return None

	# check PostgreSQL version
#	if not verify_pg_version(service_group, db.getConn()):
#		_log.Log(gmLog.lErr, "Wrong PostgreSQL version.")
#		return None

	# import schema
	schema_files = _cfg.get(service_group, "schema")
	if schema_files is None:
		_log.Log(gmLog.lErr, "Need to know schema definition to install service [%s]." % aService)
		return None

#	if not import_schema(conn, schema_files):
#		_log.Log(gmLog.lErr, "Cannot import schema definition for service [%s] into database [%s]." % (aService, database_alias))
#		return None

	# FIXME - register service
	# a) in its own database
	# b) in the distributed database
	return 1
#------------------------------------------------------------------
def bootstrap_services():
	# get service list
	services = _cfg.get("installation", "services")
	if services is None:
		exit_with_msg("Service list empty. Nothing to do here.")
	# run through services
	for service in services:
		if bootstrap_service(service) is None:
			return None
	return 1
#==================================================================
def exit_with_msg(aMsg = None):
	if not (aMsg is None):
		print aMsg
	print "Please see log file for details."
	try:
		dbconn.close()
	except:
		pass
	_log.Log(gmLog.lErr, aMsg)
	_log.Log(gmLog.lInfo, "shutdown")
	sys.exit(1)
#------------------------------------------------------------------
def show_msg(aMsg = None):
	if not (aMsg is None):
		print aMsg
	print "Please see log file for details."
#==================================================================
if __name__ == "__main__":
	_log.Log(gmLog.lInfo, "startup (%s)" % __version__)
	_log.Log(gmLog.lInfo, "bootstrapping GnuMed database system from file [%s] (%s)" % (_cfg.get("revision control", "file"), _cfg.get("revision control", "version")))

	print "Bootstrapping GnuMed database system..."

	tmp = _cfg.get("installation", "interactive")
	if tmp == "yes":
		_interactive = 1

	# bootstrap services
	if not bootstrap_services():
		exit_with_msg("Cannot bootstrap services.")

	# connect to template database as superuser

#	tmp = connect_to_db()
#	if tmp is None:
#		exit_with_msg("Cannot connect to database.")
#	dbconn = tmp

	# create users/groups
#	bootstrap_user_structure()

	# insert procedural languages
#	bootstrap_procedural_languages()

	# boostrap gnumed core database
#	bootstrap_core_database()

	# setup (possibly distributed) services

#	dbconn.close()
	_log.Log(gmLog.lInfo, "shutdown")
	print "Done bootstrapping."
else:
	print "This currently isn't intended to be used as a module."
#==================================================================
# $Log: bootstrap-gm_db_system.py,v $
# Revision 1.1  2003-01-13 16:55:20  ncq
# - first checkin of next generation
#
# Revision 1.10  2002/11/29 13:02:53  ncq
# - re-added psycopg support (hopefully)
#
# Revision 1.9  2002/11/18 22:41:21  ncq
# - don't really know what changed
#
# Revision 1.8  2002/11/18 12:23:31  ncq
# - make Debian happy by checking for psycopg, too
#
# Revision 1.7  2002/11/16 01:12:09  ncq
# - now finally also imports sql schemata from files
#
# Revision 1.6  2002/11/03 15:03:07  ncq
# - capture a little more info to hopefully catch the bug with DSN setup
#
# Revision 1.5  2002/11/01 15:17:44  ncq
# - need to wrap "create database" in "commit; ...; begin;" to work
#   around auto-transactions in pyPgSQL
#
# Revision 1.4  2002/11/01 14:06:53  ncq
# - another typo
#
# Revision 1.3  2002/11/01 14:05:39  ncq
# - typo
#
# Revision 1.2  2002/11/01 13:56:05  ncq
# - now also installs the GnuMed core database "gnumed"
#
# Revision 1.1  2002/10/31 22:59:19  ncq
# - tests environment, bootstraps users, bootstraps procedural languages
# - basically replaces gnumed.sql and setup-users.py
#
