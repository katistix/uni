import unittest
from repos.assignment import AssignmentRepository

class TestAssignmentRepository(unittest.TestCase):
    def setUp(self):
        self.repo = AssignmentRepository([])

    def test_create_assignment(self):
        self.assertEqual(self.repo.get_all_assignments(), [])
        # Accessing private member _next_id for testing purposes
        self.assertEqual(self.repo._next_id, 1)

        assignment1 = self.repo.create_assignment(1, "7_1")
        self.assertEqual(assignment1.get_assignment_id(), 1)
        self.assertEqual(assignment1.get_student_id(), 1)
        self.assertEqual(assignment1.get_problem_id(), "7_1")
        self.assertIsNone(assignment1.get_grade())
        self.assertEqual(len(self.repo.get_all_assignments()), 1)

        assignment2 = self.repo.create_assignment(2, "7_2")
        self.assertEqual(assignment2.get_assignment_id(), 2)
        self.assertEqual(len(self.repo.get_all_assignments()), 2)

    def test_grade_assignment(self):
        self.repo.create_assignment(1, "7_1")
        self.repo.grade_assignment(1, 9.5)
        graded = self.repo.get_assignment_by_id(1)
        self.assertIsNotNone(graded)
        self.assertEqual(graded.get_grade(), 9.5)

        with self.assertRaises(ValueError) as cm:
            self.repo.grade_assignment(999, 8.0)
        self.assertIn("not found", str(cm.exception))

    def test_assignment_exists(self):
        self.repo.create_assignment(1, "7_1")
        self.assertTrue(self.repo.assignment_exists(1, "7_1"))
        self.assertFalse(self.repo.assignment_exists(1, "7_2"))
        self.assertFalse(self.repo.assignment_exists(999, "7_1"))

    def test_get_assignments_by_student_and_problem(self):
        self.repo.create_assignment(1, "7_1")
        
        student_assignments = self.repo.get_assignments_by_student(1)
        self.assertEqual(len(student_assignments), 1)
        self.assertEqual(student_assignments[0].get_assignment_id(), 1)

        problem_assignments = self.repo.get_assignments_by_problem("7_1")
        self.assertEqual(len(problem_assignments), 1)
        self.assertEqual(problem_assignments[0].get_assignment_id(), 1)

    def test_remove_assignment(self):
        self.repo.create_assignment(1, "7_1")
        self.repo.create_assignment(2, "7_2")
        self.repo.create_assignment(1, "7_2")
        
        self.repo.remove_assignment(1)
        self.assertEqual(len(self.repo.get_all_assignments()), 2)
        self.assertIsNone(self.repo.get_assignment_by_id(1))

        with self.assertRaises(ValueError) as cm:
            self.repo.remove_assignment(999)
        self.assertIn("not found", str(cm.exception))
