#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# OSDetect.py
#    A simple solution to detect the operating system, including detection of wine
#
# Copyright © 2012 Malte Bublitz, https://malte-bublitz.de
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
import os
import platform
try:
	import _winreg
except ImportError:
	pass

class OSInfo(object):
	def __init__(self):
		self.info = {}
		# Linux detection
		if sys.platform.startswith("linux"):
			self.GetLinuxInfo()
		elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
			self.GetWinNTInfo()
		elif sys.platform.startswith("darwin"):
			self.GetOSXInfo()
		
	def GetLinuxInfo(self):
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = platform.uname()[2]
		self.info["Distribution"] = " ".join(platform.dist())
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		
	def GetOSXInfo(self):
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = platform.uname()[2]
		self.info["Distribution"] = "Mac OS X " + platform.mac_ver()[0]
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		
	def GetWinNTInfo(self):
		self.info["OS"] = platform.system()
		self.info["OSVersion"] = self.GetWinNTVersion()
		self.info["Distribution"] = self.GetWinNTProductInfo()
		self.info["Machine"] = platform.machine()
		self.info["Python"] = self.GetPythonInfo()
		
	def GetPythonInfo(self):
		return {"implementation": platform.python_implementation(), "version": platform.python_version() }
		
	def GetWinNTProductInfo(self):
		RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion")
		return _winreg.QueryValueEx(RegistryKey, "ProductName")+" "+_winreg.QueryValueEx(RegistryKey, "CSDVersion")
		
	def GetWinNTVersion(self):
		RegistryKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion")
		return _winreg.QueryValueEx(RegistryKey, "CurrentVersion")
		
	def GetInfo(self):
		return self.info
		
def run():
	_info = OSInfo()
	info = _info.GetInfo()
	print "Operating System:",info["OS"]
	print "Operating System Version:",info["OSVersion"]
	print "Distribution:",info["Distribution"]
	print "Machine:",info["Machine"]
	print "Python:",info["Python"]["implementation"],info["Python"]["version"]

if __name__=='__main__':
	run()
