from api.comon import paths
import pytest
import sys
sys.path.append('./')
# print(sys.path)
pytest.main(["-s", "--alluredir", "../\\report"])

