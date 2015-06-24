import re

class ReverserHandler(object):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def handle(self, text):
        m = self.pattern.match(text)
        if m is not None:
            r = text[:m.end()-1:-1]
            return {'username': 'Logicoma', 'text': str(r), 'icon_emoji': ':logicoma:'}
