from ..core.driver.kernel.i2c import I2cKernelDriver

class Pali2FanCpldKernelDriver(I2cKernelDriver):
   MODULE = 'minke-fan-cpld'
   NAME = 'pali2_cpld'
