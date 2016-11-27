
# todo: make actual unit tests

from os.path import join
from tempfile import gettempdir
from file_cache_decorator import cache_to_file


@cache_to_file(mem_limit=3)
def myfun(a, b):
	return a + b


class MyCls(object):
	def __init__(self, q=-1):
		self.q = q
	
	@cache_to_file
	def myfun(self, a, b):
		return a + b + self.q

	@cache_to_file(ignore_self=True, debug_msgs=True)
	def myfun2(self, a, b):
		return a + b - self.q


print(myfun(8, 5))
print(myfun(5, 8))
print(myfun(5, 8))
print(myfun(5, b=8))
print(myfun(a=5, b=8))
print(myfun(a=5, b=8))
print(myfun(a=5, b=7))

print('---')
inst = MyCls()
print(inst.myfun(8, 5))
print(inst.myfun(8, 5))
inst2 = MyCls(q=8)
print(inst2.myfun(8, 5))
print(inst2.myfun(8, 5))
inst2.q = 17
print(inst2.myfun(8, 5))

print('---')
print(inst2.myfun2(8, 5))
inst2.q = -4
print(inst2.myfun2(8, 5))


