"""Click with python 3 struggles with unicode. This often comes from SSHing
between machines with different locaeles or when click is ran as an init script.
"""
import os
import locale
import codecs


def _ascii_fix():
    if codecs.lookup(locale.getpreferredencoding()).name == 'ascii':
        os.environ['LC_ALL'] = os.environ['LANG'] = 'en_US.utf-8'
