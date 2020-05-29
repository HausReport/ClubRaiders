class PassThroughDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __missing__(self, key):
        return '$' + key
