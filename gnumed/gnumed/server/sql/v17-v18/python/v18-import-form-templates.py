# coding: utf8
#==============================================================
# GNUmed database schema change script
#
# License: GPL v2 or later
# Author: karsten.hilbert@gmx.net
#
#==============================================================
import os

from Gnumed.pycommon import gmPG2

#--------------------------------------------------------------

def run(conn=None):

	# vaccination history
	gmPG2.file2bytea (
		query = u"""
			update ref.paperwork_templates set
				data = %(data)s::bytea,
				external_version = '18.0'
			where
				name_long = 'Vaccination history (GNUmed default)'""",
		filename = os.path.join('..', 'sql', 'v17-v18', 'data', 'v18-GNUmed-default_vaccination_history_template.tex'),
		conn = conn
	)

	# invalid GKV-Rezept
	gmPG2.file2bytea (
		query = u"""
			update ref.paperwork_templates set
				data = %(data)s::bytea,
				external_version = '18.0'
			where
				name_long = 'ungültiges GKV-Rezept (GNUmed-Vorgabe)'""",
		filename = os.path.join('..', 'sql', 'v17-v18', 'data', 'v18-GNUmed-INVALID_default_GKV_Rezept_template.tex'),
		conn = conn
	)

	# LMcC autograph
	gmPG2.file2bytea (
		query = u"""
			update ref.keyword_expansion set
				textual_data = NULL,
				binary_data = %(data)s::bytea
			where
				keyword = 'autograph-LMcC'""",
		filename = os.path.join('..', 'sql', 'v17-v18', 'data', 'v18-LMcC_autograph.png'),
		conn = conn
	)

	# 1x1 pixels transparent PNG for use in overpic LaTeX environments
	gmPG2.file2bytea (
		query = u"""
			update ref.keyword_expansion set
				textual_data = NULL,
				binary_data = %(data)s::bytea
			where
				keyword = '1x1-transparent-PNG'""",
		filename = os.path.join('..', 'sql', 'v17-v18', 'data', 'v18-1x1-transparent.png'),
		conn = conn
	)

	return True

#==============================================================