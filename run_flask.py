import configparser
import logging
import logging.config
from optparse import OptionParser
from logicoma import Logicoma


def main():
    usage = 'usage: %prog [options]'
    parser = OptionParser(usage)
    parser.add_option('-f', '--flask-conf', action='store', default='configs/flask.ini')
    parser.add_option('-L', '--logicoma-conf', action='store', default='configs/logicoma.json')
    parser.add_option('-l', '--logging-conf', action='store', default='configs/logger.ini')
    parser.add_option('--logicoma-token', action='store', default=None)
    parser.add_option('--debug', action='store_true')
    opts, args = parser.parse_args()

    logging.config.fileConfig(opts.logging_conf)

    config = configparser.ConfigParser()
    config.read(opts.flask_conf)
    server_conf = dict(config['flask'])
    server_conf['port'] = int(server_conf.get('port', '7290'))
    other_opts = {}
    if opts.logicoma_token is not None:
        other_opts['token'] = opts.logicoma_token
    if opts.debug:
        other_opts['debug'] = opts.debug
    bot = Logicoma(opts.logicoma_conf, other_opts)
    bot.run(**server_conf)

if __name__ == '__main__':
    main()
