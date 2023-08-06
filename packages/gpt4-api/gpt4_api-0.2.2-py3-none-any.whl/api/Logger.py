import logging


class Logger:
    def __init__(self, name, log_file_name="app.log", log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)  # 设置日志等级

        # 创建日志文件handler并设置等级
        file_handler = logging.FileHandler(log_file_name)
        file_handler.setLevel(log_level)

        # 创建控制台handler并设置等级
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # 定义handler输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加到logger中
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
