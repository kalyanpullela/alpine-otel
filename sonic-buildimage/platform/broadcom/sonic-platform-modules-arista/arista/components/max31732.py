
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.max31732 import Max31732KernelDriver

class Max31732(I2cComponent):
   DRIVER = Max31732KernelDriver
   PRIORITY = Priority.THERMAL
