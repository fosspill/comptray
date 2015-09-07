#! /usr/bin/python2

import sys
import os
import os.path
from subprocess import CalledProcessError, check_output, call

  
def comptonisrunning():
	try:
		output = check_output(["pgrep", "barorororo"])
	except CalledProcessError as e:
		output=False
	if output:
		curstatus=True
	else:
		curstatus=False
	return curstatus

print (comptonisrunning())
