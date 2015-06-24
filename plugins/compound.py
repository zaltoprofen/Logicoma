import re
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import logging

log = logging.getLogger(__name__)

class ZincHandler(object):
    def __init__(self):
        self.pattern = re.compile('^compound:([a-zA-Z0-9]+)$')

    def handle(self, text):
        try:
            return self._handle(text)
        except HTTPError:
            return {'username': 'Logicoma',
                    'text': '対象の検索結果，見つかりませんでした〜',
                    'icon_emoji': ':logicoma:'}
        except:
            log.exception('ZincHandler:handle: catch unexcepted error')
            return {'username': 'Logicoma',
                    'text': '検索に失敗しました〜',
                    'icon_emoji': ':logicoma:'}

    def _handle(self, text):
        m = self.pattern.match(text)
        if m is not None:
            query = m.groups()[0]
            url = 'http://zinc.docking.org/synonym/%s' % query
            log.info('querying to %s', url)
            with urlopen(url) as f:
                bs = BeautifulSoup(f)
            img = bs.find('img', class_='molecule')
            src = img.attrs['src']
            return {'username': 'Logicoma',
                    'text': '%sでの検索結果です！<http:%s>' % (query, src),
                    'icon_emoji': ':logicoma:'}
