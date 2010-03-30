#!/bin/bash

# maybe force some locale setting here
#export LANGUAGE=fr

# if there are unicode troubles you can force to ASCII with this:
#export LANGUAGE=en


# source systemwide startup extension shell script if it exists
if [ -r /etc/gnumed/gnumed-startup-local.sh ] ; then
	echo "running /etc/gnumed/gnumed-startup-local.sh"
	. /etc/gnumed/gnumed-startup-local.sh
fi


# source local startup extension shell script if it exists
if [ -r ${HOME}/.gnumed/scripts/gnumed-startup-local.sh ] ; then
	echo "running ${HOME}/.gnumed/scripts/gnumed-startup-local.sh"
	. ${HOME}/.gnumed/scripts/gnumed-startup-local.sh
fi


# standard options
LOG="--log-file=gm-from-vcs.log"
CONF="--conf-file=gm-from-vcs.conf"
# these options are useful for development and debugging:
DEV_OPTS="--override-schema-check --skip-update-check --local-import --debug"
# --profile=gm-from-vcs.prof

PSYCOPG_DEBUG="on"		# should actually be done within gnumed.py based on --debug


# eventually run it
# - devel version:
echo "-------------------------------------------------"
echo "Running from Git branch: "`git branch | grep \*`
echo "-------------------------------------------------"
python gnumed.py ${LOG} ${CONF} ${DEV_OPTS} $@

# - production version:
#python gnumed.py ${LOG} ${CONF} $@

# - production version with HIPAA support:
#python gnumed.py ${LOG} ${CONF} --hipaa $@