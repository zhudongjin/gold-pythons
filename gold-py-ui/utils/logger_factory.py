import logging


class LoggerFactory:
    # Log文件
    LOGGER_FILE_PATH = "cache/app.log"
    # 全局单例
    GLOBAL_LOGGER = None

    @staticmethod
    def get_logger():
        if LoggerFactory.GLOBAL_LOGGER is not None:
            return LoggerFactory.GLOBAL_LOGGER

        # 创建 logger对象
        LoggerFactory.GLOBAL_LOGGER = logging.getLogger('ROOT')
        # 设置 logger级别
        LoggerFactory.GLOBAL_LOGGER.setLevel(logging.INFO)

        # 创建 handler日志处理器
        fh = logging.FileHandler(LoggerFactory.LOGGER_FILE_PATH, encoding='utf-8')
        # 创建 handler在控制台打印
        ch = logging.StreamHandler()

        # 设置日志输出格式
        # %(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %X"
        )

        # 给 handler设置输出日志格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 为 logger 添加日志处理器
        LoggerFactory.GLOBAL_LOGGER.addHandler(fh)
        LoggerFactory.GLOBAL_LOGGER.addHandler(ch)

        return LoggerFactory.GLOBAL_LOGGER

    @staticmethod
    def add_push_handler(call_back):
        """添加handerl"""
        # 创建 handler推送日志
        ph = LoggerPushHandler(call_back)
        # 设置日志输出格式
        # %(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %X"
        )
        ph.setFormatter(formatter)
        LoggerFactory.GLOBAL_LOGGER.addHandler(ph)


class LoggerPushHandler(logging.Handler):
    """推送到需要的地方"""

    def __init__(self, call_back):
        logging.Handler.__init__(self)
        self.call_back = call_back

    def emit(self, record):
        self.call_back(self.format(record))
        pass


if __name__ == '__main__':
    logger = LoggerFactory.get_logger()
    # 输出日志
    logger.debug('我是 debug')
    logger.warning('我是 warn')
    logger.info('我是 info')
    logger.error('我是 error')
