class NamedItem:

    NAME = 'name'
    ID = 'id'

    def __init__(self, name='', eddbId=0):
        self._name = name
        self._id = eddbId

    @property
    def get_id(self):
        return self._id

    def set_id(self, x):
        self._id = x

    def get_name(self):
        return self._name

    def set_name(self, x):
        self._name = x
