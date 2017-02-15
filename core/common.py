import logging

STDOUT = 'stdout'

STDERR = 'stderr'

RETCODE = 'retcode'

logger = logging.getLogger('control')


def format_result(retcode, result):
    if retcode == 0:
        return {RETCODE: retcode, STDERR: '', STDOUT: result}
    else:
        return {RETCODE: retcode, STDERR: result, STDOUT: ''}


def try_except(func):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception, e:
            result = format_result(1, str(e))
        finally:
            return result

    return wrapped
