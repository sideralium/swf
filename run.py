#!/bin/env python3

""" this program is used to extract abc code from a swf file """

from os.path import exists

from src.file import File
from src.misc import ensure_rabcdasm_tools_exists
from src.args import args, args_dict
from src.swf import SWF


def init():
    file = File(args_dict.get(args.file))
    file.download()

    swf = SWF(file)
    print('\t* size: %d bytes' % swf.size())
    print('\t* version: %d' % swf.version())
    if swf.compressed:
        print('\t* compressed')

    if args.extract:
        file.extract()

    if args.disassemble:
        if not exists(file.abc):
            file.extract()
        file.disassemble()

    if args.git_remote_url and 'origin' not in file.repository.remotes:
        file.repository.create_remote('origin', args.git_remote_url)


if __name__ == '__main__':
    ensure_rabcdasm_tools_exists()
    init()
