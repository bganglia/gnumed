#==============================================================
# GNUmed database schema change script
#
# License: GPL
# Author: karsten.hilbert@gmx.net
# 
#==============================================================
import os

from Gnumed.pycommon import gmPG2

#--------------------------------------------------------------
def run(conn=None):

	# medication list
	gmPG2.file2bytea (
		query = u"""
update ref.paperwork_templates
set data = %(data)s::bytea
where name_long = 'Current medication list (GNUmed default)'
""",
		filename = os.path.join('..', 'sql', 'v13-v14', 'data', 'GNUmed-default_medication_list_template.tex'),
		conn = conn
	)

	# referral letter
	gmPG2.file2bytea (
		query = u"""
update ref.paperwork_templates
set data = %(data)s::bytea
where name_long = 'Referral letter (GNUmed default) [Dr.Rogerio Luz]'
""",
		filename = os.path.join('..', 'sql', 'v13-v14', 'data', 'GNUmed-default_referral_letter_template.tex'),
		conn = conn
	)

	return True

#==============================================================