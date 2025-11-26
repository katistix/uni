from dataclasses import dataclass
from datetime import date
from domain.problem import Problem


@dataclass
class ProblemDTO:
    lab_number: int
    problem_number: int
    description: str
    deadline: str  # Store as string for CSV compatibility
    
    @classmethod
    def from_domain(cls, problem: Problem) -> 'ProblemDTO':
        """Create DTO from domain object"""
        return cls(
            lab_number=problem.get_lab_number(),
            problem_number=problem.get_problem_number(),
            description=problem.get_description(),
            deadline=problem.get_deadline().isoformat()  # Convert date to string
        )
    
    def to_domain(self) -> Problem:
        """Convert DTO to domain object"""
        return Problem(
            self.lab_number,
            self.problem_number,
            self.description,
            date.fromisoformat(self.deadline)  # Convert string back to date
        )
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'ProblemDTO':
        """Create DTO from CSV row dictionary"""
        return cls(
            lab_number=int(row['lab_number']),
            problem_number=int(row['problem_number']),
            description=row['description'],
            deadline=row['deadline']
        )
    
    def to_csv_row(self) -> dict:
        """Convert DTO to CSV row dictionary"""
        return {
            'lab_number': self.lab_number,
            'problem_number': self.problem_number,
            'description': self.description,
            'deadline': self.deadline
        }
    
    @property
    def problem_id(self) -> str:
        """Get problem ID in format lab_problem"""
        return f"{self.lab_number}_{self.problem_number}"


def test_module():
    # Test from domain
    problem_date = date(2024, 12, 15)
    problem = Problem(7, 1, "Sort array", problem_date)
    dto = ProblemDTO.from_domain(problem)
    assert dto.lab_number == 7
    assert dto.problem_number == 1
    assert dto.description == "Sort array"
    assert dto.deadline == "2024-12-15"
    assert dto.problem_id == "7_1"
    
    # Test to domain
    back_to_domain = dto.to_domain()
    assert back_to_domain.get_lab_number() == 7
    assert back_to_domain.get_problem_number() == 1
    assert back_to_domain.get_description() == "Sort array"
    assert back_to_domain.get_deadline() == problem_date
    
    # Test CSV conversion
    csv_row = {
        'lab_number': '8',
        'problem_number': '2',
        'description': 'Search algorithm',
        'deadline': '2024-12-20'
    }
    dto_from_csv = ProblemDTO.from_csv_row(csv_row)
    assert dto_from_csv.lab_number == 8
    assert dto_from_csv.problem_number == 2
    assert dto_from_csv.description == "Search algorithm"
    assert dto_from_csv.deadline == "2024-12-20"
    
    csv_back = dto_from_csv.to_csv_row()
    assert csv_back['lab_number'] == 8
    assert csv_back['problem_number'] == 2
    assert csv_back['description'] == "Search algorithm"
    assert csv_back['deadline'] == "2024-12-20"