import unittest
from domain.assignment import Assignment

class TestAssignment(unittest.TestCase):
    def test_assignment_creation(self):
        assignment = Assignment(1, 10, "7_1")
        self.assertEqual(assignment.get_assignment_id(), 1)
        self.assertEqual(assignment.assignment_id, 1)
        self.assertEqual(assignment.get_student_id(), 10)
        self.assertEqual(assignment.get_problem_id(), "7_1")
        self.assertIsNone(assignment.get_grade())
        self.assertFalse(assignment.has_grade())
        
        assignment2 = Assignment(2, 30, "9_1", 8.0)
        self.assertEqual(assignment2.get_grade(), 8.0)
        self.assertTrue(assignment2.has_grade())

    def test_assignment_modification(self):
        assignment = Assignment(1, 10, "7_1")
        
        assignment.set_student_id(20)
        self.assertEqual(assignment.get_student_id(), 20)
        
        assignment.set_problem_id("8_2")
        self.assertEqual(assignment.get_problem_id(), "8_2")
        
        assignment.set_grade(9.5)
        self.assertEqual(assignment.get_grade(), 9.5)
        self.assertTrue(assignment.has_grade())
        
        assignment.set_grade(None)
        self.assertIsNone(assignment.get_grade())
        self.assertFalse(assignment.has_grade())

    def test_invalid_grade(self):
        assignment = Assignment(1, 10, "7_1")
        
        with self.assertRaises(ValueError):
            assignment.set_grade(15)
            
        with self.assertRaises(ValueError):
            assignment.set_grade(-1)
