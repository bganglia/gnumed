@echo off
REM =================================
REM $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/test-area/blobs_hilbert/viewer-tree/Attic/run-viewer.bat,v $
REM $Revision: 1.4 $
REM =================================
REM set your preferred language here
REM set LANG=de_DE@euro

c:\Python22\python.exe .\gmShowMedDocs.py --conf-file=.\gnumed-archive.conf --text-domain=gnumed-archive

REM Delete the XDT file with the patient data
REM pause
REM del c:\....\patient.dat
