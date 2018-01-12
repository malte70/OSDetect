import OSDetect

def test_get_info_is_dict():
	assert isinstance(OSDetect.info.getInfo(), dict)
	
def test_get_function_os_is_string():
	assert isinstance(OSDetect.info.get("OS"), str)
	
def test_get_function_python_is_dict():
	assert isinstance(OSDetect.info.get("Python"), dict)
	
def test_get_function_python_dict_keys():
	keys = OSDetect.info.get("Python").keys()
	assert "Implementation" in keys and "Version" in keys and len(keys) == 2
	
def test_get_os_is_string():
	assert isinstance(OSDetect.info.getOS(), str)
	
