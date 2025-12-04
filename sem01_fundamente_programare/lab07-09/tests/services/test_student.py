import unittest
import random
from services.student import StudentService

class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.service = StudentService()

    def test_random_functionality(self):
        random_seed = 123
        random.seed(random_seed)

        random_name = self.service.generate_random_name()
        self.assertEqual(random_name, "drfXArgc")
        random_name = self.service.generate_random_name()
        self.assertEqual(random_name, "yIJvvdki")
        random_name = self.service.generate_random_name()
        self.assertEqual(random_name, "vJvSpkaB")

        random_group = self.service.generate_random_group()
        self.assertEqual(random_group, 793)
        random_group = self.service.generate_random_group()
        self.assertEqual(random_group, 90)
        random_group = self.service.generate_random_group()
        self.assertEqual(random_group, 900)

    def test_add_and_list_students(self):
        student1 = self.service.add_student("John Doe", 917)
        self.assertEqual(student1.get_name(), "John Doe")
        self.assertEqual(student1.get_group(), 917)
        
        students = self.service.list_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].get_name(), "John Doe")
        
        self.service.add_student("Jane Smith", 918)
        self.assertEqual(len(self.service.list_students()), 2)

    def test_modify_student(self):
        self.service.add_student("John Doe", 917)
        self.service.modify_student(1, "Johnny Doe", 919)
        
        modified_students = self.service.list_students()
        modified_student = next(s for s in modified_students if s.get_id() == 1)
        self.assertEqual(modified_student.get_name(), "Johnny Doe")
        self.assertEqual(modified_student.get_group(), 919)

        with self.assertRaises(ValueError) as cm:
            self.service.modify_student(999, "Test", 123)
        self.assertIn("not found", str(cm.exception))

    def test_search_students(self):
        self.service.add_student("Johnny Doe", 919)
        self.service.add_student("Jane Smith", 918)

        results = self.service.search_students("johnny", "name")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_name(), "Johnny Doe")
        
        results = self.service.search_students("1", "id")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_id(), 1)
        
        results = self.service.search_students("918", "group")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get_group(), 918)

    def test_remove_student(self):
        self.service.add_student("John Doe", 917)
        self.service.remove_student(1)
        self.assertEqual(len(self.service.list_students()), 0)
        
        with self.assertRaises(ValueError) as cm:
            self.service.remove_student(999)
        self.assertIn("not found", str(cm.exception))
