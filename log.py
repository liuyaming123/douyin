import logging

import time
import os

# 设置日志的根目录
root_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(root_dir, "logs")

if not os.path.exists(log_dir):
    os.mkdir(log_dir)


class DemoLogger():
    def __init__(self):
        # 创建一个日志器
        self.logger = logging.getLogger("logger")

        # 设置日志输出的最低等级,低于当前等级则会被忽略
        self.logger.setLevel(logging.INFO)

        # 创建处理器;sh为控制台处理器;fh为文件处理器
        sh = logging.StreamHandler()

        # 创建处理器;sh为控制台处理器;fh为文件处理器,log_file为日志存放的文件夹
        log_file = os.path.join(log_dir, f'{time.strftime("%Y_%m_%d", time.localtime())}.log')
        # log_file = os.path.join(log_dir, "autotest.log")
        fh = logging.FileHandler(log_file, encoding='utf-8')

        # 创建格式器,并将sh、fh设置对应的格式
        formator = logging.Formatter(fmt='%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
        # sh.setFormatter(formator)
        fh.setFormatter(formator)

        # 将处理器添加至日志器中
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


logger = DemoLogger().logger

