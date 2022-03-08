__all__ = ["config", "logger_dict"]

config = {

}

# logging.py
logger_dict = {
    'version': 1,
    'formatters': {
        'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s', }
    },
    # 设置处理器
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'level': 'DEBUG'
        }},
    # 设置root日志对象配置
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    },
    # 设置其他日志对象配置
    'loggers': {
        'test':
            {'level': 'DEBUG',
             'handlers': ['wsgi'],
             'propagate': 0}
    }
}
