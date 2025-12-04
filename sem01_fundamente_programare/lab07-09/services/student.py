import random
from repos.student import StudentRepository
from domain.student import Student
from domain.assignment import Assignment
from domain.student_statistic import StudentStatistic
from typing import List



class StudentService:
    def __init__(self):
        self._student_repo = StudentRepository([])

    def generate_random_name(self) -> str:
        char_options = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # choose a random length, or fix one — here I'll pick length 8
        length = 8
        return ''.join(random.choice(char_options) for _ in range(length))

    def generate_random_group(self) -> int:
        # choose any range you want — here I'll use 1 to 999
        return random.randint(1, 999)

    def add_student(self,name:str,group:int):
        student = self._student_repo.add_student(name, group)
        return student

    def list_students(self) -> list[Student]:
        students = self._student_repo.get_all_students()
        return students
    
    def remove_student(self, student_id: int):
        """Remove a student by ID. Raises ValueError if not found."""
        try:
            self._student_repo.remove_student(student_id)
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def modify_student(self, student_id: int, new_name: str, new_group: int) -> None:
        """Modify an existing student's name and group. Raises ValueError if not found."""
        try:
            self._student_repo.modify_student(student_id, new_name, new_group)
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def search_students(self, search_term: str, search_type: str) -> list[Student]:
        """Search for students by name, id, or group"""
        results = self._student_repo.search_students(search_term, search_type)
        return results

    def get_top_students(self, assignments: list, limit: int = 10) -> List[StudentStatistic]:
        """Get top students by average grade"""        
        students = self._student_repo.get_all_students()
        student_stats = []
        
        for student in students:
            student_assignments = [a for a in assignments if a.get_student_id() == student.get_id()]
            graded_assignments = [a for a in student_assignments if a.has_grade()]
            
            if graded_assignments:
                avg_grade = sum(a.get_grade() for a in graded_assignments) / len(graded_assignments)
                student_stats.append(StudentStatistic(
                    student_id=student.get_id(),
                    student_name=student.get_name(),
                    group=student.get_group(),
                    average_grade=avg_grade,
                    total_assignments=len(student_assignments),
                    graded_assignments=len(graded_assignments)
                ))
        
        # Sort by average grade descending
        student_stats.sort(key=lambda x: x.get_average_grade(), reverse=True)
        return student_stats[:limit]

