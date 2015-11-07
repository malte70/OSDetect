#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# OSDetect.py
#    A simple solution to detect the operating system, including detection of wine
#
# Copyright © 2012-2013 Malte Bublitz, https://malte-bublitz.de
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
# 
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 

import sys
import platform
try:
	import _winreg
	ISCYGWIN=False
except ImportError:
	try:
		import cygwinreg as _winreg
		ISCYGWIN=True
	except ImportError:
		pass

class OSInfo(object):
	"""Operating System Information object
	
	When creating an object of this class, the __init__()-function
	obtains all information. You can get the information as an dict using
	the GetInfo()-method.
	"""
	def __init__(self):
		self.info = {}
		# Linux detection
		if sys.platform.startswith("linux"):
			self.GetLinuxInfo()
		elif sys.platform.startswith("freebsd"):
			self.GetFreeBSDInfo()
		elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
			self.GetWinNTInfo()
		elif sys.platform.startswith("darwin"):
			self.GetOSXInfo()
		
	def GetLinuxInfo(self):
		"""Get the Information, this method contains the GNU/Linux-specific logic."""
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = platform.uname()[2]
		self.info["Distribution"] = " ".join(platform.dist())
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		
	def GetFreeBSDInfo(self):
		"""Get the Information, this method contains the FreeBSD-specific logic."""
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = platform.uname()[2]
		self.info["Distribution"] = " ".join(platform.dist())
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		
	def GetOSXInfo(self):
		"""Get the Information, this method contains the Mac OS X-specific logic."""
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = platform.uname()[2]
		self.info["Distribution"] = "Mac OS X " + platform.mac_ver()[0]
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		
	def GetWinNTInfo(self):
		"""Get the Information, this method contains the Windows NT-specific logic."""
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = self.GetWinNTVersion()
		self.info["Distribution"] = self.GetWinNTProductInfo()
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		self.info["Uptime"] = self.GetWinNTUptime()
		
	def GetPythonInfo(self):
		"""Get Information about the python runtime."""
		return {"implementation": platform.python_implementation(), "version": platform.python_version() }
		
	def GetWinNTUptime(self):
		from uptime import uptime
		seconds  = int(uptime())
		days     = seconds/60/60/24
		seconds -= days*60*60*24
		hours    = seconds/60/60
		seconds -= hours*60*60
		minutes  = seconds/60
		seconds -= minutes*60
		up = {
				"Days": days,
				"Hours": hours,
				"Minutes": minutes
				}
		up_str = u""
		_DAYS = u" days"
		_DAY = u" day"
		_HOURS = u" hours"
		_HOUR = u" hour"
		_MINUTES = u" minutes"
		_MINUTE = u" minute"
		if up["Days"]      > 1:
			up_str += ", " + unicode(up["Days"])    + _DAYS
		elif up["Days"]    > 0:
			up_str += ", " + unicode(up["Days"])    + _DAY
		if up["Hours"]     > 1:
			up_str += ", " + unicode(up["Hours"])   + _HOURS
		elif up["Hours"]   > 0:
			up_str += ", " + unicode(up["Hours"])   + _HOUR
		if up["Minutes"]   > 1:
			up_str += ", " + unicode(up["Minutes"]) + _MINUTES
		elif up["Minutes"] > 0:
			up_str += ", " + unicode(up["Minutes"]) + _MINUTE
		return up_str.lstrip(", ")
		
	def GetWinNTProductInfo(self):
		"""Get Information about the Windows NT Product,
		a.k.a. the official Name like Windows 7"""
		RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion")
		if not ISCYGWIN:
			return _winreg.QueryValueEx(RegistryKey, "ProductName")+" "+_winreg.QueryValueEx(RegistryKey, "CSDVersion")
		else:
			return _winreg.QueryValueEx(RegistryKey, "ProductName")[0]+" "+_winreg.QueryValueEx(RegistryKey, "CSDVersion")[0]
		
	def GetWinNTVersion(self):
		"""Get the NT Version of an Windows System, e.g. 6.1 for Windows 7"""
		RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion")
		if not ISCYGWIN:
			return _winreg.QueryValueEx(RegistryKey, "CurrentVersion")
		else:
			return _winreg.QueryValueEx(RegistryKey, "CurrentVersion")[0]
		
	def GetInfo(self):
		"""Return the obtained information."""
		return self.info
		
_info = OSInfo()
info = _info.GetInfo()

def run():
	global info
	print("Operating System: "+info["OS"])
	print("Operating System Version: "+info["OSVersion"])
	print("Distribution: "+info["Distribution"])
	print("Machine: "+info["Machine"])
	print("Python: "+info["Python"]["implementation"]+" "+info["Python"]["version"])

if __name__=='__main__':
	run()
