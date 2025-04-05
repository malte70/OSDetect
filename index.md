---
title: OSDetect
---

What is OSDetect?
-----------------

OSDetect is a small python module which is able to get
some information about your system and your Python
installation, like the Operating System or the CPU
architecture.

Supported operating systems
---------------------------

The following iperating systems are supported:

- GNU/Linux
- mac OS
- FreeBSD
- Windows
- Windows/Cygwin

Please keep in mind that the available information
may differ on the different platforms.

Installation instructions
-------------------------

You can install OSDetect from PyPI using pip:

```sh
pip install OSDetect
```

Alternatively clone the Git repository and install
directly from the source code:

```sh
git clone "https://github.com/malte70/OSDetect"
cd OSDetect
pip install .
```

Command Line Usage
------------------

OSDetect includes a function which is executed if the
module is directly executed. So give it a try and run:

```sh
python -m OSDetect
```

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

The output of course depends on your system, but it
should look similar to this:

```
{'Distribution': 'Mac OS X 15.4',
 'Machine': 'arm64',
 'OS': 'Darwin',
 'OSVersion': '24.4.0',
 'Python': {'Implementation': 'CPython', 'Version': '3.13.2'}}

Distribution:   Mac OS X 15.4
Python.Version: 3.13.2
```

