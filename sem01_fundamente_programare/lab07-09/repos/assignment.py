from domain.assignment import Assignment
from typing import List, Optional

class AssignmentRepository:
    def __init__(self, assignment_list: List[Assignment]):
        self._assignment_list = assignment_list
        self._next_id = max((a.assignment_id for a in assignment_list), default=0) + 1

    def create_assignment(self, student_id: int, problem_id: str) -> Assignment:
        """Create a new assignment for a student and problem."""
        new_assignment = Assignment(self._next_id, student_id, problem_id)
        self._assignment_list.append(new_assignment)
        self._next_id += 1
        return new_assignment

    def grade_assignment(self, assignment_id: int, grade: float) -> None:
        """Grade an existing assignment. Raises ValueError if not found."""
        for assignment in self._assignment_list:
            if assignment.assignment_id == assignment_id:
                assignment.set_grade(grade)
                return
        raise ValueError(f"Assignment with id {assignment_id} not found")

    def get_assignment_by_id(self, assignment_id: int) -> Optional[Assignment]:
        """Get assignment by ID. Returns None if not found."""
        for assignment in self._assignment_list:
            if assignment.assignment_id == assignment_id:
                return assignment
        return None

    def get_all_assignments(self) -> List[Assignment]:
        """Return a copy of all assignments in the repository."""
        return self._assignment_list.copy()

    def get_assignments_by_student(self, student_id: int) -> List[Assignment]:
        """Get all assignments for a specific student."""
        return [a for a in self._assignment_list if a.get_student_id() == student_id]

    def get_assignments_by_problem(self, problem_id: str) -> List[Assignment]:
        """Get all assignments for a specific problem."""
        return [a for a in self._assignment_list if a.get_problem_id() == problem_id]

    def assignment_exists(self, student_id: int, problem_id: str) -> bool:
        """Check if an assignment already exists for this student and problem."""
        for assignment in self._assignment_list:
            if assignment.get_student_id() == student_id and assignment.get_problem_id() == problem_id:
                return True
        return False

    def remove_assignment(self, assignment_id: int) -> None:
        """Remove an assignment by ID. Raises ValueError if not found."""
        for assignment in self._assignment_list:
            if assignment.assignment_id == assignment_id:
                self._assignment_list.remove(assignment)
                return
        raise ValueError(f"Assignment with id {assignment_id} not found")

