"""
定义读取配置文件类
"""
import configparser
from api.comon import paths


class ReadConfig:
    def __init__(self, file_name):
        self.conf = configparser.ConfigParser()  # 实例化ConfigParser对象
        self.conf.read(file_name, encoding='utf-8')  # 加载配置文件
        if 'switch' in self.conf.sections() and self.conf.getboolean('switch', 'on'):
            # print(self.conf.getboolean('switch', 'on'))
            self.conf.read(paths.dedug_file, encoding='utf-8')
        else:
            self.conf.read(file_name, encoding='utf-8')

    def get(self, section, option):
        return self.conf.get(section, option)


# conf = ReadConfig()

if __name__ == '__main__':
    read = ReadConfig()
    print(read.get('api', 'url'))
