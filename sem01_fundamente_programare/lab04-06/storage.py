import numar_complex


def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


class UndoManager:
    """Manages undo operations without using deepcopy"""
    
    def __init__(self):
        self.history = []
    
    def save_state(self, numbers_list):
        """Save current state by creating a new list with the same numbers"""
        # Create a manual copy of the list
        state_copy = []
        for number in numbers_list:
            state_copy.append(numar_complex.ComplexNumber(number.real, number.imaginary))
        self.history.append(state_copy)
        
        # Keep only last 10 operations to avoid memory issues
        if len(self.history) > 10:
            self.history.pop(0)
    
    def can_undo(self):
        return len(self.history) > 0
    
    def get_last_state(self):
        if self.can_undo():
            return self.history.pop()
        return None


class DeltaUndoManager:
    """Git-like undo manager that tracks changes (deltas) instead of full states"""
    
    def __init__(self):
        self.operations = []  # Stack of operations that can be undone
    
    def record_append(self, number):
        """Record an append operation (undo: remove last element)"""
        operation = {
            'type': 'append',
            'number': numar_complex.ComplexNumber(number.real, number.imaginary)
        }
        self.operations.append(operation)
        self._maintain_history_limit()
    
    def record_insert(self, position, number):
        """Record an insert operation (undo: remove at position)"""
        operation = {
            'type': 'insert',
            'position': position,
            'number': numar_complex.ComplexNumber(number.real, number.imaginary)
        }
        self.operations.append(operation)
        self._maintain_history_limit()
    
    def record_delete(self, position, deleted_number):
        """Record a delete operation (undo: insert at position)"""
        operation = {
            'type': 'delete',
            'position': position,
            'number': numar_complex.ComplexNumber(deleted_number.real, deleted_number.imaginary)
        }
        self.operations.append(operation)
        self._maintain_history_limit()
    
    def record_delete_interval(self, start, end, deleted_numbers):
        """Record a delete interval operation (undo: insert all at positions)"""
        # Store numbers in reverse order for proper restoration
        stored_numbers = []
        for number in deleted_numbers:
            stored_numbers.append(numar_complex.ComplexNumber(number.real, number.imaginary))
        
        operation = {
            'type': 'delete_interval',
            'start': start,
            'end': end,
            'numbers': stored_numbers
        }
        self.operations.append(operation)
        self._maintain_history_limit()
    
    def record_replace_all(self, old_number, new_number, positions):
        """Record a replace all operation (undo: restore old values at positions)"""
        operation = {
            'type': 'replace_all',
            'old_number': numar_complex.ComplexNumber(old_number.real, old_number.imaginary),
            'new_number': numar_complex.ComplexNumber(new_number.real, new_number.imaginary),
            'positions': positions[:]  # Copy the list of positions
        }
        self.operations.append(operation)
        self._maintain_history_limit()
    
    def record_filter_operation(self, operation_type, removed_data):
        """Record a filter operation (undo: restore removed elements)"""
        # removed_data should be a list of (position, number) tuples
        stored_data = []
        for position, number in removed_data:
            stored_data.append((position, numar_complex.ComplexNumber(number.real, number.imaginary)))
        
        operation = {
            'type': 'filter',
            'operation_type': operation_type,
            'removed_data': stored_data
        }
        self.operations.append(operation)
        self._maintain_history_limit()
    
    def can_undo(self):
        """Check if there are operations to undo"""
        return len(self.operations) > 0
    
    def undo_last_operation(self, numbers_list):
        """Undo the last operation and return True if successful"""
        if not self.can_undo():
            return False
        
        operation = self.operations.pop()
        
        if operation['type'] == 'append':
            # Undo append: remove last element
            if len(numbers_list) > 0:
                numbers_list.pop()
        
        elif operation['type'] == 'insert':
            # Undo insert: remove at the position
            pos = operation['position']
            if 0 <= pos < len(numbers_list):
                numbers_list.pop(pos)
        
        elif operation['type'] == 'delete':
            # Undo delete: insert back at the position
            pos = operation['position']
            number = operation['number']
            if 0 <= pos <= len(numbers_list):
                numbers_list.insert(pos, number)
        
        elif operation['type'] == 'delete_interval':
            # Undo delete interval: insert all numbers back at their positions
            start = operation['start']
            numbers = operation['numbers']
            for i, number in enumerate(numbers):
                numbers_list.insert(start + i, number)
        
        elif operation['type'] == 'replace_all':
            # Undo replace all: restore old values at the recorded positions
            old_number = operation['old_number']
            positions = operation['positions']
            for pos in positions:
                if 0 <= pos < len(numbers_list):
                    numbers_list[pos] = numar_complex.ComplexNumber(old_number.real, old_number.imaginary)
        
        elif operation['type'] == 'filter':
            # Undo filter: restore all removed elements at their original positions
            removed_data = operation['removed_data']
            # For filter operations, we need to rebuild the entire list in correct order
            # Create a combined list of current and removed elements with their positions
            all_elements = []
            
            # Add current elements with their current positions
            for i, number in enumerate(numbers_list):
                all_elements.append((i, number, 'current'))
            
            # Add removed elements with their original positions
            for position, number in removed_data:
                all_elements.append((position, number, 'removed'))
            
            # Sort by position to get original order
            all_elements.sort(key=lambda x: x[0])
            
            # Rebuild the list with all elements
            numbers_list.clear()
            for position, number, element_type in all_elements:
                numbers_list.append(number)
        
        return True
    
    def _maintain_history_limit(self):
        """Keep only last 10 operations to avoid memory issues"""
        if len(self.operations) > 10:
            self.operations.pop(0)


