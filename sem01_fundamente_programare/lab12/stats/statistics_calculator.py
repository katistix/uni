from typing import List, Optional
from dataclasses import dataclass
from domain.student import Student
from domain.problem import Problem
from domain.assignment import Assignment

@dataclass
class StudentStatistics:
    student_id: int
    student_name: str
    total_assignments: int
    graded_assignments: int
    average_grade: Optional[float]

@dataclass
class ProblemStatistics:
    problem_id: str
    description: str
    total_assignments: int
    graded_assignments: int
    completion_rate: float

@dataclass
class GroupReport:
    group_id: int
    total_students: int
    students_with_assignments: int

class StatisticsCalculator:
    def __init__(self, students: List[Student], problems: List[Problem], assignments: List[Assignment]):
        self._students = students
        self._problems = problems
        self._assignments = assignments

    def calculate_student_statistics(self) -> List[StudentStatistics]:
        stats = []
        for student in self._students:
            student_assignments = [a for a in self._assignments if a.get_student_id() == student.get_id()]
            graded_assignments = [a for a in student_assignments if a.has_grade()]
            
            total = len(student_assignments)
            graded = len(graded_assignments)
            
            avg = None
            if graded > 0:
                avg = sum(a.get_grade() for a in graded_assignments) / graded
                
            stats.append(StudentStatistics(
                student.get_id(),
                student.get_name(),
                total,
                graded,
                avg
            ))
        # Sort by average grade descending
        stats.sort(key=lambda s: s.average_grade if s.average_grade is not None else -1, reverse=True)
        return stats

    def calculate_problem_statistics(self) -> List[ProblemStatistics]:
        stats = []
        total_students = len(self._students)
        
        for problem in self._problems:
            problem_id = f"{problem.get_lab_number()}_{problem.get_problem_number()}"
            problem_assignments = [a for a in self._assignments if a.get_problem_id() == problem_id]
            graded_assignments = [a for a in problem_assignments if a.has_grade()]
            
            total = len(problem_assignments)
            graded = len(graded_assignments)
            
            completion_rate = 0.0
            if total_students > 0:
                completion_rate = (total / total_students) * 100
                
            stats.append(ProblemStatistics(
                problem_id,
                problem.get_description(),
                total,
                graded,
                completion_rate
            ))
        return stats

    def generate_group_report(self, group_id: int) -> GroupReport:
        group_students = [s for s in self._students if s.get_group() == group_id]
        total_students = len(group_students)
        
        students_with_assignments = 0
        for student in group_students:
            has_assignment = any(a.get_student_id() == student.get_id() for a in self._assignments)
            if has_assignment:
                students_with_assignments += 1
                
        return GroupReport(group_id, total_students, students_with_assignments)

class ReportExporter:
    @staticmethod
    def export_student_statistics(stats: List[StudentStatistics], filepath: str):
        with open(filepath, 'w') as f:
            f.write("Student ID,Name,Total Assignments,Graded Assignments,Average Grade\n")
            for s in stats:
                avg_str = f"{s.average_grade:.2f}" if s.average_grade is not None else ""
                f.write(f"{s.student_id},{s.student_name},{s.total_assignments},{s.graded_assignments},{avg_str}\n")

    @staticmethod
    def export_problem_statistics(stats: List[ProblemStatistics], filepath: str):
        with open(filepath, 'w') as f:
            f.write("Problem ID,Description,Total Assignments,Graded Assignments,Completion Rate\n")
            for s in stats:
                f.write(f"{s.problem_id},{s.description},{s.total_assignments},{s.graded_assignments},{s.completion_rate:.2f}%\n")

    @staticmethod
    def export_all_grades(students: List[Student], assignments: List[Assignment], filepath: str):
        with open(filepath, 'w') as f:
            f.write("Student Name,Group,Problem ID,Grade\n")
            for assignment in assignments:
                student = next((s for s in students if s.get_id() == assignment.get_student_id()), None)
                if student:
                    grade_str = str(assignment.get_grade()) if assignment.has_grade() else "Ungraded"
                    f.write(f"{student.get_name()},{student.get_group()},{assignment.get_problem_id()},{grade_str}\n")
