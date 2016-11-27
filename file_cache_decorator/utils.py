
from base64 import urlsafe_b64encode
from os.path import join
from tempfile import gettempdir
from hashlib import md5


DEFAULT_CACHE_DIR = join(gettempdir(), 'cache_to_file')


def hash_func_md5(bin):
	"""
	Calculates the md5 hash of a binary 'string', as a filesystem-safe string.
	"""
	return str(urlsafe_b64encode(md5(bin).digest()), 'ascii')


