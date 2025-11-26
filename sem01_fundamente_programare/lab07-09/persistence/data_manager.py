import os
import csv
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from datetime import date
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from domain.student import Student
from domain.problem import Problem
from domain.assignment import Assignment


class CSVPersistence(ABC):
    """Base class for CSV persistence operations"""
    
    def __init__(self, filepath: str, fieldnames: List[str]):
        self.filepath = filepath
        self.fieldnames = fieldnames
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create file with headers if it doesn't exist"""
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
    
    def save_all(self, data: List[Dict[str, Any]]) -> None:
        """Save all data to CSV file (overwrite)"""
        try:
            with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise ValueError(f"Failed to save data to {self.filepath}: {e}")
    
    def load_all(self) -> List[Dict[str, Any]]:
        """Load all data from CSV file"""
        try:
            data = []
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = [row for row in reader]
            return data
        except Exception as e:
            raise ValueError(f"Failed to load data from {self.filepath}: {e}")
    
    def append_row(self, row: Dict[str, Any]) -> None:
        """Append a single row to CSV file"""
        try:
            with open(self.filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(row)
        except Exception as e:
            raise ValueError(f"Failed to append data to {self.filepath}: {e}")
    
    def backup_file(self) -> str:
        """Create a backup of the current file"""
        if os.path.exists(self.filepath):
            backup_path = f"{self.filepath}.backup"
            try:
                import shutil
                shutil.copy2(self.filepath, backup_path)
                return backup_path
            except Exception as e:
                raise ValueError(f"Failed to create backup: {e}")
        return ""


@dataclass
class StudentDTO:
    id: int
    name: str
    group: int
    
    @classmethod
    def from_domain(cls, student: Student) -> 'StudentDTO':
        return cls(student.get_id(), student.get_name(), student.get_group())
    
    def to_domain(self) -> Student:
        return Student(self.id, self.name, self.group)
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'StudentDTO':
        return cls(int(row['id']), row['name'], int(row['group']))
    
    def to_csv_row(self) -> dict:
        return {'id': self.id, 'name': self.name, 'group': self.group}


@dataclass
class ProblemDTO:
    lab_number: int
    problem_number: int
    description: str
    deadline: str
    
    @classmethod
    def from_domain(cls, problem: Problem) -> 'ProblemDTO':
        return cls(
            problem.get_lab_number(),
            problem.get_problem_number(),
            problem.get_description(),
            problem.get_deadline().isoformat()
        )
    
    def to_domain(self) -> Problem:
        return Problem(
            self.lab_number,
            self.problem_number,
            self.description,
            date.fromisoformat(self.deadline)
        )
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'ProblemDTO':
        return cls(
            int(row['lab_number']),
            int(row['problem_number']),
            row['description'],
            row['deadline']
        )
    
    def to_csv_row(self) -> dict:
        return {
            'lab_number': self.lab_number,
            'problem_number': self.problem_number,
            'description': self.description,
            'deadline': self.deadline
        }


@dataclass
class AssignmentDTO:
    assignment_id: int
    student_id: int
    problem_id: str
    grade: Optional[float] = None
    
    @classmethod
    def from_domain(cls, assignment: Assignment) -> 'AssignmentDTO':
        return cls(
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
    
    @classmethod
    def from_csv_row(cls, row: dict) -> 'AssignmentDTO':
        grade_str = row.get('grade', '')
        grade = float(grade_str) if grade_str and grade_str.lower() != 'none' else None
        return cls(
            int(row['assignment_id']),
            int(row['student_id']),
            row['problem_id'],
            grade
        )
    
    def to_csv_row(self) -> dict:
        return {
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'problem_id': self.problem_id,
            'grade': self.grade if self.grade is not None else ''
        }


class StudentPersistence(CSVPersistence):
    """CSV persistence for students"""
    
    def __init__(self, filepath: str = "data/students.csv"):
        super().__init__(filepath, ['id', 'name', 'group'])
    
    def save_students(self, students: List[Student]) -> None:
        """Save students to CSV"""
        dtos = [StudentDTO.from_domain(s) for s in students]
        rows = [dto.to_csv_row() for dto in dtos]
        self.save_all(rows)
    
    def load_students(self) -> List[Student]:
        """Load students from CSV"""
        rows = self.load_all()
        dtos = [StudentDTO.from_csv_row(row) for row in rows]
        return [dto.to_domain() for dto in dtos]


class ProblemPersistence(CSVPersistence):
    """CSV persistence for problems"""
    
    def __init__(self, filepath: str = "data/problems.csv"):
        super().__init__(filepath, ['lab_number', 'problem_number', 'description', 'deadline'])
    
    def save_problems(self, problems: List[Problem]) -> None:
        """Save problems to CSV"""
        dtos = [ProblemDTO.from_domain(p) for p in problems]
        rows = [dto.to_csv_row() for dto in dtos]
        self.save_all(rows)
    
    def load_problems(self) -> List[Problem]:
        """Load problems from CSV"""
        rows = self.load_all()
        dtos = [ProblemDTO.from_csv_row(row) for row in rows]
        return [dto.to_domain() for dto in dtos]


class AssignmentPersistence(CSVPersistence):
    """CSV persistence for assignments"""
    
    def __init__(self, filepath: str = "data/assignments.csv"):
        super().__init__(filepath, ['assignment_id', 'student_id', 'problem_id', 'grade'])
    
    def save_assignments(self, assignments: List[Assignment]) -> None:
        """Save assignments to CSV"""
        dtos = [AssignmentDTO.from_domain(a) for a in assignments]
        rows = [dto.to_csv_row() for dto in dtos]
        self.save_all(rows)
    
    def load_assignments(self) -> List[Assignment]:
        """Load assignments from CSV"""
        rows = self.load_all()
        dtos = [AssignmentDTO.from_csv_row(row) for row in rows]
        return [dto.to_domain() for dto in dtos]


class DataManager:
    """Central data persistence manager"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.student_persistence = StudentPersistence(os.path.join(data_dir, "students.csv"))
        self.problem_persistence = ProblemPersistence(os.path.join(data_dir, "problems.csv"))
        self.assignment_persistence = AssignmentPersistence(os.path.join(data_dir, "assignments.csv"))
    
    def save_all_data(self, students: List[Student], problems: List[Problem], assignments: List[Assignment]) -> None:
        """Save all application data"""
        try:
            # Create backups first
            self.student_persistence.backup_file()
            self.problem_persistence.backup_file()
            self.assignment_persistence.backup_file()
            
            # Save data
            self.student_persistence.save_students(students)
            self.problem_persistence.save_problems(problems)
            self.assignment_persistence.save_assignments(assignments)
        except Exception as e:
            raise ValueError(f"Failed to save data: {e}")
    
    def load_all_data(self) -> tuple[List[Student], List[Problem], List[Assignment]]:
        """Load all application data"""
        try:
            students = self.student_persistence.load_students()
            problems = self.problem_persistence.load_problems()
            assignments = self.assignment_persistence.load_assignments()
            return students, problems, assignments
        except Exception as e:
            raise ValueError(f"Failed to load data: {e}")
    
    def export_to_directory(self, export_dir: str) -> None:
        """Export all data to a different directory"""
        os.makedirs(export_dir, exist_ok=True)
        
        import shutil
        
        files_to_copy = [
            ("students.csv", self.student_persistence.filepath),
            ("problems.csv", self.problem_persistence.filepath),
            ("assignments.csv", self.assignment_persistence.filepath)
        ]
        
        for filename, source_path in files_to_copy:
            if os.path.exists(source_path):
                dest_path = os.path.join(export_dir, filename)
                shutil.copy2(source_path, dest_path)


def test_module():
    import tempfile
    import shutil
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        data_manager = DataManager(temp_dir)
        
        # Create test data
        students = [
            Student(1, "John Doe", 917),
            Student(2, "Jane Smith", 918)
        ]
        
        problems = [
            Problem(7, 1, "Sort array", date(2024, 12, 15)),
            Problem(8, 2, "Search algorithm", date(2024, 12, 20))
        ]
        
        assignments = [
            Assignment(1, 1, "7_1", 9.5),
            Assignment(2, 2, "8_2", None)
        ]
        
        # Test save and load
        data_manager.save_all_data(students, problems, assignments)
        
        loaded_students, loaded_problems, loaded_assignments = data_manager.load_all_data()
        
        # Verify students
        assert len(loaded_students) == 2
        assert loaded_students[0].get_name() == "John Doe"
        assert loaded_students[1].get_group() == 918
        
        # Verify problems
        assert len(loaded_problems) == 2
        assert loaded_problems[0].get_description() == "Sort array"
        assert loaded_problems[1].get_deadline() == date(2024, 12, 20)
        
        # Verify assignments
        assert len(loaded_assignments) == 2
        assert loaded_assignments[0].get_grade() == 9.5
        assert loaded_assignments[1].get_grade() is None
        
        # Test export
        export_dir = os.path.join(temp_dir, "export")
        data_manager.export_to_directory(export_dir)
        
        assert os.path.exists(os.path.join(export_dir, "students.csv"))
        assert os.path.exists(os.path.join(export_dir, "problems.csv"))
        assert os.path.exists(os.path.join(export_dir, "assignments.csv"))