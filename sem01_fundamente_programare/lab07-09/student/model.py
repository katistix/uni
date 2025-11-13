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


def test_module():
    student = Student(1, "John Doe", 917)
    assert student.get_id() == 1
    assert student.id == 1
    assert student.get_name() == "John Doe"
    assert student.get_group() == 917
    
    student.set_name("Jane Smith")
    assert student.get_name() == "Jane Smith"
    
    student.set_group(918)
    assert student.get_group() == 918
    
    student2 = Student(0, "", 0)
    assert student2.get_id() == 0
    assert student2.get_name() == ""
    assert student2.get_group() == 0

