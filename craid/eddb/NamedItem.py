class NamedItem:
    NAME = 'name'
    ID = 'id'

    def __init__(self, name='', eddbId=0):
        self._name: str = name
        self._id: int = eddbId

    def get_id(self) -> int:
        return self._id

    def set_id(self, x: int):
        self._id = x

    def get_name(self) -> str:
        return self._name

    def set_name(self, x: str):
        self._name = x
