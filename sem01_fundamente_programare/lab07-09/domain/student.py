class Student:
    def __init__(self, id: int, name: str, group: int):
        self._id = id
        self._name = name
        self._group = group

    @property
    def id(self) -> int:
        return self._id

    def get_id(self) -> int:
        return self._id
    

    def get_name(self)->str:
        return self._name
    
    def set_name(self, new_name: str):
        self._name = new_name


    def get_group(self)->int:
        return self._group
    
    def set_group(self, new_group: int):
        self._group = new_group



