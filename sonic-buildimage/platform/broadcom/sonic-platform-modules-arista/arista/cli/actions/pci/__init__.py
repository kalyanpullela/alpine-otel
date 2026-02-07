import os
from typing import Optional

from .. import registerAction
from ...args.pci import pciParser
from ....core.log import getLogger

logging = getLogger(__name__)

DEVICE_SYSFS_ROOT = '/sys/bus/pci/devices'

def getDeviceSysfsPath(device: str) -> str:
   return os.path.join(DEVICE_SYSFS_ROOT, device)

def getResourcePath(device: str, resource: str) -> Optional[str]:
   devicePath = getDeviceSysfsPath(device)
   if not os.path.isdir(devicePath):
      logging.error('Device %s does not exist or is not loaded', device)
      return None

   try:
      with open(os.path.join(devicePath, 'enable'), 'r', encoding='utf-8') as f:
         if f.read().strip() != '1':
            logging.error('Device %s is not enabled', device)
            return None
   except IOError:
      logging.error('Cannot read %s device sysfs', device)

   path = os.path.join(devicePath, f'resource{resource}')
   if not os.path.exists(path):
      logging.error('BAR resource %d for device %s does not exist', device, resource)
      return None

   return path

@registerAction(pciParser)
def doPci(ctx, args) -> None: # pylint: disable=unused-argument
   pass
