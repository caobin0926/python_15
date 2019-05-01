import re
import configparser
from api.comon.config import ReadConfig
from api.comon import paths


class TestData:
    loan_id = None
    invest_id = None
    loaner_id = None


# 定义一个替换字符串中每个字符的函数
def replace(data, file_name, section):
    conf = ReadConfig(file_name)
    data1 = data
    while re.search('%(.*?)%', data1):
        result = re.search('%(.*?)%', data1)
        g = result.group(1)
        try:
            ms = conf.get(section, g)
        except configparser.NoOptionError as e:
            ms = str(getattr(TestData, g))
        finally:
            data1 = re.sub('%.*?%', ms, data1, count=1)
    return data1


if __name__ == '__main__':
    data = "{'mobilephone':'%loan_cell%','pwd':'%loan_pwd%'}"
    data1 = replace(data, paths.gloads_file, 'api')
    print(data1)
