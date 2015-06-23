import json
import random
import re
import logging

log = logging.getLogger(__name__)

def load_from_config(section):
    log.debug('loading %s', section)
    if section.get('type') == 'json':
        filepath = section['file_path']
        return JSONDefinedHandler(filepath)
    raise ValueError()

class DictDefinedHandler(object):
    def __init__(self, definition={}):
        log.debug('constructing DictDefinedHandler: %s', definition)
        self.pattern = re.compile(definition.get('pattern', '*'))
        self.candidates = definition.get('candidates', [])
        self.default = definition.get('default', {})

    def handle(self, text):
        log.debug('handling: %s', text)
        if self.pattern.match(text) is None:
            return None
        log.debug('match: %s', text)
        res = self.default.copy()
        if len(self.candidates) > 0:
            res.update(random.sample(self.candidates, 1)[0])
        log.info('responding: %s', res)
        return res

class JSONDefinedHandler(object):
    def __init__(self, filename):
        with open(filename) as fp:
            s = json.load(fp)
        self.delegate = DictDefinedHandler(s)

    def handle(self, text):
        return self.delegate.handle(text)
