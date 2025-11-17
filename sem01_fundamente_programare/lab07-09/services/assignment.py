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


def test_module():
    service = AssignmentService()
    
    # Setup test data
    service._student_repo.add_student("John Doe", 917)
    service._student_repo.add_student("Jane Smith", 918)
    
    from datetime import date
    service._problem_repo.add_problem(7, 1, "Sort array", date(2024, 12, 15))
    service._problem_repo.add_problem(7, 2, "Search algorithm", date(2024, 12, 20))
    
    # Test creating assignment
    assignment1 = service.create_assignment(1, "7_1")
    assert assignment1.get_student_id() == 1
    assert assignment1.get_problem_id() == "7_1"
    assert assignment1.get_grade() is None
    
    # Test assignment already exists
    try:
        service.create_assignment(1, "7_1")
        assert False, "Should raise ValueError for duplicate assignment"
    except ValueError as e:
        assert "already exists" in str(e)
    
    # Test invalid student
    try:
        service.create_assignment(999, "7_1")
        assert False, "Should raise ValueError for invalid student"
    except ValueError as e:
        assert "not found" in str(e)
    
    # Test invalid problem
    try:
        service.create_assignment(1, "8_1")
        assert False, "Should raise ValueError for invalid problem"
    except ValueError as e:
        assert "not found" in str(e)
    
    # Test grading
    service.grade_assignment(1, 9.5)
    graded = service.get_assignment_by_id(1)
    assert graded is not None
    assert graded.get_grade() == 9.5
    
    # Test invalid grade
    try:
        service.grade_assignment(1, 11)
        assert False, "Should raise ValueError for grade > 10"
    except ValueError as e:
        assert "between 0 and 10" in str(e)
    
    try:
        service.grade_assignment(1, -1)
        assert False, "Should raise ValueError for grade < 0"
    except ValueError as e:
        assert "between 0 and 10" in str(e)
    
    # Test listing
    assignments = service.list_assignments()
    assert len(assignments) == 1
    assert assignments[0].get_assignment_id() == 1
    
    # Test helper methods
    student_name = service.get_student_name(1)
    assert student_name == "John Doe"
    
    problem_desc = service.get_problem_description("7_1")
    assert problem_desc == "Sort array"
    
    unknown_student = service.get_student_name(999)
    assert "Unknown" in unknown_student
    
    unknown_problem = service.get_problem_description("9_1")
    assert "Unknown" in unknown_problem