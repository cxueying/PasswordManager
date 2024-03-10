import logging
from logging.handlers import TimedRotatingFileHandler
from config import constants
from pathlib import Path
import datetime


class Log():
    
    def __init__(self):
        self.logger = logging.getLogger("psdLogger")
        self.__logger_init()
        
    def __add_time_file_handler(self):
        # 输出到文件
        # 创建日志处理器
        filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        # 确保目录 logs 存在
        if not Path(constants.LOGS_LOCATION).exists():
            Path(constants.LOGS_LOCATION).mkdir()
            
        handler = TimedRotatingFileHandler(Path(constants.LOGS_LOCATION, filename), when="midnight", encoding='utf-8')
        handler.setLevel(logging.DEBUG)
        
        # 定义处理器输出格式
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - File \"%(pathname)s\", line %(lineno)d: %(message)s")
        handler.setFormatter(formatter)
        
        # 给 logger 添加handler
        self.logger.addHandler(handler)
        
        
    def __add_console_handler(self):
        # 创建日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # 定义处理器输出格式
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - File \"%(pathname)s\", line %(lineno)d: %(message)s")
        console_handler.setFormatter(formatter)
        
        # 给 logger 添加handler
        self.logger.addHandler(console_handler)
        
    
    def __logger_init(self):
        # 设置日志器级别
        self.logger.setLevel(logging.DEBUG)
        
        # 添加日志处理器
        self.__add_time_file_handler()
        # self.__add_console_handler()


log = Log().logger
log.debug("日志器初始化成功！")