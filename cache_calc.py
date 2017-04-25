import time
from functools import wraps

from cachetools import LRUCache


class CacheCalc:
    def __init__(self, cache_limit=50):
        self.cache = LRUCache(maxsize=cache_limit)
        self.cache_count = 0
        self.computation_count = 0
        self.max_computation_time = 0.0

    def check_time(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start = time.time()
            result = func(self, *args, **kwargs)
            computation_time = time.time() - start
            if computation_time > self.max_computation_time:
                self.max_computation_time = computation_time
            return result

        return wrapper

    @check_time
    def sum(self, *args):
        arguments = tuple(sorted(args))
        if arguments not in self.cache:
            result = sum(arguments)
            self.cache[arguments] = (result, 1)
            self.computation_count += 1
        else:
            result = self.cache[arguments][0]
            self.cache[arguments] = (result, self.cache[arguments][1] + 1)
            self.cache_count += 1
        return result

    def save_results(self, filename):
        with open(filename, "w+") as results_file:
            results_file.write(self.cache.__str__())

    def show_results(self):
        print("Real computations count - {}".format(self.computation_count))
        print("Cache computations count - {}".format(self.cache_count))
        print("Max sum time - {}".format(self.max_computation_time))


calc = CacheCalc(5)
print(calc.sum(1, 2, 3, 4, 5))
print(calc.sum(2, 3, 1, 4, 5))
print(calc.sum(1, 2, 3, 4, 5))
print(calc.sum(1, 2, 3, 4, 6))
print(calc.sum(1, 2, 3, 4, 6))
print(calc.sum(1, 2, 3, 4, 7))
print(calc.sum(1, 2, 3, 4, 8))
print(calc.sum(1, 2, 3, 4, 9))
print(calc.sum(*list(range(1, 100))))
calc.save_results("test.txt")
calc.show_results()
