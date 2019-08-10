# coding = utf-8
import os
import logging.config
import datetime

log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '/log/')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_name = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
log_path = os.path.join(log_dir + log_name)

dictLogConfig = {
    "version": 1,
    'disable_existing_loggers': True,
    "formatters":
        {
            "myFormatter": {
                "format": '%(asctime)s [%(levelname)s] -- [%(filename)s:%(funcName)s] -- message:%(message)s'
            },
            "errorFormatter": {
                "format": '%(message)s'
            },
        },
    "handlers":
        {
            # 打印到终端日志
            "consoleHandler": {
                "class": "logging.StreamHandler",  # 打印到控制台
                "formatter": "myFormatter"
            },
            'default_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_path,
                # 若是添加如下两项配置，日志不能重写，每次都是追加
                # 'maxBytes': 1024*1024*5,
                # 'backupCount': 5,
                'formatter': 'myFormatter',
                'encoding': 'utf-8',
                # w为每次重写，a是追加
                'mode': 'w',
            },
            'error_handler': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_path,
                # 若是添加如下两项配置，日志不能重写，每次都是追加
                # 'maxBytes': 1024*1024*5,
                # 'backupCount': 5,
                'formatter': 'errorFormatter',
                # w为每次重写，a是追加
                'mode': 'w',
            }
        },
    "loggers":
        {
            'default.logger': {
                'handlers': ['default_handler', 'consoleHandler'],
                'level': 'DEBUG',
                'propagate': True
            },
            'error.logger': {
                'handlers': ['error_handler'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
}

###########################################################################
## 全局环境变量
###########################################################################
# 日志模块的加载
logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger('default.logger')
logger_error = logging.getLogger('error.logger')
