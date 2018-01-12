import os
import OSDetect

def test_get_os():
	OS             = OSDetect.info.getOS()
	TRAVIS_OS_NAME = os.getenv("TRAVIS_OS_NAME")
	
	if TRAVIS_OS_NAME is None:
		assert isinstance(OS, str)
		
	elif TRAVIS_OS_NAME == "linux":
		assert OS.lower() == TRAVIS_OS_NAME.lower()
		
