OSDetect README
===============

What is OSDetect?
-----------------

OSDetect is a small python module which is able to get some information
about your system and python implementation, like the Operating System
or the hardware platform.

Supported operating systems
---------------------------

As of now, only GNU/Linux, Mac OS X, Windows NT and Windows NT/Cygwin are supported. At the
moment, I'm working on support for a wider range of operating systems.

Since version 1.1.0, Python 2 and Python 3 are both supported.

Note that the information available on the different platforms may differ.

Installation instructions
-------------------------

Since OSDetect uses setuptools, you simply need to run

	python setup.py install

Command Line Usage
------------------

OSDetect includes a function which is executed if the module is directly called. So give it
a try and run:

	python -m OSDetect

Example uses of the module
--------------------------

	# Get information on a GNU/Linux system
	print(OSDetect.info)

On a ArchLinux box, this results in:

	{
		'Python': {
			'version': '3.4.2',
			'implementation': 'CPython'
		},
		'Machine': 'i686',
		'OSVersion': '3.14.30-1-lts',
		'Distribution': 'arch Arch Linux',
		'OS': 'Linux'
	}


