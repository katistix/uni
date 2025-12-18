from repos.assignment import AssignmentRepository
from repos.student import StudentRepository
from repos.problem import ProblemRepository
from domain.assignment import Assignment
from domain.student import Student
from domain.problem import Problem
from typing import List, Optional


class AssignmentService:
    def __init__(self):
        self._assignment_repo = AssignmentRepository([])
        self._student_repo = StudentRepository([])
        self._problem_repo = ProblemRepository([])

    def create_assignment(self, student_id: int, problem_id: str) -> Assignment:
        """Create a new assignment for a student and problem.
        
        Validates that:
        - Student exists
        - Problem exists
        - Assignment doesn't already exist for this student-problem pair
        """
        # Validate student exists
        students = self._student_repo.get_all_students()
        student_exists = any(s.get_id() == student_id for s in students)
        if not student_exists:
            raise ValueError(f"Student with ID {student_id} not found")
        
        # Validate problem exists
        problems = self._problem_repo.list_problems()
        problem_exists = any(f"{p.get_lab_number()}_{p.get_problem_number()}" == problem_id for p in problems)
        if not problem_exists:
            raise ValueError(f"Problem with ID {problem_id} not found")
        
        # Check if assignment already exists
        if self._assignment_repo.assignment_exists(student_id, problem_id):
            raise ValueError(f"Assignment already exists for student {student_id} and problem {problem_id}")
        
        return self._assignment_repo.create_assignment(student_id, problem_id)

    def grade_assignment(self, assignment_id: int, grade: float) -> None:
        """Grade an assignment. Validates grade is between 0 and 10."""
        if grade < 0 or grade > 10:
            raise ValueError("Grade must be between 0 and 10")
        
        try:
            self._assignment_repo.grade_assignment(assignment_id, grade)
        except ValueError as e:
            raise ValueError(f"Error: {e}")

    def list_assignments(self) -> List[Assignment]:
        """Get all assignments."""
        return self._assignment_repo.get_all_assignments()

    def get_assignment_by_id(self, assignment_id: int) -> Optional[Assignment]:
        """Get assignment by ID."""
        return self._assignment_repo.get_assignment_by_id(assignment_id)

    def get_assignments_by_student(self, student_id: int) -> List[Assignment]:
        """Get all assignments for a student."""
        return self._assignment_repo.get_assignments_by_student(student_id)

    def get_assignments_by_problem(self, problem_id: str) -> List[Assignment]:
        """Get all assignments for a problem."""
        return self._assignment_repo.get_assignments_by_problem(problem_id)

    def get_student_name(self, student_id: int) -> str:
        """Get student name for display purposes."""
        students = self._student_repo.get_all_students()
        for student in students:
            if student.get_id() == student_id:
                return student.get_name()
        return f"Unknown (ID: {student_id})"

    def get_problem_description(self, problem_id: str) -> str:
        """Get problem description for display purposes."""
        problems = self._problem_repo.list_problems()
        for problem in problems:
            if f"{problem.get_lab_number()}_{problem.get_problem_number()}" == problem_id:
                return problem.get_description()
        return f"Unknown (ID: {problem_id})"

    # Methods to access underlying repositories (needed for CLI integration)
    def get_student_service_data(self):
        """Get student repository for integration."""
        return self._student_repo

    def get_problem_service_data(self):
        """Get problem repository for integration."""
        return self._problem_repo

    def set_student_repo(self, student_repo: StudentRepository):
        """Set student repository (for integration with existing services)."""
        self._student_repo = student_repo

    def set_problem_repo(self, problem_repo: ProblemRepository):
        """Set problem repository (for integration with existing services)."""
        self._problem_repo = problem_repo

