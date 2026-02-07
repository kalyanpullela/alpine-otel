from argparse import ArgumentParser

from .. import registerParser
from ..default import defaultPlatformParser

@registerParser('pci', parent=None,
                help='PCIe debug commands')
def pciParser(parser: ArgumentParser) -> None: # pylint: disable=unused-argument
   pass
