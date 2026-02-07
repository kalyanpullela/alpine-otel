from ...tests.testing import unittest

from ..log_helper import LazyArgsStr

class LogHelperTest(unittest.TestCase):
   def testLazyArgsStrSimple(self):
      self.assertEqual('0x22, 0x24', str(LazyArgsStr([34, 36], {})))

   def testLazyArgsStrList(self):
      self.assertEqual('[34, 36]', str(LazyArgsStr([[34, 36]], {})))

   def testLazyArgsKwargs(self):
      self.assertEqual('a=34, b=36', str(LazyArgsStr([], {'a': 0x22, 'b': 0x24})))

   def testLazyArgsBothArgsAndKwargs(self):
      self.assertEqual('0x22, a=36', str(LazyArgsStr([34], {'a': 0x24})))
