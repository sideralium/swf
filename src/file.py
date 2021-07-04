from posixpath import basename, splitext
from os.path import join, exists
from git import Repo
from subprocess import Popen

from .project import random_name
from .misc import download, info, git_exists, error, assets_dir, warn
from .args import args


class File:
    def __init__(self, path):
        self.path = path

        s, ext = splitext(path)
        if ext != '.swf':
            warn('handling a non-swf file (%s)' % ext)

        bn = basename(s)
        self.swf = join(assets_dir, self.path)
        self.abc = join(assets_dir, '%s-0.abc' % s)
        self.asasm_dir = join(assets_dir, '%s-0' % s)
        self.asasm = join(self.asasm_dir, '%s-0.main.asasm' % bn)

        if exists(join(self.asasm_dir, '.git')):
            self.repository = Repo(self.asasm_dir)

    def download(self):
        self.hash = download(self.path)
        self.project_name = random_name(self.hash)
        print('\t* random project name: %s' % self.project_name)

    def extract(self):
        info('extracting %s.swf' % args.file)
        if exists(self.abc):
            return
        p = Popen(['abcexport', self.swf])
        p.communicate()
        if p.returncode > 0:
            error('an error occured while extracting abc from %s.swf' % args.file)

    def disassemble(self):
        info('disassembling %s.swf' % args.file)
        if exists(self.asasm):
            return
        p = Popen(['rabcdasm', self.abc])
        p.communicate()
        if p.returncode > 0:
            error('an error occured while disassembling %s.swf\'s abc' % args.file)
        self.git_init()

    def git_init(self):
        if not git_exists():
            return

        if not exists(join(self.asasm_dir, '.git')):
            self.repository = Repo.init(
                self.asasm_dir, mkdir=False, initial_branch=self.project_name)

        if self.repository.is_dirty(untracked_files=True):
            self.repository.index.add(self.repository.untracked_files)
            self.repository.index.commit('init')
