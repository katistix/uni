import unittest
from datetime import date
from repos.problem import ProblemRepository

class TestProblemRepository(unittest.TestCase):
    def setUp(self):
        self.repo = ProblemRepository([])

    def test_add_problem(self):
        self.assertEqual(self.repo.list_problems(), [])
        
        problem_date = date(2024, 12, 15)
        problem1 = self.repo.add_problem(7, 1, "Sort array problem", problem_date)
        self.assertEqual(problem1.get_lab_number(), 7)
        self.assertEqual(problem1.get_problem_number(), 1)
        self.assertEqual(len(self.repo.list_problems()), 1)
        
        self.repo.add_problem(7, 2, "Search problem", problem_date)
        self.assertEqual(len(self.repo.list_problems()), 2)

    def test_modify_problem(self):
        problem_date = date(2024, 12, 15)
        self.repo.add_problem(7, 1, "Sort array problem", problem_date)
        
        new_date = date(2024, 12, 20)
        self.repo.modify_problem(7, 1, "Updated sort problem", new_date)
        modified_problem = self.repo.list_problems()[0]
        self.assertEqual(modified_problem.get_description(), "Updated sort problem")
        self.assertEqual(modified_problem.get_deadline(), new_date)
        
        with self.assertRaises(ValueError) as cm:
            self.repo.modify_problem(99, 99, "Test", new_date)
        self.assertIn("not found", str(cm.exception))

    def test_search_problems(self):
        problem_date = date(2024, 12, 15)
        self.repo.add_problem(7, 1, "Sort array problem", problem_date)
        
        results = self.repo.search_problems_by_id("7_1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_lab_number(), 7)
        self.assertEqual(results[0].get_problem_number(), 1)
        
        results = self.repo.search_problems_by_id("invalid")
        self.assertEqual(len(results), 0)
        
        results = self.repo.search_problems_by_id("99_99")
        self.assertEqual(len(results), 0)

    def test_remove_problem(self):
        problem_date = date(2024, 12, 15)
        self.repo.add_problem(7, 1, "Sort array problem", problem_date)
        self.repo.add_problem(7, 2, "Search problem", problem_date)
        
        self.repo.remove_problem(7, 1)
        self.assertEqual(len(self.repo.list_problems()), 1)
        
        with self.assertRaises(ValueError) as cm:
            self.repo.remove_problem(99, 99)
        self.assertIn("not found", str(cm.exception))
