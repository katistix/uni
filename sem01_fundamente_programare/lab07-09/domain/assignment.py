from typing import Optional

class Assignment:
    def __init__(self, assignment_id: int, student_id: int, problem_id: str, grade: Optional[float] = None):
        self._assignment_id = assignment_id
        self._student_id = student_id
        self._problem_id = problem_id
        self._grade = grade

    @property
    def assignment_id(self) -> int:
        return self._assignment_id

    def get_assignment_id(self) -> int:
        return self._assignment_id

    def get_student_id(self) -> int:
        return self._student_id

    def set_student_id(self, new_student_id: int):
        self._student_id = new_student_id

    def get_problem_id(self) -> str:
        return self._problem_id

    def set_problem_id(self, new_problem_id: str):
        self._problem_id = new_problem_id

    def get_grade(self) -> Optional[float]:
        return self._grade

    def set_grade(self, new_grade: Optional[float]):
        if new_grade is not None and (new_grade < 0 or new_grade > 10):
            raise ValueError("Grade must be between 0 and 10")
        self._grade = new_grade

    def has_grade(self) -> bool:
        return self._grade is not None


def test_module():
    assignment = Assignment(1, 10, "7_1")
    assert assignment.get_assignment_id() == 1
    assert assignment.assignment_id == 1
    assert assignment.get_student_id() == 10
    assert assignment.get_problem_id() == "7_1"
    assert assignment.get_grade() is None
    assert not assignment.has_grade()
    
    assignment.set_student_id(20)
    assert assignment.get_student_id() == 20
    
    assignment.set_problem_id("8_2")
    assert assignment.get_problem_id() == "8_2"
    
    assignment.set_grade(9.5)
    assert assignment.get_grade() == 9.5
    assert assignment.has_grade()
    
    assignment.set_grade(None)
    assert assignment.get_grade() is None
    assert not assignment.has_grade()
    
    try:
        assignment.set_grade(15)
        assert False, "Should raise ValueError for grade > 10"
    except ValueError:
        pass
        
    try:
        assignment.set_grade(-1)
        assert False, "Should raise ValueError for grade < 0"
    except ValueError:
        pass
        
    assignment2 = Assignment(2, 30, "9_1", 8.0)
    assert assignment2.get_grade() == 8.0
    assert assignment2.has_grade()