class Storage:
    def __init__(self, numbers: list[numar_complex.ComplexNumber]):
        self.numbers = numbers
        self.undo_manager = UndoManager()  # Keep old implementation
        self.delta_undo_manager = DeltaUndoManager()  # New delta-based implementation

    def _save_state_before_modification(self):
        """Save current state before any modification (old method)"""
        self.undo_manager.save_state(self.numbers)

    def get_numbers(self):
        return self.numbers
    
    def append_number(self, new_number: numar_complex.ComplexNumber):
        self.delta_undo_manager.record_append(new_number)
        self.numbers.append(new_number)
        return self.numbers
    
    def pop_number(self):
        if len(self.numbers) > 0:
            deleted_number = self.numbers[-1]
            self.delta_undo_manager.record_delete(len(self.numbers) - 1, deleted_number)
            self.numbers.pop()
        return self.numbers
    
    def get_imaginary_parts_interval(self, start: int, end: int):
        if start < 0 or end >= len(self.numbers) or start > end:
            return []
        
        parts = []
        for i in range(start, end + 1):
            parts.append(self.numbers[i].imaginary)
        
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
    
    def insert_number_at_position(self, position: int, new_number: numar_complex.ComplexNumber):
        if position < 0 or position > len(self.numbers):
            raise ValueError(f"Position {position} is out of bounds. Valid range: 0-{len(self.numbers)}")
        
        self.delta_undo_manager.record_insert(position, new_number)
        self.numbers.insert(position, new_number)
        return self.numbers
    
    def delete_number_at_position(self, position: int):
        if position < 0 or position >= len(self.numbers):
            raise ValueError(f"Position {position} is out of bounds. Valid range: 0-{len(self.numbers)-1}")
        
        deleted_number = self.numbers[position]
        self.delta_undo_manager.record_delete(position, deleted_number)
        self.numbers.pop(position)
        return deleted_number
    
    def sum_numbers_interval(self, start: int, end: int):
        if start < 0 or end >= len(self.numbers) or start > end:
            raise ValueError(f"Invalid interval [{start}, {end}]. Valid range: 0-{len(self.numbers)-1}")
        
        if len(self.numbers) == 0:
            return numar_complex.ComplexNumber(0, 0)
        
        result = numar_complex.ComplexNumber(0, 0)
        for i in range(start, end + 1):
            result = result.add(self.numbers[i])
        
        return result
    
    def delete_numbers_interval(self, start: int, end: int):
        """Delete numbers from start to end positions (inclusive)"""
        if start < 0 or end >= len(self.numbers) or start > end:
            raise ValueError(f"Invalid interval [{start}, {end}]. Valid range: 0-{len(self.numbers)-1}")
        
        # Collect numbers that will be deleted for undo
        deleted_numbers = []
        for i in range(start, end + 1):
            deleted_numbers.append(self.numbers[i])
        
        self.delta_undo_manager.record_delete_interval(start, end, deleted_numbers)
        
        # Delete from end to start to maintain correct indices
        deleted_count = 0
        for i in range(end, start - 1, -1):
            self.numbers.pop(i)
            deleted_count += 1
        
        return deleted_count
    
    def replace_all_occurrences(self, old_number: numar_complex.ComplexNumber, new_number: numar_complex.ComplexNumber):
        """Replace all occurrences of old_number with new_number"""
        replacements = 0
        positions = []
        
        # First find all positions that need replacement
        for i, number in enumerate(self.numbers):
            if number.equals(old_number):
                replacements += 1
                positions.append(i)
        
        if replacements > 0:
            self.delta_undo_manager.record_replace_all(old_number, new_number, positions)
            
            # Replace all occurrences
            for i in positions:
                self.numbers[i] = numar_complex.ComplexNumber(new_number.real, new_number.imaginary)
        
        return replacements
    
    def product_numbers_interval(self, start: int, end: int):
        """Calculate product of numbers from start to end positions (inclusive)"""
        if start < 0 or end >= len(self.numbers) or start > end:
            raise ValueError(f"Invalid interval [{start}, {end}]. Valid range: 0-{len(self.numbers)-1}")
        
        if len(self.numbers) == 0:
            return numar_complex.ComplexNumber(1, 0)
        
        result = numar_complex.ComplexNumber(1, 0)
        for i in range(start, end + 1):
            result = result.multiply(self.numbers[i])
        
        return result
    
    def get_sorted_by_imaginary(self, descending=True):
        """Get a new list sorted by imaginary part"""
        sorted_numbers = []
        for number in self.numbers:
            sorted_numbers.append(numar_complex.ComplexNumber(number.real, number.imaginary))
        
        # Simple bubble sort implementation
        n = len(sorted_numbers)
        for i in range(n):
            for j in range(0, n - i - 1):
                if descending:
                    if sorted_numbers[j].imaginary < sorted_numbers[j + 1].imaginary:
                        sorted_numbers[j], sorted_numbers[j + 1] = sorted_numbers[j + 1], sorted_numbers[j]
                else:
                    if sorted_numbers[j].imaginary > sorted_numbers[j + 1].imaginary:
                        sorted_numbers[j], sorted_numbers[j + 1] = sorted_numbers[j + 1], sorted_numbers[j]
        
        return sorted_numbers
    
    def filter_real_part_prime(self):
        """Remove numbers where real part is prime"""
        removed_data = []  # Store (position, number) tuples for undo
        filtered_numbers = []
        removed_count = 0
        
        for i, number in enumerate(self.numbers):
            if not is_prime(abs(number.real)):  # Use absolute value for negative primes
                filtered_numbers.append(number)
            else:
                removed_data.append((i, number))
                removed_count += 1
        
        if removed_count > 0:
            self.delta_undo_manager.record_filter_operation("filter_real_part_prime", removed_data)
            self.numbers = filtered_numbers
        
        return removed_count
    
    def filter_by_module(self, operator: str, value: float):
        """Filter numbers by module using operator (<, =, >)"""
        removed_data = []  # Store (position, number) tuples for undo
        filtered_numbers = []
        removed_count = 0
        
        for i, number in enumerate(self.numbers):
            module = number.get_module()
            keep_number = False
            
            if operator == "<":
                keep_number = module >= value
            elif operator == "=":
                keep_number = abs(module - value) >= 0.001
            elif operator == ">":
                keep_number = module <= value
            
            if keep_number:
                filtered_numbers.append(number)
            else:
                removed_data.append((i, number))
                removed_count += 1
        
        if removed_count > 0:
            self.delta_undo_manager.record_filter_operation(f"filter_by_module_{operator}_{value}", removed_data)
            self.numbers = filtered_numbers
        
        return removed_count
    
    def undo_last_operation(self):
        """Undo the last operation that modified the list using delta-based approach"""
        if self.delta_undo_manager.can_undo():
            return self.delta_undo_manager.undo_last_operation(self.numbers)
        return False



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

    # Test insert at position
    n4 = numar_complex.ComplexNumber(2, 3)
    storage.insert_number_at_position(1, n4)  # Insert at position 1
    assert(len(storage.numbers) == 4)
    assert(storage.numbers[1].real == 2)
    assert(storage.numbers[1].imaginary == 3)

    # Test delete at position
    deleted = storage.delete_number_at_position(1)  # Remove the inserted number
    assert(deleted.real == 2)
    assert(deleted.imaginary == 3)
    assert(len(storage.numbers) == 3)

    # Test sum interval
    result_sum = storage.sum_numbers_interval(0, 2)  # Sum all three numbers
    assert(result_sum.real == 10)  # 3 + 6 + 1
    assert(result_sum.imaginary == 13)  # 4 + 8 + 1

    # Test partial sum
    result_sum2 = storage.sum_numbers_interval(0, 1)  # Sum first two
    assert(result_sum2.real == 9)  # 3 + 6
    assert(result_sum2.imaginary == 12)  # 4 + 8

    # Test new iteration 3 functionality
    storage2 = Storage([])
    n5 = numar_complex.ComplexNumber(2, 1)
    n6 = numar_complex.ComplexNumber(3, 4)
    n7 = numar_complex.ComplexNumber(2, 1)  # Same as n5 for replacement test
    storage2.append_number(n5)
    storage2.append_number(n6)
    storage2.append_number(n7)

    # Test delete interval
    deleted_count = storage2.delete_numbers_interval(1, 2)
    assert(deleted_count == 2)
    assert(len(storage2.numbers) == 1)
    assert(storage2.numbers[0].equals(n5))

    # Reset for replacement test
    storage2.numbers = [n5, n6, n7]
    replacement_count = storage2.replace_all_occurrences(n5, numar_complex.ComplexNumber(9, 9))
    assert(replacement_count == 2)
    assert(storage2.numbers[0].real == 9)
    assert(storage2.numbers[2].real == 9)

    # Test product interval
    storage3 = Storage([])
    storage3.append_number(numar_complex.ComplexNumber(2, 1))
    storage3.append_number(numar_complex.ComplexNumber(3, 4))
    product = storage3.product_numbers_interval(0, 1)
    assert(product.real == 2)  # (2+i)*(3+4i) = 2+11i
    assert(product.imaginary == 11)

    # Test sorting by imaginary part
    storage4 = Storage([])
    storage4.append_number(numar_complex.ComplexNumber(1, 5))
    storage4.append_number(numar_complex.ComplexNumber(2, 1))
    storage4.append_number(numar_complex.ComplexNumber(3, 8))
    sorted_numbers = storage4.get_sorted_by_imaginary(True)
    assert(sorted_numbers[0].imaginary == 8)
    assert(sorted_numbers[1].imaginary == 5)
    assert(sorted_numbers[2].imaginary == 1)

    # Test prime filtering
    storage5 = Storage([])
    storage5.append_number(numar_complex.ComplexNumber(3, 1))  # 3 is prime
    storage5.append_number(numar_complex.ComplexNumber(4, 2))  # 4 is not prime
    storage5.append_number(numar_complex.ComplexNumber(5, 3))  # 5 is prime
    removed = storage5.filter_real_part_prime()
    assert(removed == 2)
    assert(len(storage5.numbers) == 1)
    assert(storage5.numbers[0].real == 4)

    # Test module filtering
    storage6 = Storage([])
    storage6.append_number(numar_complex.ComplexNumber(3, 4))  # module = 5
    storage6.append_number(numar_complex.ComplexNumber(6, 8))  # module = 10
    storage6.append_number(numar_complex.ComplexNumber(1, 1))  # module ≈ 1.41
    removed = storage6.filter_by_module("<", 5.0)
    assert(removed == 1)  # Only 1+1i should be removed
    assert(len(storage6.numbers) == 2)

    # Test delta undo functionality
    storage7 = Storage([])
    storage7.append_number(numar_complex.ComplexNumber(1, 1))
    storage7.append_number(numar_complex.ComplexNumber(2, 2))
    assert(len(storage7.numbers) == 2)
    
    storage7.delete_number_at_position(1)
    assert(len(storage7.numbers) == 1)
    
    success = storage7.undo_last_operation()
    assert(success == True)
    assert(len(storage7.numbers) == 2)
    assert(storage7.numbers[1].real == 2)

    # Test utility functions
    assert(is_prime(2) == True)
    assert(is_prime(3) == True)
    assert(is_prime(4) == False)
    assert(is_prime(17) == True)
    assert(is_prime(1) == False)
    assert(is_prime(0) == False)


