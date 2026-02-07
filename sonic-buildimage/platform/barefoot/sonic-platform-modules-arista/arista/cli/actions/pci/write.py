from . import getResourcePath
from .. import registerAction
from ...args.pci.write import writeParser
from ....core.log import getLogger
from ....core.utils import MmapResource

logging = getLogger(__name__)

def writePciAddress(device: str, resource: str, address: int,
                    data: int, size: int, verify: bool=False) -> bool:
   path = getResourcePath(device, resource)
   if not path:
      return False

   try:
      with MmapResource(path) as mmapData:
         write = getattr(mmapData, f'write{size}')
         write(address, data)
         if verify:
            read = getattr(mmapData, f'read{size}')
            return read(address) == data
         return False
   except Exception as e: # pylint: disable=broad-except
      logging.error('Cannot read %s device resource: %s', device, str(e))
      return False

@registerAction(writeParser, needsPlatform=False)
def doWrite(ctx, args): # pylint: disable=unused-argument
   return writePciAddress(args.device, args.resource, args.address,
                          args.data, args.size, verify=args.verify)
