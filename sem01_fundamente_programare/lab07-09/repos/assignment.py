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


def test_module():
    repo = AssignmentRepository([])
    assert repo.get_all_assignments() == []
    assert repo._next_id == 1

    assignment1 = repo.create_assignment(1, "7_1")
    assert assignment1.get_assignment_id() == 1
    assert assignment1.get_student_id() == 1
    assert assignment1.get_problem_id() == "7_1"
    assert assignment1.get_grade() is None
    assert len(repo.get_all_assignments()) == 1

    assignment2 = repo.create_assignment(2, "7_2")
    assert assignment2.get_assignment_id() == 2
    assert len(repo.get_all_assignments()) == 2

    repo.grade_assignment(1, 9.5)
    graded = repo.get_assignment_by_id(1)
    assert graded is not None
    assert graded.get_grade() == 9.5

    try:
        repo.grade_assignment(999, 8.0)
        assert False
    except ValueError as e:
        assert "not found" in str(e)

    assert repo.assignment_exists(1, "7_1") == True
    assert repo.assignment_exists(1, "7_2") == False
    assert repo.assignment_exists(999, "7_1") == False

    student_assignments = repo.get_assignments_by_student(1)
    assert len(student_assignments) == 1
    assert student_assignments[0].get_assignment_id() == 1

    problem_assignments = repo.get_assignments_by_problem("7_1")
    assert len(problem_assignments) == 1
    assert problem_assignments[0].get_assignment_id() == 1

    assignment3 = repo.create_assignment(1, "7_2")
    assert assignment3.get_assignment_id() == 3

    repo.remove_assignment(1)
    assert len(repo.get_all_assignments()) == 2
    assert repo.get_assignment_by_id(1) is None

    try:
        repo.remove_assignment(999)
        assert False
    except ValueError as e:
        assert "not found" in str(e)