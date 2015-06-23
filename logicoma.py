# -*- coding: utf-8 -*-
from flask import Flask, Response, request, make_response
import json
import configparser
import sys
import logging
import handlers

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Logicoma(object):

    def __init__(self, config_path='logicoma.ini'):
        self.app = Flask('Logicoma')
        self.app.route('/', methods=['post'])(self.hook)
        self.app.route('/', methods=['get'])(lambda:'hello world')
        self.load_config(config_path)

    def load_config(self, config_path):
        conf = configparser.ConfigParser()
        conf.read(config_path)
        c = conf['logicoma']
        self.token = c['token']
        self.debug = c.getboolean('debug')
        handler_names = map(lambda s: s.strip(), c['handlers'].split(','))
        sections = map(lambda name: conf['handler_%s' % name], handler_names)
        self.handlers = [handlers.load_from_config(s) for s in sections]

    def run(self, *args, **kwargs):
        return self.app.run(*args, **kwargs)

    def dispatch(self, text):
        for h in self.handlers:
            response = h.handle(text)
            if response is not None:
                response_json = json.dumps(response)
                return (response_json, 200, {'Content-Type': 'application/json'})
        return ('', 200, {})

    def hook(self):
        try:
            payload = request.form
            logger.debug("payload: %s", payload)
            if self.debug or payload and payload.get('token') == self.token:
                if 'text' in payload and payload.get('user_id') != 'USLACKBOT':
                    return make_response(self.dispatch(payload.get('text')))
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
    bot = Logicoma()
    bot.run(**server_conf)

if __name__ == '__main__':
    main()
