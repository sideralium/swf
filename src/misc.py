from subprocess import Popen, PIPE
from os import makedirs, remove
from posixpath import dirname
from urllib.parse import urljoin
from urllib.request import urlopen
from urllib.error import HTTPError
from os.path import join
from hashlib import sha256
from os import getcwd


prefix = join(getcwd())
assets_dir = join(prefix, 'assets')
app_name = 'swf-python-tool'


def download(path):
    url = urljoin('https://darkorbit-22.bpsecure.com', path)

    full_path = join(assets_dir, path)
    makedirs(dirname(full_path), exist_ok=True)

    info('downloading %s' % url)
    f = open(full_path, 'wb')

    try:
        content = urlopen(url).read()
    except HTTPError as err:
        remove(full_path)
        error('http error %d' % err.code)

    f.write(content)
    f.close()

    h = hash(full_path)
    print('\t* sha256: %s' % h)
    return h


def hash(file):
    with open(file, 'rb') as f:
        return sha256(f.read()).hexdigest()


def program_exists(name):
    p = Popen(['/usr/bin/which', name], stdout=PIPE)
    p.communicate()
    return p.returncode == 0


def git_exists():
    return program_exists('git')


def robust_abc_doc(program):
    print('%s is missing\nTo install the required tools to use this script, install robust ' +
          'abc\'s d binaries available here: https://github.com/CyberShadow/RABCDAsm' % program)
    exit(1)


def info(message):
    print('[-] %s' % message)


def error(message):
    print('\033[31m[x] %s\033[0m' % message)
    exit(1)


def warn(message):
    print('\033[31m[!] %s\033[0m' % message)


def ensure_rabcdasm_tools_exists():
    if not program_exists('abcexport'):
        robust_abc_doc('abcexport')

    if not program_exists('rabcdasm'):
        robust_abc_doc('rabcdasm')
