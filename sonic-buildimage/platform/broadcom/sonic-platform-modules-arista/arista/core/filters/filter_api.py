import abc


class Filter(abc.ABC):
   """
   Abstract class for implementing sensor value filters.
   """
   @abc.abstractmethod
   def apply(self, value: float) -> float:
      ...

   @abc.abstractmethod
   def reset(self) -> None:
      ...
