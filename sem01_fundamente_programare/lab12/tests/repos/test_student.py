import unittest
from repos.student import StudentRepository

class TestStudentRepository(unittest.TestCase):
    def setUp(self):
        self.repo = StudentRepository([])

    def test_add_student(self):
        self.assertEqual(self.repo.get_all_students(), [])
        # Accessing private member _next_id for testing purposes, usually discouraged but keeping fidelity to original test
        self.assertEqual(self.repo._next_id, 1)

        student1 = self.repo.add_student("John Doe", 917)
        self.assertEqual(student1.get_id(), 1)
        self.assertEqual(student1.get_name(), "John Doe")
        self.assertEqual(student1.get_group(), 917)
        self.assertEqual(len(self.repo.get_all_students()), 1)

        student2 = self.repo.add_student("Jane Smith", 918)
        self.assertEqual(student2.get_id(), 2)
        self.assertEqual(len(self.repo.get_all_students()), 2)

    def test_modify_student(self):
        self.repo.add_student("John Doe", 917)
        self.repo.modify_student(1, "Johnny Doe", 919)
        modified_student = self.repo.get_all_students()[0]
        self.assertEqual(modified_student.get_name(), "Johnny Doe")
        self.assertEqual(modified_student.get_group(), 919)

        with self.assertRaises(ValueError) as cm:
            self.repo.modify_student(999, "Test", 123)
        self.assertIn("not found", str(cm.exception))

    def test_search_students(self):
        self.repo.add_student("Johnny Doe", 919)
        self.repo.add_student("Jane Smith", 918)

        results = self.repo.search_students("john", "name")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_name(), "Johnny Doe")

        results = self.repo.search_students("1", "id")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_id(), 1)

        results = self.repo.search_students("918", "group")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_group(), 918)

    def test_remove_student(self):
        self.repo.add_student("John Doe", 917)
        self.repo.add_student("Jane Smith", 918)
        
        self.repo.remove_student(1)
        self.assertEqual(len(self.repo.get_all_students()), 1)
        self.assertEqual(self.repo.get_all_students()[0].get_id(), 2)

        with self.assertRaises(ValueError) as cm:
            self.repo.remove_student(999)
        self.assertIn("not found", str(cm.exception))
