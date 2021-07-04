from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('file', choices=['preloader'])
parser.add_argument('-x', '--extract', required=False,
                    default=False, action='store_true')
parser.add_argument('-d', '--disassemble', required=False,
                    default=False, action='store_true')
parser.add_argument('--git-remote-url', required=False, default=False)
args = parser.parse_args()

args_dict = {'preloader': 'spacemap/preloader.swf'}
