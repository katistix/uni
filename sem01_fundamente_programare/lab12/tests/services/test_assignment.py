import unittest
from datetime import date
from services.assignment import AssignmentService

class TestAssignmentService(unittest.TestCase):
    def setUp(self):
        self.service = AssignmentService()
        # Setup test data
        self.service._student_repo.add_student("John Doe", 917)
        self.service._student_repo.add_student("Jane Smith", 918)
        
        self.service._problem_repo.add_problem(7, 1, "Sort array", date(2024, 12, 15))
        self.service._problem_repo.add_problem(7, 2, "Search algorithm", date(2024, 12, 20))

    def test_create_assignment(self):
        assignment1 = self.service.create_assignment(1, "7_1")
        self.assertEqual(assignment1.get_student_id(), 1)
        self.assertEqual(assignment1.get_problem_id(), "7_1")
        self.assertIsNone(assignment1.get_grade())
        
        # Test assignment already exists
        with self.assertRaises(ValueError) as cm:
            self.service.create_assignment(1, "7_1")
        self.assertIn("already exists", str(cm.exception))
        
        # Test invalid student
        with self.assertRaises(ValueError) as cm:
            self.service.create_assignment(999, "7_1")
        self.assertIn("not found", str(cm.exception))
        
        # Test invalid problem
        with self.assertRaises(ValueError) as cm:
            self.service.create_assignment(1, "8_1")
        self.assertIn("not found", str(cm.exception))

    def test_grade_assignment(self):
        self.service.create_assignment(1, "7_1")
        self.service.grade_assignment(1, 9.5)
        graded = self.service.get_assignment_by_id(1)
        self.assertIsNotNone(graded)
        self.assertEqual(graded.get_grade(), 9.5)
        
        # Test invalid grade
        with self.assertRaises(ValueError) as cm:
            self.service.grade_assignment(1, 11)
        self.assertIn("between 0 and 10", str(cm.exception))
        
        with self.assertRaises(ValueError) as cm:
            self.service.grade_assignment(1, -1)
        self.assertIn("between 0 and 10", str(cm.exception))

    def test_list_assignments(self):
        self.service.create_assignment(1, "7_1")
        assignments = self.service.list_assignments()
        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0].get_assignment_id(), 1)

    def test_helper_methods(self):
        student_name = self.service.get_student_name(1)
        self.assertEqual(student_name, "John Doe")
        
        problem_desc = self.service.get_problem_description("7_1")
        self.assertEqual(problem_desc, "Sort array")
        
        unknown_student = self.service.get_student_name(999)
        self.assertIn("Unknown", unknown_student)
        
        unknown_problem = self.service.get_problem_description("9_1")
        self.assertIn("Unknown", unknown_problem)
