import logging.config
import os

from flask import Flask

from flask_cors import CORS
from flask_rbac import RBAC
from config import dict_logger
from .userservices import user_service
from .seatservices import seat_service

rbac = RBAC()


def create_app(config_name):
    app = Flask(__name__,
                static_url_path='/static',
                )
    # 跨域名
    app.debug = False
    CORS(app, supports_credentials=True)
    logging.config.dictConfig(dict_logger)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.register_blueprint(seat_service, url_prefix='/seat/')
    app.register_blueprint(user_service, url_prefix='/user/')
    app.config['RBAC_USE_WHITE'] = True
    rbac.init_app(app)
    return app
