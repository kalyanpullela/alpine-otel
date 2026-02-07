from ...tests.testing import unittest
from ..filters import ratelimit


class FilterTest(unittest.TestCase):
   def testRateLimit(self):
      filt = ratelimit.RateLimitFilter(10.0)

      # First value passed to the filter should be returned unchanged.
      self.assertEqual(filt.apply(42.), 42.)

      # A big swing for the next value should be rate-limited.
      self.assertEqual(filt.apply(30.), 32.)

      # The next value should be limited according to the last value returned, not
      # the last input.
      self.assertEqual(filt.apply(21.), 22.)

      # A change below the rate limit should be returned unmodified.
      self.assertEqual(filt.apply(30.), 30.)

      # A change equal to the rate limit should be returned unmodified.
      self.assertEqual(filt.apply(40.), 40.)

      # Resetting the filter should allow for a swing of any size.
      filt.reset()
      self.assertEqual(filt.apply(20.), 20.)


if __name__ == '__main__':
   unittest.main()
