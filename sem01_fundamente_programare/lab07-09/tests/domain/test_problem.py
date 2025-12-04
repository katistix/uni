import unittest
from datetime import date
from domain.problem import Problem

class TestProblem(unittest.TestCase):
    def test_problem_creation(self):
        problem_date = date(2024, 12, 15)
        problem = Problem(7, 1, "Sort array problem", problem_date)
        
        self.assertEqual(problem.get_lab_number(), 7)
        self.assertEqual(problem.get_problem_number(), 1)
        self.assertEqual(problem.get_description(), "Sort array problem")
        self.assertEqual(problem.get_deadline(), problem_date)
        
    def test_problem_modification(self):
        problem_date = date(2024, 12, 15)
        problem = Problem(7, 1, "Sort array problem", problem_date)
        
        problem.set_lab_number(8)
        self.assertEqual(problem.get_lab_number(), 8)
        
        problem.set_problem_number(2)
        self.assertEqual(problem.get_problem_number(), 2)
        
        problem.set_description("Updated description")
        self.assertEqual(problem.get_description(), "Updated description")
        
        new_date = date(2024, 12, 20)
        problem.set_deadline(new_date)
        self.assertEqual(problem.get_deadline(), new_date)
