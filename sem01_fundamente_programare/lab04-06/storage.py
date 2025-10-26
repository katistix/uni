import numar_complex

class Storage:
    def __init__(self, numbers: list[numar_complex.ComplexNumber]):
        self.numbers = numbers

    def get_numbers(self):
        return self.numbers
    
    def append_number(self, new_number: numar_complex.ComplexNumber):
        self.numbers.append(new_number)

        return self.numbers
    
    def pop_number(self):
        self.numbers.pop()

        return self.numbers
    
    def get_imaginary_parts_interval(self, start: int, end: int):
        if start < 0 or end >= len(self.numbers) or start > end:
            return []
        
        parts = []
        for i in range(start, end + 1):
            parts.append(self.numbers[i].get_imaginary())
        
        return parts
    
    def get_numbers_module_less_than(self, value: float):
        numbers = []
        for number in self.numbers:
            if number.get_module() < value:
                numbers.append(number)
        
        return numbers
    
    def get_numbers_module_equal(self, value: float):
        numbers = []
        for number in self.numbers:
            if abs(number.get_module() - value) < 0.001:
                numbers.append(number)
        
        return numbers



def test_module():
    storage = Storage([])
    assert(storage.get_numbers() == [])

    n1 = numar_complex.ComplexNumber(3, 4)
    n2 = numar_complex.ComplexNumber(6, 8)
    n3 = numar_complex.ComplexNumber(1, 1)

    storage.append_number(n1)
    assert(len(storage.numbers) == 1)

    storage.append_number(n2)
    storage.append_number(n3)
    assert(len(storage.numbers) == 3)

    # Test interval imaginary parts
    parts = storage.get_imaginary_parts_interval(0, 2)
    assert(parts == [4, 8, 1])

    parts = storage.get_imaginary_parts_interval(0, 1)
    assert(parts == [4, 8])

    # Test module filters
    small_numbers = storage.get_numbers_module_less_than(10.0)
    assert(len(small_numbers) == 2)  # 3+4i and 1+1i

    equal_numbers = storage.get_numbers_module_equal(10.0)
    assert(len(equal_numbers) == 1)  # 6+8i