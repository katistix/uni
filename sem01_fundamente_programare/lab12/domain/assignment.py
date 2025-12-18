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

