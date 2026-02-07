from ..core.component.i2c import I2cComponent
from ..drivers.pca954x import Pca9548KernelDriver

class Pca954x(I2cComponent):

   def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.buses = {}

   def getBus(self, channel):
      bus = self.buses.get(channel)
      if bus is None:
         bus = self.driver.getBus(channel)
         self.buses[channel] = bus
      return bus

class Pca9548(Pca954x):
   DRIVER = Pca9548KernelDriver
