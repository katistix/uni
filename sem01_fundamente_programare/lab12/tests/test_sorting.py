import unittest
from services.sorting import insertion_sort, comb_sort
from domain.student import Student
from domain.problem import Problem


class TestSortingFunctions(unittest.TestCase):
    """Test cases for the sorting functions"""
    
    def test_insertion_sort_basic(self):
        """Test insertion sort with basic integer list"""
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        result = insertion_sort(data)
        self.assertEqual(result, expected)
    
    def test_insertion_sort_reverse(self):
        """Test insertion sort with reverse=True"""
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [90, 64, 34, 25, 22, 12, 11]
        result = insertion_sort(data, reverse=True)
        self.assertEqual(result, expected)
    
    def test_insertion_sort_with_key(self):
        """Test insertion sort with key function"""
        data = ["banana", "pie", "washington", "book"]
        expected = ["pie", "book", "banana", "washington"]
        result = insertion_sort(data, key=len)
        self.assertEqual(result, expected)
    
    def test_comb_sort_basic(self):
        """Test comb sort with basic integer list"""
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        result = comb_sort(data)
        self.assertEqual(result, expected)
    
    def test_comb_sort_reverse(self):
        """Test comb sort with reverse=True"""
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [90, 64, 34, 25, 22, 12, 11]
        result = comb_sort(data, reverse=True)
        self.assertEqual(result, expected)
    
    def test_comb_sort_with_key(self):
        """Test comb sort with key function"""
        data = ["banana", "pie", "washington", "book"]
        expected = ["pie", "book", "banana", "washington"]
        result = comb_sort(data, key=len)
        self.assertEqual(result, expected)
    
    def test_insertion_sort_with_students(self):
        """Test insertion sort with Student objects"""
        students = [
            Student(3, "Ion", 914),
            Student(1, "Ana", 912), 
            Student(2, "Maria", 913)
        ]
        
        # Sort by ID
        result = insertion_sort(students, key=lambda s: s.get_id())
        expected_ids = [1, 2, 3]
        actual_ids = [s.get_id() for s in result]
        self.assertEqual(actual_ids, expected_ids)
        
        # Sort by name
        result = insertion_sort(students, key=lambda s: s.get_name())
        expected_names = ["Ana", "Ion", "Maria"]
        actual_names = [s.get_name() for s in result]
        self.assertEqual(actual_names, expected_names)
    
    def test_comb_sort_with_students(self):
        """Test comb sort with Student objects"""
        students = [
            Student(3, "Ion", 914),
            Student(1, "Ana", 912), 
            Student(2, "Maria", 913)
        ]
        
        # Sort by group (descending)
        result = comb_sort(students, key=lambda s: s.get_group(), reverse=True)
        expected_groups = [914, 913, 912]
        actual_groups = [s.get_group() for s in result]
        self.assertEqual(actual_groups, expected_groups)
    
    def test_empty_list(self):
        """Test sorting empty lists"""
        self.assertEqual(insertion_sort([]), [])
        self.assertEqual(comb_sort([]), [])
    
    def test_single_element(self):
        """Test sorting single element lists"""
        self.assertEqual(insertion_sort([42]), [42])
        self.assertEqual(comb_sort([42]), [42])
    
    def test_already_sorted(self):
        """Test sorting already sorted lists"""
        data = [1, 2, 3, 4, 5]
        self.assertEqual(insertion_sort(data), data)
        self.assertEqual(comb_sort(data), data)
    
    def test_reverse_sorted(self):
        """Test sorting reverse sorted lists"""
        data = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(insertion_sort(data), expected)
        self.assertEqual(comb_sort(data), expected)
    
    def test_original_list_unchanged(self):
        """Test that original list is not modified"""
        original = [64, 34, 25, 12, 22, 11, 90]
        original_copy = original.copy()
        
        insertion_sort(original)
        self.assertEqual(original, original_copy)
        
        comb_sort(original)
        self.assertEqual(original, original_copy)


if __name__ == '__main__':
    unittest.main()