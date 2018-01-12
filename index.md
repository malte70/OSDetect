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

```python
# Get a dict containing all gathered information
from OSDetect import info as os_info
print(os_info.getInfo())

# Get a specific value
print("Distribution:   "+os_info.getDistribution())
# or using the dict key (a dot means a dict containing a dict)
print("Python.Version: "+os_info.get("Python.Version"))
```

On a ArchLinux system, it looks like this:

```python
{
	'Distribution': 'Arch Linux',
	'Machine': 'i686',
	'OS': 'Linux',
	'OSVersion': '4.14.11-1.0-ARCH',
	'Python': {
		'Implementation': 'CPython',
		'Version': '3.6.4'
	}
}

ArchLinux
Python.Version: 3.6.4
```

