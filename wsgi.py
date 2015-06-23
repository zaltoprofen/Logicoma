from logicoma import Logicoma
from configparser import ConfigParser
import logging
import logging.config

logging.config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

conf = ConfigParser()
conf.read('config.ini')
bot = Logicoma(**dict(conf['logicoma']))
app = bot.app
