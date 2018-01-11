#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright (c) 2012-2017, Malte Bublitz <https://malte70.de>
# 

__doc__ = """A small helper to get some information about your system and
python implementation, like the Operating System or the hardware platform.

	# Get a dict containing all gathered information
	from OSDetect import info as os_info
	print(os_info.getInfo())

	# Get a specific value
	print(os_info.getDistribution())
	# or using the dict key (a dot means a dict containing a dict)
	print(os_info.get("Python.Version"))

"""

import os
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
		elif sys.platform.startswith("win") or sys.platform.startswith("cygwin") or sys.platform.startswith("msys"):
			self.GetWinNTInfo()
		elif sys.platform.startswith("darwin"):
			self.GetOSXInfo()
		
	def GetLinuxInfo(self):
		"""Get the Information, this method contains the GNU/Linux-specific logic."""
		
		# Parse /etc/os-release
		if not os.path.exists("/etc/os-release"):
			os_release = None
		else:
			os_release = {}
			for _l in open("/etc/os-release").read().split("\n"):
				if not len(_l):
					continue
				_k, _v = _l.split("=")
				_v = _v.strip("\"")
				os_release[_k] = _v
		
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = platform.uname()[2]
		if os_release:
			self.info["Distribution"] = os_release["NAME"]
		else:
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
		return {
			"Implementation": platform.python_implementation(),
			"Version": platform.python_version()
		}
		
	def GetWinNTUptime(self):
		try:
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
		except ImportError:
			return "unknown"
		
	def GetWinNTProductInfo(self):
		"""Get Information about the Windows NT Product,
		a.k.a. the official Name like Windows 7"""
		try:
			RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion")
			if not ISCYGWIN:
				product = _winreg.QueryValueEx(RegistryKey, "ProductName")+" "+_winreg.QueryValueEx(RegistryKey, "CSDVersion")
			else:
				product = _winreg.QueryValueEx(RegistryKey, "ProductName")[0]+" "+_winreg.QueryValueEx(RegistryKey, "CSDVersion")[0]
		except NameError: # _winreg doesn't exist on msys
			product = platform.uname().system + " " + platform.uname().release
			
		return product
		
	def GetWinNTVersion(self):
		"""Get the NT Version of an Windows System, e.g. 6.1 for Windows 7"""
		try:
			RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion")
			if not ISCYGWIN:
				return _winreg.QueryValueEx(RegistryKey, "CurrentVersion")
			else:
				return _winreg.QueryValueEx(RegistryKey, "CurrentVersion")[0]
		except NameError: # _winreg doesn't exist on msys
			return ".".join(
				platform.uname().version.split(".")[:2]
			)
		
	def getInfo(self):
		"""Return the obtained information."""
		return self.info
		
	def get(self, key):
		value = None
		if not "." in key:
			if key in self.info.keys():
				value = self.info[key]
		else:
			if key.split(".")[0] in self.info.keys():
				_sub = self.info[key.split(".")[0]]
				if key.split(".")[1] in _sub.keys():
					value = _sub[key.split(".")[1]]
		
		return value
		
	def getOS(self):
		return self.get("OS")
		
	def getOSVersion(self):
		return self.get("OSVersion")
		
	def getDistribution(self):
		return self.get("Distribution")
		
	def getMachine(self):
		return self.get("Machine")
		
	def getPythonImplementation(self):
		return self.get("Python.Implementation")
		
	def getPythonVersion(self):
		return self.get("Python.Version")
		
	def hasGUI(self):
		if self.getOS() in ["Darwin", "Windows"]:
			# On OS X and Windows NT, a GUI is always present
			return True
			
		elif self.getOS() in ["Linux", "FreeBSD"]:
			# On GNU/Linux and FreeBSD check for presence of
			# $DISPLAY environment variable
			return "DISPLAY" in os.environ.keys()
		
info = OSInfo()

def main():
	print("Operating System: "+info.getOS()+" version "+info.getOSVersion())
	print("Distribution:     "+info.getDistribution())
	print("Machine:          "+info.getMachine())
	print("Python:           "+info.getPythonImplementation()+" "+info.getPythonVersion())
	
if __name__=='__main__':
	main()
