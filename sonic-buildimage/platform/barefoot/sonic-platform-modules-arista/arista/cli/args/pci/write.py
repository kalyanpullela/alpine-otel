from argparse import ArgumentParser
from functools import partial

from . import pciParser
from .. import registerParser

@registerParser('write', parent=pciParser,
                help='write PCIe resource memory')
def writeParser(parser: ArgumentParser) -> None:
   parser.add_argument('--size', '-s', type=int, default=32, choices=[8, 16, 32],
                       help='Size of memory value to write')
   parser.add_argument('--resource', '-r', type=int, default=0,
                        help='BAR resource to write')
   parser.add_argument('--verify', '-V', action='store_true', default=False,
                       help='Read back memory value for verification, do not use '
                       'for clear-on-read registers')
   parser.add_argument('device', type=str,
                       help='PCIe device to write')
   parser.add_argument('address', type=partial(int, base=0),
                       help='Address to write')
   parser.add_argument('data', type=partial(int, base=0),
                       help='Data value to write to PCIe memory')
