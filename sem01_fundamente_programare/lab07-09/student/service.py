from student.repository import StudentRepository
from student.model import Student


class StudentService:
    def __init__(self):
        self._student_repo = StudentRepository([])

    def add_student(self,name:str,group:int):
        student = self._student_repo.add_student(name, group)
        return student

    def list_students(self) -> list[Student]:
        students = self._student_repo.get_all_students()
        return students
    
    def remove_student(self, student_id: int):
        try:
            self._student_repo.remove_student(student_id)
            raise ValueError(f"Student with ID {student_id} removed successfully")
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")


def test_module():
    service = StudentService()
    
    student1 = service.add_student("John Doe", 917)
    assert student1.get_name() == "John Doe"
    assert student1.get_group() == 917
    
    students = service.list_students()
    assert len(students) == 1
    assert students[0].get_name() == "John Doe"
    
    student2 = service.add_student("Jane Smith", 918)
    assert len(service.list_students()) == 2
    
    try:
        service.remove_student(1)
        assert False
    except ValueError as e:
        assert "removed successfully" in str(e)
    
    try:
        service.remove_student(999)
        assert False
    except ValueError as e:
        assert "not found" in str(e)