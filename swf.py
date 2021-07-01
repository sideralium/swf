#!/bin/env python3

""" this program is used to extract abc code from a swf file """

from __future__ import print_function
from genericpath import exists
from os import makedirs, getcwd, remove
from os.path import join
from posixpath import basename, dirname, splitext
from urllib.parse import urljoin
from urllib.request import urlopen
from subprocess import Popen, PIPE
from urllib.error import HTTPError
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('file', choices=['preloader', 'expressInstall', 'main'])
parser.add_argument('-x', '--extract', required=False, default=False, action='store_true')
parser.add_argument('-d', '--disassemble', required=False, default=False, action='store_true')
args = parser.parse_args()

prefix = join(getcwd())
assets_dir = join(prefix, 'assets')


def download(path):
    url = urljoin('https://darkorbit-22.bpsecure.com', path)

    full_path = join(assets_dir, path)
    makedirs(dirname(full_path), exist_ok=True)
    if exists(full_path):
        print('[-] skipping the download of %s.swf, already has it' % args.file)
        return

    print('[-] downloading %s' % url)
    f = open(full_path, 'wb')

    try:
        content = urlopen(url).read()
    except HTTPError as err:
        remove(full_path)
        print(err)
        exit(1)

    f.write(content)
    f.close()


class File:
    def __init__(self, path):
        self.path = path

        s, ext = splitext(path)
        if ext != '.swf':
            print('[!] handling a non-swf file (%s)' % ext)

        bn = basename(s)
        self.abc = join(assets_dir, '%s-0.abc' % s)
        self.asasm_dir = join(assets_dir, '%s-0' % s)
        self.asasm = join(self.asasm_dir, '%s-0.main.asasm' % bn)

    def download(self):
        download(self.path)

    def extract_abc(self):
        if exists(self.abc):
            return 0
        p = Popen(['abcexport', join(assets_dir, self.path)])
        p.communicate()
        return p.returncode

    def disassemble_abc(self):
        if exists(self.asasm):
            return 0
        p = Popen(['rabcdasm', self.abc])
        p.communicate()
        return p.returncode

def program_exists(name):
    p = Popen(['/usr/bin/which', name], stdout=PIPE)
    p.communicate()
    return p.returncode == 0


def git_exists():
    return program_exists('git')


def init():
    if not program_exists('abcexport'):
        robust_abc_doc('abcexport')

    if not program_exists('rabcdasm'):
        robust_abc_doc('rabcdasm')


def robust_abc_doc(program):
    print('%s is missing\nTo install the required tools to use this script, install robust ' +
          'abc\'s d binaries available here: https://github.com/CyberShadow/RABCDAsm' % program)
    exit(1)

def extract(file):
    print('[-] extracting %s.swf' % args.file)
    if file.extract_abc() > 0:
        print('[x] an error occured while extracting abc from %s.swf' % args.file)

def disassemble(file):
    print('[-] disassembling %s.swf' % args.file)
    if file.disassemble_abc() > 0:
        print('[x] an error occured while disassembling %s.swf\'s abc' % args.file)


dict = {"preloader": "spacemap/preloader.swf", "main": "spacemap/main.swf", "expressInstall": "swf_global/expressInstall.swf"}

init()
file = File(dict.get(args.file))
file.download()

if args.extract:
    extract(file)

if args.disassemble:
    if not exists(file.abc):
        extract(file)
    disassemble(file)
