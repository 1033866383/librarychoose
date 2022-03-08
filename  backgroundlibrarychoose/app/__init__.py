import logging, logging.config
from flask import Flask
from flask_cors import CORS
from config import logger_dict


def create_app(config_name):
    app = Flask(__name__,
                static_url_path='/static',
                )
    # 跨域名
    CORS(app, supports_credentials=True)
    app.debug = False
    logging.config.dictConfig(logger_dict)
    logger = logging.getLogger(u'root')
    from .userservices import user_service
    from .seatservices import seat_service
    app.register_blueprint(seat_service, url_prefix='/seat/')
    return app
