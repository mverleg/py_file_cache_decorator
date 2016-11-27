
Python file cache decorator
===============================

A simple decorator that caches function return values to memory and to files, so that they are fast preserved between runs.

.. code-block:: python

    @cache_to_file
    def myfun(a, b):
        return a + b

    print(myfun(8, 5))
    print(myfun(8, 5))

There are various options, but no documentation yet.

Usage & contributions
---------------------------------------

Revised BSD License; at your own risk, you can mostly do whatever you want with this code, just don't use my name for promotion and do keep the license file.


