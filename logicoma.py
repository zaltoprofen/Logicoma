# -*- coding: utf-8 -*-
from flask import Flask, Response, request, make_response
import json
import logging
import handlers

logger = logging.getLogger(__name__)

class Logicoma(object):

    def __init__(self, config_path='configs/logicoma.json', other_opts={}):
        self.app = Flask('Logicoma')
        self.app.route('/', methods=['post'])(self.hook)
        self.app.route('/', methods=['get'])(lambda:'hello world')
        self.other_opts = other_opts
        self.load_config(config_path)

    def load_config(self, config_path):
        with open(config_path) as fp:
            conf = json.load(fp)
        conf.update(self.other_opts)
        self.token = conf['token']
        self.debug = conf.get('debug', False)
        self.handlers = [handlers.load_from_config(s) for s in conf['handlers']]

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
