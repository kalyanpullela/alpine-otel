from . import filter_api

class RateLimitFilter(filter_api.Filter):
   """
   Filter to limit the rate of change of a value to a maximum threshold.

   Note: if the limit is set to a value less than the diff threshold used by a sensor
         client, rate-of-change warnings in the client will be ineffective.

   :param limit: The maximum delta between adjacent samples.
   """

   def __init__(self, limit: float) -> None:
      super().__init__()

      # The absolute value of the limit is stored since we apply it symmetrically and
      # not having to check the sign simplifies the implementation.
      self.limit = abs(limit)
      self.lastValue = None

   def apply(self, value: float) -> float:
      # Clamp the value to the range [lastValue - limit, lastValue + limit].
      if self.lastValue is not None:
         value = min(self.lastValue + self.limit,
                     max(self.lastValue - self.limit, value))

      self.lastValue = value

      return value

   def reset(self) -> None:
      self.lastValue = None
