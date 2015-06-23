import json
import random
import re

def load_from_config(section):
    if section.get('type') == 'json':
        filepath = section['file_path']
        return JSONDefinedHandler(filepath)
    raise ValueError()

class DictDefinedHandler(object):
    def __init__(self, definition={}):
        self.pattern = re.compile(definition.get('pattern', '*'))
        self.candidates = definition.get('candidates', [])
        self.default = definition.get('default', {})

    def handle(self, text):
        if self.pattern.match(text) is None:
            return None
        res = self.default.copy()
        if len(self.candidates) > 0:
            res.update(random.sample(self.candidates, 1))
        return res

class JSONDefinedHandler(object):
    def __init__(self, filename):
        with open(filename) as fp:
            s = json.load(fp)
        self.delegate = DictDefinedHandler(s)

    def handle(self, text):
        return self.delegate.handle(text)
