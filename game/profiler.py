import time
from functools import wraps
from game.constants import function_names
from collections import defaultdict


class Profiler():
  def __init__(self):
    self.reset_profiler()

  def profile_function(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
      start_time = time.time()
      result = func(self,*args, **kwargs)
      elapsed_time = time.time() - start_time

      self.profiler.profile_data[func.__name__]["total_time"] += elapsed_time
      self.profiler.profile_data[func.__name__]["call_count"] += 1

      return result

    return wrapper

  def print_profile_summary(self):
    print(f"\n{'-' * 10} Chess Engine Profiling Summary {'-' * 10}")
    print("{:<20} {:<15} {:<15}".format("Function Name", "Call Count", "Total Time (s)"))
    print("-" * 52)

    for func_name, data in self.profile_data.items():
      print("{:<20} {:<15} {:<15.3f}".format(func_name, data["call_count"], data["total_time"]))

    print("-" * 52)

  def reset_profiler(self):
    def default_profiling_data():
      return {"total_time": 0, "call_count": 0}

    self.profile_data = defaultdict(default_profiling_data, {name: default_profiling_data() for name in function_names})