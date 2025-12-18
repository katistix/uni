import unittest
import tempfile
import shutil
import os
from datetime import date
from services.persistence_service import PersistenceService
from services.student import StudentService
from services.problem import ProblemService
from services.assignment import AssignmentService

class TestPersistenceService(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.persistence = PersistenceService(self.test_dir)
        
        self.student_service = StudentService()
        self.problem_service = ProblemService()
        self.assignment_service = AssignmentService()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_and_load_data(self):
        # Add test data
        self.student_service.add_student("John Doe", 917)
        self.student_service.add_student("Jane Smith", 918)
        
        problem_date = date(2024, 12, 15)
        self.problem_service.add_problem(7, 1, "Test problem", problem_date)
        
        # We need to manually link repos for assignment service to work correctly in this integration context
        self.assignment_service._student_repo.add_student("John Doe", 917)
        self.assignment_service._problem_repo.add_problem(7, 1, "Test problem", problem_date)
        
        self.assignment_service.create_assignment(1, "7_1")
        self.assignment_service.grade_assignment(1, 9.5)

        # Save data
        self.persistence.save_application_data(
            self.student_service, 
            self.problem_service, 
            self.assignment_service
        )
        
        # Verify files exist
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "students.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "problems.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "assignments.csv")))

        # Load data back
        students, problems, assignments = self.persistence.load_application_data()
        
        # Verify loaded data
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].get_name(), "John Doe")
        self.assertEqual(students[1].get_name(), "Jane Smith")
        
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].get_description(), "Test problem")
        self.assertEqual(problems[0].get_deadline(), problem_date)
        
        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0].get_student_id(), 1)
        self.assertEqual(assignments[0].get_problem_id(), "7_1")
        self.assertEqual(assignments[0].get_grade(), 9.5)

    def test_ensure_files_exist(self):
        # Check if files were created on init
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "students.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "problems.csv")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "assignments.csv")))

    def test_backup_creation(self):
        # Create a dummy file
        student_file = os.path.join(self.test_dir, "students.csv")
        with open(student_file, 'w') as f:
            f.write("test")
            
        self.persistence.save_application_data(
            self.student_service, 
            self.problem_service, 
            self.assignment_service
        )
        
        self.assertTrue(os.path.exists(f"{student_file}.backup"))

    def test_export_data(self):
        export_dir = os.path.join(self.test_dir, "export")
        self.persistence.export_data(export_dir)
        
        self.assertTrue(os.path.exists(os.path.join(export_dir, "students.csv")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "problems.csv")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "assignments.csv")))
