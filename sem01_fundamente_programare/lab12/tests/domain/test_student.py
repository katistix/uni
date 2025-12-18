import unittest
from domain.student import Student

class TestStudent(unittest.TestCase):
    def test_student_creation(self):
        student = Student(1, "John Doe", 917)
        self.assertEqual(student.get_id(), 1)
        self.assertEqual(student.id, 1)
        self.assertEqual(student.get_name(), "John Doe")
        self.assertEqual(student.get_group(), 917)
    
    def test_student_modification(self):
        student = Student(1, "John Doe", 917)
        student.set_name("Jane Smith")
        self.assertEqual(student.get_name(), "Jane Smith")
        
        student.set_group(918)
        self.assertEqual(student.get_group(), 918)
        
    def test_empty_student(self):
        student2 = Student(0, "", 0)
        self.assertEqual(student2.get_id(), 0)
        self.assertEqual(student2.get_name(), "")
        self.assertEqual(student2.get_group(), 0)
