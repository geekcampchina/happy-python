import traceback

from happy_python import HappyLog


class HappyPyException(Exception):
    hlog = HappyLog.get_instance()

    @staticmethod
    def get_stack(e: Exception):
        return '\n'.join(traceback.format_exception(e))

    def __init__(self, err='Happy Python Error', e: Exception = None):
        if e:
            self.hlog.error(HappyPyException.get_stack(e))
        else:
            self.hlog.error(err)

        Exception.__init__(self, err)
