import os
import csv
import shutil
from typing import List, Dict, Any, Optional
from datetime import date

from domain.student import Student
from domain.problem import Problem
from domain.assignment import Assignment
from services.student import StudentService
from services.problem import ProblemService  
from services.assignment import AssignmentService


class PersistenceService:
    """Service to handle data persistence for the application"""
    
    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.students_file = os.path.join(data_dir, "students.csv")
        self.problems_file = os.path.join(data_dir, "problems.csv")
        self.assignments_file = os.path.join(data_dir, "assignments.csv")
        
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create CSV files with headers if they don't exist"""
        files_and_headers = [
            (self.students_file, ['id', 'name', 'group']),
            (self.problems_file, ['lab_number', 'problem_number', 'description', 'deadline']),
            (self.assignments_file, ['assignment_id', 'student_id', 'problem_id', 'grade'])
        ]
        
        for filepath, fieldnames in files_and_headers:
            if not os.path.exists(filepath):
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
    
    def _backup_file(self, filepath: str) -> str:
        """Create a backup of a file"""
        if os.path.exists(filepath):
            backup_path = f"{filepath}.backup"
            try:
                shutil.copy2(filepath, backup_path)
                return backup_path
            except Exception as e:
                raise ValueError(f"Failed to create backup: {e}")
        return ""
    
    def save_application_data(self, student_service: StudentService, 
                            problem_service: ProblemService,
                            assignment_service: AssignmentService) -> None:
        """Save all application data to CSV files"""
        try:
            # Create backups first
            self._backup_file(self.students_file)
            self._backup_file(self.problems_file)
            self._backup_file(self.assignments_file)
            
            # Get data from services
            students = student_service.list_students()
            problems = problem_service.list_problems()
            assignments = assignment_service.list_assignments()
            
            # Save students
            with open(self.students_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'name', 'group'])
                writer.writeheader()
                for student in students:
                    writer.writerow({
                        'id': student.get_id(),
                        'name': student.get_name(),
                        'group': student.get_group()
                    })
            
            # Save problems
            with open(self.problems_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['lab_number', 'problem_number', 'description', 'deadline'])
                writer.writeheader()
                for problem in problems:
                    writer.writerow({
                        'lab_number': problem.get_lab_number(),
                        'problem_number': problem.get_problem_number(),
                        'description': problem.get_description(),
                        'deadline': problem.get_deadline().isoformat()
                    })
            
            # Save assignments
            with open(self.assignments_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['assignment_id', 'student_id', 'problem_id', 'grade'])
                writer.writeheader()
                for assignment in assignments:
                    writer.writerow({
                        'assignment_id': assignment.get_assignment_id(),
                        'student_id': assignment.get_student_id(),
                        'problem_id': assignment.get_problem_id(),
                        'grade': assignment.get_grade() if assignment.get_grade() is not None else ''
                    })
            
            print("Data saved successfully to CSV files.")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_application_data(self) -> tuple[List[Student], List[Problem], List[Assignment]]:
        """Load all application data from CSV files"""
        try:
            students = []
            problems = []
            assignments = []
            
            # Load students
            if os.path.exists(self.students_file):
                with open(self.students_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        students.append(Student(
                            int(row['id']),
                            row['name'],
                            int(row['group'])
                        ))
            
            # Load problems
            if os.path.exists(self.problems_file):
                with open(self.problems_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        problems.append(Problem(
                            int(row['lab_number']),
                            int(row['problem_number']),
                            row['description'],
                            date.fromisoformat(row['deadline'])
                        ))
            
            # Load assignments
            if os.path.exists(self.assignments_file):
                with open(self.assignments_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        grade_str = row.get('grade', '')
                        grade = float(grade_str) if grade_str and grade_str.lower() != 'none' else None
                        assignments.append(Assignment(
                            int(row['assignment_id']),
                            int(row['student_id']),
                            row['problem_id'],
                            grade
                        ))
            
            return students, problems, assignments
        except Exception as e:
            print(f"Error loading data: {e}")
            return [], [], []
    
    def export_data(self, export_dir: str) -> None:
        """Export data to a different directory"""
        try:
            os.makedirs(export_dir, exist_ok=True)
            
            files_to_copy = [
                ("students.csv", self.students_file),
                ("problems.csv", self.problems_file),
                ("assignments.csv", self.assignments_file)
            ]
            
            for filename, source_path in files_to_copy:
                if os.path.exists(source_path):
                    dest_path = os.path.join(export_dir, filename)
                    shutil.copy2(source_path, dest_path)
            
            print(f"Data exported successfully to {export_dir}")
        except Exception as e:
            print(f"Error exporting data: {e}")

