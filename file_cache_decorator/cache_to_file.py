
from collections import OrderedDict
from os.path import join, exists, getmtime
from sys import stderr
from time import time
from os import makedirs
from pickle import dumps, dump, load
from file_cache_decorator.utils import DEFAULT_CACHE_DIR, hash_func_md5


def cache_to_file(func=None, duration=259200, dir=DEFAULT_CACHE_DIR, mem_limit=1000,
		hash_func=hash_func_md5, ignore_self=False, check_collisions=False, debug_msgs=False):
	"""
	Cache a function return values to memory and to a file.

	:param func: The function that is being decorated.
	:param duration: How long cache is valid for, in seconds.
	:param mem_limit: Maximum number of objects stored in memory cache (file cache is unlimited).
	:param hash_func: Non-cryptographic hash function which takes binary and returns filesystem-safe ascii (default md5).
	:param ignore_self: Ignore the first positional argument (presumably `self`) in cache invalidation.
	:param check_collisions: This makes all the arguments be stored, and checked on retrieval. This prevents wrong results in the case of hash collisions, but imposes a significant performance penalty.

	Assumes that:

	* Each argument is pickle-able.
	* Return value (that's being cached) is pickle-able.
	* Function names are unique.
	* No hash collisions for pickled arguments.

	Can be used as `@cache_to_file` or `@cache_to_file(...)`. Do NOT use positional arguments, only keywords.

	Calling`f(a)` as `f(5)` and then `f(a=5)` will result in a cache-miss (but works fine except for that).
	The same applies for calling `instance.method()` and changing the instance before calling again.
	"""
	if check_collisions:
		raise NotImplementedError('check_collisions not implemented')
	def cache_to_file_decorator(func):
		assert hasattr(func, '__call__'), 'Not a callable: {0:}'.format(func)
		makedirs(dir, exist_ok=True)
		func._CACHE = {}
		func._CACHE_TIME = OrderedDict()
		def cache_or_func(*args, **kwargs):
			use_args = args[1:] if ignore_self else args
			arghash = hash_func(dumps(tuple(use_args) + tuple(sorted(kwargs.items()))))
			for cachekey, cachetime in tuple(func._CACHE_TIME.items()):
				if len(func._CACHE_TIME) < mem_limit and time() - cachetime < duration:
					break
				del func._CACHE[cachekey]
				del func._CACHE_TIME[cachekey]
			if arghash in func._CACHE_TIME:
				if debug_msgs:
					stderr.write('cache hit (memory) for {0:}\n'.format(func))
				return func._CACHE[arghash]
			cache_str = '{f:s}_{arg:}'.format(f=func.__name__, arg=arghash[:12])
			pth = join(dir, '{0:s}.cache'.format(cache_str))
			if exists(pth):
				mtime = getmtime(pth)
				if time() - mtime < duration:
					with open(pth, 'rb') as fh:
						if debug_msgs:
							stderr.write('cache hit (disk) for {0:}\n'.format(func))
						func._CACHE[arghash] = load(fh)
						func._CACHE_TIME[arghash] = mtime
						return func._CACHE[arghash]
			if debug_msgs:
				t0 = time()
				func._CACHE[arghash] = func(*args, **kwargs)
				stderr.write('cache miss for {0:}, took {1:.8f}ms\n'.format(func, 1e3 * (time() - t0)))
			else:
				func._CACHE[arghash] = func(*args, **kwargs)
			func._CACHE_TIME[arghash] = time()
			with open(pth, 'wb+') as fh:
				dump(func._CACHE[arghash], fh)
			return func._CACHE[arghash]
		return cache_or_func
	if func:
		""" Used WITHOUT brackets. """
		return cache_to_file_decorator(func)
	else:
		""" Used WITH brackets. """
		return cache_to_file_decorator


