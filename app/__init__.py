import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from config import Config
from app import utils


# Initialize plugins
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_class=Config):
    """Flask application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    utils.safe_make_dir(app.config["LOG_DIR"])

    if not app.debug and app.testing:
        # logging to file
        log_dir = app.config['LOG_DIR']

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('../logs'):
                os.mkdir('../logs')
            file_handler = RotatingFileHandler(
                os.path.join(log_dir, 'ds_recruitment_api.log'),
                maxBytes=10240,
                backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Datasentics Recruitment API startup')

    return app
