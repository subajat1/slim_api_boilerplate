from crypt import methods
from flask import (
    Flask,
    jsonify,
    request,
)
from dotenv import load_dotenv
from os.path import isfile
from logging import basicConfig
from logging.config import dictConfig
from time import strftime

import os
import yaml
import traceback
import logging


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))

debug = True


def configure_logger(log_config='app/logging.yaml'):
    """Configure the logging subsystem"""
    if not isfile(log_config):
        return basicConfig()

    with open(log_config) as fh:
        log_config = yaml.safe_load(fh)
        return dictConfig(log_config)


TEMPLATES_DIR = os.path.join(basedir, 'templates')


def create_app(name: str = __name__) -> Flask:
    configure_logger()
    app = Flask(
            name,
            template_folder=TEMPLATES_DIR,
            instance_relative_config=True,)

    return app


app = create_app()


@app.route('/', methods=['POST'])
def hello_world():
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')

    return jsonify(hello='world')


@app.after_request
def after_request(response):
    info = f'[INFO] {request.remote_addr} {request.method} \
            {request.scheme} {request.full_path} {response.status}'
    app.logger.info(info)
    app.logger.info(f'[REQ] {request.get_json(force=True)}')
    app.logger.info(f'[RES] {response.data}')
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    app.logger.error('%s %s %s %s %s\n%s',
                     timestamp,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb,)
    return e


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
