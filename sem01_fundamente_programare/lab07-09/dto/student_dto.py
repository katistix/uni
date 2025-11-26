from dataclasses import dataclass
from typing import Optional
from domain.student import Student


@dataclass
class StudentDTO:
    id: int
    name: str
    group: int
    
    @classmethod
    def from_domain(cls, student: Student) -> 'StudentDTO':
        """Create DTO from domain object"""
        return cls(
            id=student.get_id(),
            name=student.get_name(),
            group=student.get_group()
        )
    
    def to_domain(self) -> Student:
        """Convert DTO to domain object"""
        return Student(self.id, self.name, self.group)
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'StudentDTO':
        """Create DTO from CSV row dictionary"""
        return cls(
            id=int(row['id']),
            name=row['name'],
            group=int(row['group'])
        )
    
    def to_csv_row(self) -> dict:
        """Convert DTO to CSV row dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'group': self.group
        }


def test_module():
    # Test from domain
    student = Student(1, "John Doe", 917)
    dto = StudentDTO.from_domain(student)
    assert dto.id == 1
    assert dto.name == "John Doe"
    assert dto.group == 917
    
    # Test to domain
    back_to_domain = dto.to_domain()
    assert back_to_domain.get_id() == 1
    assert back_to_domain.get_name() == "John Doe"
    assert back_to_domain.get_group() == 917
    
    # Test CSV conversion
    csv_row = {'id': '2', 'name': 'Jane Smith', 'group': '918'}
    dto_from_csv = StudentDTO.from_csv_row(csv_row)
    assert dto_from_csv.id == 2
    assert dto_from_csv.name == "Jane Smith"
    assert dto_from_csv.group == 918
    
    csv_back = dto_from_csv.to_csv_row()
    assert csv_back['id'] == 2
    assert csv_back['name'] == "Jane Smith"
    assert csv_back['group'] == 918