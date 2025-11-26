import os
import sys
from typing import Optional

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from persistence.data_manager import DataManager
from services.student import StudentService
from services.problem import ProblemService  
from services.assignment import AssignmentService


class PersistenceService:
    """Service to handle data persistence for the application"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_manager = DataManager(data_dir)
        
    def save_application_data(self, student_service: StudentService, 
                            problem_service: ProblemService,
                            assignment_service: AssignmentService) -> None:
        """Save all application data to CSV files"""
        try:
            students = student_service.list_students()
            problems = problem_service.list_problems()
            assignments = assignment_service.list_assignments()
            
            self.data_manager.save_all_data(students, problems, assignments)
            print("Data saved successfully to CSV files.")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_application_data(self) -> tuple:
        """Load all application data from CSV files"""
        try:
            return self.data_manager.load_all_data()
        except Exception as e:
            print(f"Error loading data: {e}")
            return [], [], []
    
    def export_data(self, export_dir: str) -> None:
        """Export data to a different directory"""
        try:
            self.data_manager.export_to_directory(export_dir)
            print(f"Data exported successfully to {export_dir}")
        except Exception as e:
            print(f"Error exporting data: {e}")


def test_module():
    """Test the persistence service"""
    from domain.student import Student
    from domain.problem import Problem
    from domain.assignment import Assignment
    from datetime import date
    
    # Create test services
    student_service = StudentService()
    problem_service = ProblemService()
    assignment_service = AssignmentService()
    
    # Add some test data
    student_service.add_student("John Doe", 917)
    student_service.add_student("Jane Smith", 918)
    
    problem_service.add_problem(7, 1, "Test problem", date(2024, 12, 15))
    
    # Create persistence service and save data
    persistence = PersistenceService("test_data")
    persistence.save_application_data(student_service, problem_service, assignment_service)
    
    # Load data back
    students, problems, assignments = persistence.load_application_data()
    print(f"Loaded {len(students)} students, {len(problems)} problems, {len(assignments)} assignments")


if __name__ == "__main__":
    test_module()