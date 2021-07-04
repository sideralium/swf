from os.path import join

from .file import File
from .misc import assets_dir, error


class SWF:
    def __init__(self, file: File) -> None:
        self.file = file

        with open(join(assets_dir, self.file.path), 'rb') as f:
            self.header = f.read(8)

        if not self.valid():
            error('downloaded file is not a swf file')

    def valid(self) -> bool:
        fb = self.header[:1]
        if fb == b'F':
            self.compressed = False
        elif fb == b'C' or fb == b'Z':
            self.compressed = True
        else:
            error('swf file\'s first byte has a bad signature: %s' % fb)

        if fb == b'Z':
            self.lzma = True

        return self.header[1:3] == b'WS'

    def version(self) -> int:
        return int.from_bytes(self.header[3:4], 'big')

    def size(self) -> int:
        return int.from_bytes(self.header[4:8], 'little')