def test_delta_undo_manager():
    """Comprehensive tests for DeltaUndoManager"""
    
    # Test append and undo
    storage = Storage([])
    n1 = numar_complex.ComplexNumber(3, 4)
    storage.append_number(n1)
    assert(len(storage.numbers) == 1)
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 0)
    
    # Test insert and undo
    storage = Storage([numar_complex.ComplexNumber(1, 1)])
    n2 = numar_complex.ComplexNumber(2, 2)
    storage.insert_number_at_position(0, n2)
    assert(len(storage.numbers) == 2)
    assert(storage.numbers[0].real == 2)
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 1)
    assert(storage.numbers[0].real == 1)
    
    # Test delete and undo
    storage = Storage([numar_complex.ComplexNumber(1, 1), numar_complex.ComplexNumber(2, 2)])
    deleted = storage.delete_number_at_position(0)
    assert(deleted.real == 1)
    assert(len(storage.numbers) == 1)
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 2)
    assert(storage.numbers[0].real == 1)
    
    # Test delete interval and undo
    storage = Storage([
        numar_complex.ComplexNumber(1, 1),
        numar_complex.ComplexNumber(2, 2),
        numar_complex.ComplexNumber(3, 3),
        numar_complex.ComplexNumber(4, 4)
    ])
    deleted_count = storage.delete_numbers_interval(1, 2)
    assert(deleted_count == 2)
    assert(len(storage.numbers) == 2)
    assert(storage.numbers[0].real == 1)
    assert(storage.numbers[1].real == 4)
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 4)
    assert(storage.numbers[1].real == 2)
    assert(storage.numbers[2].real == 3)
    
    # Test replace all and undo
    storage = Storage([
        numar_complex.ComplexNumber(1, 1),
        numar_complex.ComplexNumber(2, 2),
        numar_complex.ComplexNumber(1, 1)
    ])
    old_num = numar_complex.ComplexNumber(1, 1)
    new_num = numar_complex.ComplexNumber(9, 9)
    replaced = storage.replace_all_occurrences(old_num, new_num)
    assert(replaced == 2)
    assert(storage.numbers[0].real == 9)
    assert(storage.numbers[2].real == 9)
    assert(storage.undo_last_operation() == True)
    assert(storage.numbers[0].real == 1)
    assert(storage.numbers[2].real == 1)
    
    # Test filter prime and undo
    storage = Storage([
        numar_complex.ComplexNumber(2, 1),  # 2 is prime
        numar_complex.ComplexNumber(4, 2),  # 4 is not prime
        numar_complex.ComplexNumber(3, 3)   # 3 is prime
    ])
    removed = storage.filter_real_part_prime()
    assert(removed == 2)
    assert(len(storage.numbers) == 1)
    assert(storage.numbers[0].real == 4)
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 3)
    # After undo, check that all original numbers are back (order may differ)
    real_parts = [n.real for n in storage.numbers]
    assert(2 in real_parts)
    assert(3 in real_parts)
    assert(4 in real_parts)
    
    # Test filter by module and undo  
    storage = Storage([
        numar_complex.ComplexNumber(3, 4),  # module = 5
        numar_complex.ComplexNumber(1, 1),  # module ≈ 1.41
        numar_complex.ComplexNumber(6, 8)   # module = 10
    ])
    removed = storage.filter_by_module("<", 3.0)
    assert(removed == 1)  # Only 1+1i should be removed
    assert(len(storage.numbers) == 2)
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 3)
    # Check that 1+1i is back in the list (position may differ)
    real_parts = [n.real for n in storage.numbers]
    assert(1 in real_parts)
    
    # Test multiple operations and undo
    storage = Storage([])
    storage.append_number(numar_complex.ComplexNumber(1, 1))
    storage.append_number(numar_complex.ComplexNumber(2, 2))
    storage.insert_number_at_position(1, numar_complex.ComplexNumber(15, 15))
    assert(len(storage.numbers) == 3)
    assert(storage.numbers[1].real == 15)
    
    # Undo insert
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 2)
    assert(storage.numbers[1].real == 2)
    
    # Undo second append
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 1)
    assert(storage.numbers[0].real == 1)
    
    # Undo first append
    assert(storage.undo_last_operation() == True)
    assert(len(storage.numbers) == 0)
    
    # No more operations to undo
    assert(storage.undo_last_operation() == False)
    
    # Test history limit (should keep only last 10 operations)
    storage = Storage([])
    for i in range(15):
        storage.append_number(numar_complex.ComplexNumber(i, i))
    
    # Try to undo more than 10 operations
    undo_count = 0
    while storage.undo_last_operation():
        undo_count += 1
    
    assert(undo_count == 10)  # Should only undo last 10 operations
    assert(len(storage.numbers) == 5)  # 15 - 10 = 5