from domain.assignment import Assignment
from typing import Optional

class AssignmentDTO:
    def __init__(self, assignment_id: int, student_id: int, problem_id: str, grade: Optional[float]):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.problem_id = problem_id
        self.grade = grade

    @staticmethod
    def from_domain(assignment: Assignment) -> 'AssignmentDTO':
        return AssignmentDTO(
            assignment.get_assignment_id(),
            assignment.get_student_id(),
            assignment.get_problem_id(),
            assignment.get_grade()
        )

    def to_domain(self) -> Assignment:
        return Assignment(
            self.assignment_id,
            self.student_id,
            self.problem_id,
            self.grade
        )

    def to_csv_row(self) -> str:
        grade_str = str(self.grade) if self.grade is not None else ""
        return f"{self.assignment_id},{self.student_id},{self.problem_id},{grade_str}"

    @staticmethod
    def from_csv_row(row: str) -> 'AssignmentDTO':
        parts = row.strip().split(',')
        assignment_id = int(parts[0])
        student_id = int(parts[1])
        problem_id = parts[2]
        grade_str = parts[3]
        grade = float(grade_str) if grade_str else None
        return AssignmentDTO(assignment_id, student_id, problem_id, grade)
