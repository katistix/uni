import unittest
from datetime import date
from services.problem import ProblemService

class TestProblemService(unittest.TestCase):
    def setUp(self):
        self.service = ProblemService()

    def test_add_and_list_problems(self):
        problem_date = date(2024, 12, 15)
        problem1 = self.service.add_problem(7, 1, "Sort array problem", problem_date)
        self.assertEqual(problem1.get_lab_number(), 7)
        self.assertEqual(problem1.get_problem_number(), 1)
        self.assertEqual(problem1.get_description(), "Sort array problem")
        
        problems = self.service.list_problems()
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0].get_description(), "Sort array problem")
        
        self.service.add_problem(7, 2, "Search problem", problem_date)
        self.assertEqual(len(self.service.list_problems()), 2)

    def test_modify_problem(self):
        problem_date = date(2024, 12, 15)
        self.service.add_problem(7, 1, "Sort array problem", problem_date)
        
        new_date = date(2024, 12, 20)
        self.service.modify_problem(7, 1, "Updated sort problem", new_date)
        
        updated_problems = self.service.list_problems()
        updated_problem = next(p for p in updated_problems if p.get_problem_number() == 1)
        self.assertEqual(updated_problem.get_description(), "Updated sort problem")
        self.assertEqual(updated_problem.get_deadline(), new_date)

        with self.assertRaises(ValueError) as cm:
            self.service.modify_problem(99, 99, "Test", new_date)
        self.assertIn("not found", str(cm.exception))

    def test_search_problems(self):
        problem_date = date(2024, 12, 15)
        self.service.add_problem(7, 1, "Sort array problem", problem_date)
        
        results = self.service.search_problems_by_id("7_1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_lab_number(), 7)
        self.assertEqual(results[0].get_problem_number(), 1)
        
        results = self.service.search_problems_by_id("invalid")
        self.assertEqual(len(results), 0)

    def test_remove_problem(self):
        problem_date = date(2024, 12, 15)
        self.service.add_problem(7, 1, "Sort array problem", problem_date)
        self.service.add_problem(7, 2, "Search problem", problem_date)
        
        self.service.remove_problem(7, 1)
        self.assertEqual(len(self.service.list_problems()), 1)
        
        with self.assertRaises(ValueError) as cm:
            self.service.remove_problem(99, 99)
        self.assertIn("not found", str(cm.exception))
