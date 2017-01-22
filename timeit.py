from functools import wraps
from time import time
import logging


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        logger = logging.getLogger('herobot')
        result = f(*args, **kw)
        te = time()
        # print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        logger.debug('func:%r took: %2.4f sec' % (f.__name__, te - ts))
        return result
    return wrap
