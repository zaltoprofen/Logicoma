# -*- coding: utf-8 -*-
from flask import Flask, Response, request, make_response
import json
import configparser
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Logicoma(object):

    def __init__(self, token):
        self.app = Flask('Logicoma')
        self.app.route('/', methods=['post'])(self.hook)
        self.app.route('/', methods=['get'])(lambda:'hello world')
        self.token = token
        self.listen_thread = None

    def run(self, *args, **kwargs):
        return self.app.run(*args, **kwargs)

    def handle(self, text):
        return ('', 200, {})

    def hook(self):
        try:
            payload = request.form
            logger.debug("payload: %s", payload)
            if payload and payload.get('token') == self.token:
                if 'text' in payload and payload.get('user_id') != 'USLACKBOT':
                    return make_response(self.handle(payload.get('text')))
                else:
                    return Response(status=200)
            else:
                return Response(status=400)
        except:
            logger.exception('got exception on handler')
            return Response(status=500)

def main(args=sys.argv[1:]):
    config = configparser.ConfigParser()
    config.read('flask.ini')
    server_conf = dict(config['flask'])
    server_conf['port'] = int(server_conf.get('port', '7290'))
    config = configparser.ConfigParser()
    conf = dict(config['logicoma'])
    bot = Logicoma(**conf)
    bot.run(**server_conf)

if __name__ == '__main__':
    main()
