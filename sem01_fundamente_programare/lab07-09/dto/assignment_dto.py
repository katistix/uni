from dataclasses import dataclass
from typing import Optional
from domain.assignment import Assignment


@dataclass
class AssignmentDTO:
    assignment_id: int
    student_id: int
    problem_id: str
    grade: Optional[float] = None
    
    @classmethod
    def from_domain(cls, assignment: Assignment) -> 'AssignmentDTO':
        """Create DTO from domain object"""
        return cls(
            assignment_id=assignment.get_assignment_id(),
            student_id=assignment.get_student_id(),
            problem_id=assignment.get_problem_id(),
            grade=assignment.get_grade()
        )
    
    def to_domain(self) -> Assignment:
        """Convert DTO to domain object"""
        return Assignment(
            self.assignment_id,
            self.student_id,
            self.problem_id,
            self.grade
        )
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'AssignmentDTO':
        """Create DTO from CSV row dictionary"""
        grade_str = row.get('grade', '')
        grade = float(grade_str) if grade_str and grade_str.lower() != 'none' else None
        
        return cls(
            assignment_id=int(row['assignment_id']),
            student_id=int(row['student_id']),
            problem_id=row['problem_id'],
            grade=grade
        )
    
    def to_csv_row(self) -> dict:
        """Convert DTO to CSV row dictionary"""
        return {
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'problem_id': self.problem_id,
            'grade': self.grade if self.grade is not None else ''
        }


@dataclass
class StudentStatisticsDTO:
    student_id: int
    student_name: str
    group: int
    total_assignments: int
    graded_assignments: int
    average_grade: Optional[float]
    
    def to_csv_row(self) -> dict:
        """Convert DTO to CSV row dictionary"""
        return {
            'student_id': self.student_id,
            'student_name': self.student_name,
            'group': self.group,
            'total_assignments': self.total_assignments,
            'graded_assignments': self.graded_assignments,
            'average_grade': self.average_grade if self.average_grade is not None else ''
        }


@dataclass
class ProblemStatisticsDTO:
    problem_id: str
    description: str
    total_assignments: int
    graded_assignments: int
    completion_rate: float  # percentage
    average_grade: Optional[float]
    
    def to_csv_row(self) -> dict:
        """Convert DTO to CSV row dictionary"""
        return {
            'problem_id': self.problem_id,
            'description': self.description,
            'total_assignments': self.total_assignments,
            'graded_assignments': self.graded_assignments,
            'completion_rate': self.completion_rate,
            'average_grade': self.average_grade if self.average_grade is not None else ''
        }


def test_module():
    # Test AssignmentDTO
    assignment = Assignment(1, 10, "7_1", 9.5)
    dto = AssignmentDTO.from_domain(assignment)
    assert dto.assignment_id == 1
    assert dto.student_id == 10
    assert dto.problem_id == "7_1"
    assert dto.grade == 9.5
    
    # Test to domain
    back_to_domain = dto.to_domain()
    assert back_to_domain.get_assignment_id() == 1
    assert back_to_domain.get_student_id() == 10
    assert back_to_domain.get_problem_id() == "7_1"
    assert back_to_domain.get_grade() == 9.5
    
    # Test CSV conversion
    csv_row = {
        'assignment_id': '2',
        'student_id': '20',
        'problem_id': '8_1',
        'grade': '8.0'
    }
    dto_from_csv = AssignmentDTO.from_csv_row(csv_row)
    assert dto_from_csv.assignment_id == 2
    assert dto_from_csv.student_id == 20
    assert dto_from_csv.problem_id == "8_1"
    assert dto_from_csv.grade == 8.0
    
    # Test with no grade
    csv_row_no_grade = {
        'assignment_id': '3',
        'student_id': '30',
        'problem_id': '9_1',
        'grade': ''
    }
    dto_no_grade = AssignmentDTO.from_csv_row(csv_row_no_grade)
    assert dto_no_grade.grade is None
    
    # Test statistics DTOs
    student_stats = StudentStatisticsDTO(
        student_id=1,
        student_name="John Doe",
        group=917,
        total_assignments=3,
        graded_assignments=2,
        average_grade=8.5
    )
    
    stats_csv = student_stats.to_csv_row()
    assert stats_csv['student_id'] == 1
    assert stats_csv['average_grade'] == 8.5
    
    problem_stats = ProblemStatisticsDTO(
        problem_id="7_1",
        description="Sort array",
        total_assignments=5,
        graded_assignments=4,
        completion_rate=80.0,
        average_grade=8.2
    )
    
    problem_csv = problem_stats.to_csv_row()
    assert problem_csv['completion_rate'] == 80.0