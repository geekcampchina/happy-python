class HappyPyException(Exception):
    def __init__(self, err='Happy Python Error'):
        Exception.__init__(self, err)
