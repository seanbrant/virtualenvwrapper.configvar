import logging
import os


log = logging.getLogger(__name__)


def trim(*values):
    return [value.strip() for value in values]


class Loader(object):
    _old_prefix = '__OLD_'
    _exported_key = '__EXPORTED'

    def __init__(self):
        self._exported = []
        self._source_lines = []

    def load(self, path):
        try:
            with open(path, 'r') as env:
                self._parse(env.read())
        except IOError:
            log.info('Skip loading environment. %s does not exist.' % path)

    def clear(self):
        for key, value in os.environ.items():
            if key.startswith(self._old_prefix):
                self._unset(key)
                self._export(''.join(key.split(self._old_prefix)[1:]), value)

        for key in os.environ.get(self._exported_key, '').split(','):
            if key:
                self._unset(key)

        self._unset(self._exported_key)

    def source(self):
        if self._exported:
            self._export(self._exported_key, ','.join(self._exported))

        content = '\n'.join(self._source_lines)

        self._source_lines = []
        self._exported = []

        return content

    def _parse(self, content):
        lines = content.splitlines()
        pairs = [trim(*line.split('=')) for line in lines if line.strip()]

        for key, value in pairs:
            if key in os.environ:
                self._export('%s%s' % (self._old_prefix, key), os.environ[key])

            self._export(key, value)

    def _export(self, key, value):
        self._exported.append(key)
        self._source_lines.append('export %s=%s' % (key, value))

    def _unset(self, key):
        self._source_lines.append('unset %s' % key)


loader = Loader()


def pre_activate(args):
    project = args[0]
    base = os.environ.get('PROJECT_HOME', os.environ.get('WORKON_HOME'))
    loader.load(os.path.join(base, project, '.env'))


def pre_activate_source(args):
    return loader.source()


def post_deactivate(args):
    loader.clear()


def post_deactivate_source(args):
    return loader.source()
