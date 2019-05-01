import logging
from api.comon.config import ReadConfig
from api.comon import paths
from api.comon import paths


class Logs():
    # 初始化收集器、输出渠道
    def __init__(self, logge):
        self.readconfig = ReadConfig(paths.log_file)
        self.collect_level = self.readconfig.get('logs', 'collect_level')  # 日志收集级别
        self.output_level = self.readconfig.get('logs', 'output_level')  # 日志输出级别
        self.log_format = self.readconfig.get('logs', 'log_format')  # 日志输出格式
        self.handler = self.readconfig.get('logs', 'handler')  # 日志输出渠道
        # 创建收集器
        self.my_logger = logging.getLogger(logge)
        # 创建文件输出渠道
        self.file_handler = logging.FileHandler(paths.logs_file, 'a', encoding='utf-8')
        # 创建控制台输出渠道
        self.Stream_handler = logging.StreamHandler()
        # 日志输出格式
        self.log_format = logging.Formatter(self.log_format)
        # 设置收集日志级别
        self.my_logger.setLevel(self.collect_level)
        # 判断输出哪种渠道
        if self.handler == 'FileHandler':
            self.file_handler.setLevel(self.output_level)
            self.file_handler.setFormatter(self.log_format)
            # 建立收集器和输出渠道关系
            self.my_logger.addHandler(self.file_handler)
        else:
            self.Stream_handler.setLevel(self.output_level)
            self.Stream_handler.setFormatter(self.log_format)
            self.my_logger.addHandler(self.Stream_handler)

    def getlogs(self, level, msg):
        if 'info' == level:
            self.my_logger.info(msg)
        elif 'debug' == level:
            self.my_logger.debug(msg)
        elif 'warning' == level:
            self.my_logger.warning(msg)
        elif 'error' == level:
            self.my_logger.error(msg)
        else:
            self.my_logger.critical(msg)


if __name__ == '__main__':
    # 创建ConfigParser对象
    config_parter = ConfigParser()
    # 读取配置文件
    config_parter.read('log_level.cfg', encoding='utf-8')
    # 获取指定的值
    file_name = config_parter.get('logs', 'file_name')
    collect_level = config_parter.get('logs', 'collect_level')
    output_level = config_parter.get('logs', 'output_level')
    log_format = config_parter.get('logs', 'log_format')
    handler = config_parter.get('logs', 'handler')
    # 实例化Logs对象
    logs = Logs('py15', file_name, log_format)
    # 调用setlogs方法
    logs.setlogs(collect_level, output_level, handler)
    logs.my_logger.info("This is info")
    logs.my_logger.debug("This is debug")
    logs.my_logger.warning("This is warning")
    logs.my_logger.error("This is error")
    logs.my_logger.critical("This is critical")
