from domain.student import Student

class StudentRepository:
    def __init__(self, student_list: list[Student]):
        self._student_list = student_list
        self._next_id = max((s.id for s in student_list), default=0) + 1

    def add_student(self, name: str, group: int) -> Student:
        new_student = Student(self._next_id, name, group)
        self._student_list.append(new_student)
        self._next_id += 1
        return new_student

    def remove_student(self, student_id: int) -> None:
        """Remove a student by ID. Raises ValueError if not found."""
        for student in self._student_list:
            if student.id == student_id:
                self._student_list.remove(student)
                return
        raise ValueError(f"Student with id {student_id} not found")

    def modify_student(self, student_id: int, new_name: str, new_group: int) -> None:
        """Modify an existing student's name and group. Raises ValueError if not found."""
        for student in self._student_list:
            if student.id == student_id:
                student.set_name(new_name)
                student.set_group(new_group)
                return
        raise ValueError(f"Student with id {student_id} not found")

    def get_all_students(self) -> list[Student]:
        """Return a copy of all students in the repository."""
        return self._student_list.copy()

    def search_students(self, search_term: str, search_type: str) -> list[Student]:
        """Search for students by name, id, or group.
        
        Args:
            search_term: The term to search for
            search_type: The type of search ('name', 'id', 'group')
        
        Returns:
            List of matching students
        """
        results = []
        
        if search_type == 'id':
            try:
                search_id = int(search_term)
                for student in self._student_list:
                    if student.get_id() == search_id:
                        results.append(student)
            except ValueError:
                pass
        elif search_type == 'name':
            search_term_lower = search_term.lower()
            for student in self._student_list:
                if search_term_lower in student.get_name().lower():
                    results.append(student)
        elif search_type == 'group':
            try:
                search_group = int(search_term)
                for student in self._student_list:
                    if student.get_group() == search_group:
                        results.append(student)
            except ValueError:
                pass
        
        return results

    def find_student_by_id(self, student_id: int) -> Student | None:
        """Find a student by ID. Returns the student or None if not found."""
        for student in self._student_list:
            if student.get_id() == student_id:
                return student
        return None


