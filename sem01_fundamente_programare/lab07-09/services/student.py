from repos.student import StudentRepository
from domain.student import Student


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
        """Remove a student by ID. Raises ValueError if not found."""
        try:
            self._student_repo.remove_student(student_id)
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def modify_student(self, student_id: int, new_name: str, new_group: int) -> None:
        """Modify an existing student's name and group. Raises ValueError if not found."""
        try:
            self._student_repo.modify_student(student_id, new_name, new_group)
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def search_students(self, search_term: str, search_type: str) -> list[Student]:
        """Search for students by name, id, or group"""
        results = self._student_repo.search_students(search_term, search_type)
        return results


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
    
    service.modify_student(1, "Johnny Doe", 919)
    modified_students = service.list_students()
    modified_student = next(s for s in modified_students if s.get_id() == 1)
    assert modified_student.get_name() == "Johnny Doe"
    assert modified_student.get_group() == 919
    
    results = service.search_students("johnny", "name")
    assert len(results) == 1
    assert results[0].get_name() == "Johnny Doe"
    
    results = service.search_students("1", "id")
    assert len(results) == 1
    assert results[0].get_id() == 1
    
    results = service.search_students("918", "group")
    assert len(results) == 1
    assert results[0].get_group() == 918
    
    service.remove_student(1)
    assert len(service.list_students()) == 1
    
    try:
        service.remove_student(999)
        assert False
    except ValueError as e:
        assert "not found" in str(e)
    
    try:
        service.modify_student(999, "Test", 123)
        assert False
    except ValueError as e:
        assert "not found" in str(e)