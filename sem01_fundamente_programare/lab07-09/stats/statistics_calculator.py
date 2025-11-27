import os
import sys
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
import csv

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from domain.student import Student
from domain.problem import Problem
from domain.assignment import Assignment


@dataclass
class StudentStatistics:
    student_id: int
    student_name: str
    group: int
    total_assignments: int
    graded_assignments: int
    average_grade: Optional[float]
    
    def to_csv_row(self) -> dict:
        return {
            'student_id': self.student_id,
            'student_name': self.student_name,
            'group': self.group,
            'total_assignments': self.total_assignments,
            'graded_assignments': self.graded_assignments,
            'average_grade': f"{self.average_grade:.2f}" if self.average_grade is not None else "N/A"
        }


@dataclass
class ProblemStatistics:
    problem_id: str
    description: str
    total_assignments: int
    graded_assignments: int
    completion_rate: float
    average_grade: Optional[float]
    
    def to_csv_row(self) -> dict:
        return {
            'problem_id': self.problem_id,
            'description': self.description,
            'total_assignments': self.total_assignments,
            'graded_assignments': self.graded_assignments,
            'completion_rate': f"{self.completion_rate:.1f}%",
            'average_grade': f"{self.average_grade:.2f}" if self.average_grade is not None else "N/A"
        }


@dataclass
class GroupReport:
    group_number: int
    total_students: int
    students_with_assignments: int
    total_assignments: int
    graded_assignments: int
    group_average_grade: Optional[float]
    best_student: Optional[Tuple[str, float]]  # (name, grade)
    lowest_student: Optional[Tuple[str, float]]  # (name, grade)
    
    def to_csv_row(self) -> dict:
        return {
            'group_number': self.group_number,
            'total_students': self.total_students,
            'students_with_assignments': self.students_with_assignments,
            'total_assignments': self.total_assignments,
            'graded_assignments': self.graded_assignments,
            'group_average_grade': f"{self.group_average_grade:.2f}" if self.group_average_grade is not None else "N/A",
            'best_student': f"{self.best_student[0]} ({self.best_student[1]:.2f})" if self.best_student else "N/A",
            'lowest_student': f"{self.lowest_student[0]} ({self.lowest_student[1]:.2f})" if self.lowest_student else "N/A"
        }


class StatisticsCalculator:
    """Calculate various statistics for students, problems, and groups"""
    
    def __init__(self, students: List[Student], problems: List[Problem], assignments: List[Assignment]):
        self.students = students
        self.problems = problems
        self.assignments = assignments
        
        # Create lookup dictionaries for efficiency
        self.student_lookup = {s.get_id(): s for s in students}
        self.problem_lookup = {f"{p.get_lab_number()}_{p.get_problem_number()}": p for p in problems}
    
    def calculate_student_statistics(self) -> List[StudentStatistics]:
        """Calculate statistics for all students"""
        stats = []
        
        for student in self.students:
            student_assignments = [a for a in self.assignments if a.get_student_id() == student.get_id()]
            graded_assignments = [a for a in student_assignments if a.has_grade()]
            
            total_assignments = len(student_assignments)
            graded_count = len(graded_assignments)
            
            average_grade = None
            if graded_count > 0:
                grades = []
                for assignment in graded_assignments:
                    grade = assignment.get_grade()
                    if grade is not None:
                        grades.append(grade)
                if grades:
                    average_grade = sum(grades) / len(grades)
            
            stats.append(StudentStatistics(
                student_id=student.get_id(),
                student_name=student.get_name(),
                group=student.get_group(),
                total_assignments=total_assignments,
                graded_assignments=graded_count,
                average_grade=average_grade
            ))
        
        # Sort by average grade (descending), then by name
        stats.sort(key=lambda s: (-(s.average_grade or -1), s.student_name))
        return stats
    
    def calculate_problem_statistics(self) -> List[ProblemStatistics]:
        """Calculate statistics for all problems"""
        stats = []
        
        for problem in self.problems:
            problem_id = f"{problem.get_lab_number()}_{problem.get_problem_number()}"
            problem_assignments = [a for a in self.assignments if a.get_problem_id() == problem_id]
            graded_assignments = [a for a in problem_assignments if a.has_grade()]
            
            total_assignments = len(problem_assignments)
            graded_count = len(graded_assignments)
            
            completion_rate = (graded_count / total_assignments * 100) if total_assignments > 0 else 0
            
            average_grade = None
            if graded_count > 0:
                grades = []
                for assignment in graded_assignments:
                    grade = assignment.get_grade()
                    if grade is not None:
                        grades.append(grade)
                if grades:
                    average_grade = sum(grades) / len(grades)
            
            stats.append(ProblemStatistics(
                problem_id=problem_id,
                description=problem.get_description(),
                total_assignments=total_assignments,
                graded_assignments=graded_count,
                completion_rate=completion_rate,
                average_grade=average_grade
            ))
        
        # Sort by completion rate (descending), then by average grade
        stats.sort(key=lambda s: (-s.completion_rate, -(s.average_grade or -1)))
        return stats
    
    def generate_group_report(self, group_number: int) -> GroupReport:
        """Generate detailed report for a specific group"""
        group_students = [s for s in self.students if s.get_group() == group_number]
        
        if not group_students:
            return GroupReport(
                group_number=group_number,
                total_students=0,
                students_with_assignments=0,
                total_assignments=0,
                graded_assignments=0,
                group_average_grade=None,
                best_student=None,
                lowest_student=None
            )
        
        # Calculate group statistics
        total_students = len(group_students)
        student_stats = []
        
        total_assignments = 0
        graded_assignments = 0
        all_grades = []
        
        for student in group_students:
            student_assignments = [a for a in self.assignments if a.get_student_id() == student.get_id()]
            student_graded = [a for a in student_assignments if a.has_grade()]
            
            total_assignments += len(student_assignments)
            graded_assignments += len(student_graded)
            
            if student_graded:
                grades = []
                for assignment in student_graded:
                    grade = assignment.get_grade()
                    if grade is not None:
                        grades.append(grade)
                if grades:
                    student_avg = sum(grades) / len(grades)
                    student_stats.append((student.get_name(), student_avg))
                    all_grades.extend(grades)
        
        students_with_assignments = len([s for s in group_students 
                                       if any(a.get_student_id() == s.get_id() for a in self.assignments)])
        
        group_average_grade = sum(all_grades) / len(all_grades) if all_grades else None
        
        # Find best and worst students (based on average grades)
        best_student = max(student_stats, key=lambda x: x[1]) if student_stats else None
        lowest_student = min(student_stats, key=lambda x: x[1]) if student_stats else None
        
        return GroupReport(
            group_number=group_number,
            total_students=total_students,
            students_with_assignments=students_with_assignments,
            total_assignments=total_assignments,
            graded_assignments=graded_assignments,
            group_average_grade=group_average_grade,
            best_student=best_student,
            lowest_student=lowest_student
        )
    
    def get_all_groups(self) -> List[int]:
        """Get list of all group numbers"""
        groups = set(s.get_group() for s in self.students)
        return sorted(groups)
    
    def get_top_students(self, limit: int = 10) -> List[StudentStatistics]:
        """Get top students ranked by average grade"""
        stats = self.calculate_student_statistics()
        # Filter only students with grades and sort by average grade descending
        graded_stats = [s for s in stats if s.average_grade is not None]
        graded_stats.sort(key=lambda s: s.average_grade or 0, reverse=True)
        return graded_stats[:limit]
    
    def get_group_rankings(self) -> List[Tuple[int, float, int]]:
        """Get groups ranked by average grade. Returns (group_number, average_grade, student_count)"""
        groups = self.get_all_groups()
        group_rankings = []
        
        for group in groups:
            report = self.generate_group_report(group)
            if report.group_average_grade is not None:
                group_rankings.append((
                    group, 
                    report.group_average_grade, 
                    report.students_with_assignments
                ))
        
        # Sort by average grade descending
        group_rankings.sort(key=lambda x: x[1], reverse=True)
        return group_rankings
    
    def get_difficult_problems(self) -> List[ProblemStatistics]:
        """Get problems ranked by difficulty (lowest average grade)"""
        stats = self.calculate_problem_statistics()
        # Filter only problems with grades and sort by average grade ascending (lowest first = most difficult)
        graded_stats = [s for s in stats if s.average_grade is not None]
        graded_stats.sort(key=lambda s: s.average_grade or 0)
        return graded_stats
    
    def get_problem_popularity(self) -> List[ProblemStatistics]:
        """Get problems ranked by how many students attempted them"""
        stats = self.calculate_problem_statistics()
        # Sort by total assignments descending
        stats.sort(key=lambda s: s.total_assignments, reverse=True)
        return stats
    
    def get_top_problems(self, limit: int = 10) -> List[ProblemStatistics]:
        """Get top problems ranked by number of assignments (most popular)"""
        stats = self.calculate_problem_statistics()
        # Sort by total assignments descending (most assignments = most popular)
        stats.sort(key=lambda s: s.total_assignments, reverse=True)
        return stats[:limit]
    
    def get_students_below_threshold(self, threshold: float = 5.0) -> List[StudentStatistics]:
        """Get students with average grade below threshold"""
        stats = self.calculate_student_statistics()
        return [s for s in stats if s.average_grade is not None and s.average_grade < threshold]
    
    def get_grade_distribution(self) -> Dict[str, int]:
        """Get distribution of grades by ranges"""
        distribution = {
            "10": 0,      # Grade 10
            "9-9.99": 0,  # Grade 9.00-9.99
            "8-8.99": 0,  # Grade 8.00-8.99
            "7-7.99": 0,  # Grade 7.00-7.99
            "6-6.99": 0,  # Grade 6.00-6.99
            "5-5.99": 0,  # Grade 5.00-5.99
            "0-4.99": 0   # Below 5 (failing)
        }
        
        for assignment in self.assignments:
            if assignment.has_grade():
                grade = assignment.get_grade()
                if grade is not None:
                    if grade == 10:
                        distribution["10"] += 1
                    elif grade >= 9:
                        distribution["9-9.99"] += 1
                    elif grade >= 8:
                        distribution["8-8.99"] += 1
                    elif grade >= 7:
                        distribution["7-7.99"] += 1
                    elif grade >= 6:
                        distribution["6-6.99"] += 1
                    elif grade >= 5:
                        distribution["5-5.99"] += 1
                    else:
                        distribution["0-4.99"] += 1
        
        return distribution
    
    def generate_top_report(self, k: int = 3):
        """Generate a k*k report with top k students and top k problems"""
        top_students = self.get_top_students(k)
        top_problems = self.get_top_problems(k)
        
        # Create matrix data
        matrix_data = []
        
        for student_stat in top_students:
            student_row = {
                'student_id': student_stat.student_id,
                'student_name': student_stat.student_name,
                'student_avg': student_stat.average_grade,
                'problem_data': {}
            }
            
            # For each top problem, find this student's performance
            for problem_stat in top_problems:
                problem_id = problem_stat.problem_id
                
                # Find assignments for this student and problem
                student_assignments = [a for a in self.assignments 
                                     if a.get_student_id() == student_stat.student_id 
                                     and a.get_problem_id() == problem_id]
                
                if student_assignments:
                    # Get the grade if exists
                    assignment = student_assignments[0]  # Should be only one
                    grade = assignment.get_grade() if assignment.has_grade() else "Not graded"
                    status = "Graded" if assignment.has_grade() else "Assigned"
                else:
                    grade = "Not assigned"
                    status = "Not assigned"
                
                student_row['problem_data'][problem_id] = {
                    'grade': grade,
                    'status': status,
                    'problem_desc': problem_stat.description,
                    'problem_assignments': problem_stat.total_assignments
                }
            
            matrix_data.append(student_row)
        
        return {
            'top_students': top_students,
            'top_problems': top_problems,
            'matrix_data': matrix_data,
            'k': k
        }


class ReportExporter:
    """Export reports and statistics to CSV files"""
    
    @staticmethod
    def export_student_statistics(stats: List[StudentStatistics], filepath: str) -> None:
        """Export student statistics to CSV"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        fieldnames = ['student_id', 'student_name', 'group', 'total_assignments', 'graded_assignments', 'average_grade']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for stat in stats:
                writer.writerow(stat.to_csv_row())
    
    @staticmethod
    def export_problem_statistics(stats: List[ProblemStatistics], filepath: str) -> None:
        """Export problem statistics to CSV"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        fieldnames = ['problem_id', 'description', 'total_assignments', 'graded_assignments', 'completion_rate', 'average_grade']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for stat in stats:
                writer.writerow(stat.to_csv_row())
    
    @staticmethod
    def export_group_report(report: GroupReport, filepath: str) -> None:
        """Export group report to CSV"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        fieldnames = ['group_number', 'total_students', 'students_with_assignments', 'total_assignments', 
                     'graded_assignments', 'group_average_grade', 'best_student', 'lowest_student']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(report.to_csv_row())
    
    @staticmethod
    def export_all_grades(students: List[Student], assignments: List[Assignment], filepath: str) -> None:
        """Export all grades in a detailed CSV format"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        student_lookup = {s.get_id(): s for s in students}
        
        fieldnames = ['student_id', 'student_name', 'group', 'problem_id', 'grade', 'graded']
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for assignment in assignments:
                student = student_lookup.get(assignment.get_student_id())
                if student:
                    writer.writerow({
                        'student_id': assignment.get_student_id(),
                        'student_name': student.get_name(),
                        'group': student.get_group(),
                        'problem_id': assignment.get_problem_id(),
                        'grade': assignment.get_grade() if assignment.has_grade() else '',
                        'graded': 'Yes' if assignment.has_grade() else 'No'
                    })


def test_module():
    from datetime import date
    
    # Create test data
    students = [
        Student(1, "John Doe", 917),
        Student(2, "Jane Smith", 917),
        Student(3, "Bob Wilson", 918)
    ]
    
    problems = [
        Problem(7, 1, "Sort array", date(2024, 12, 15)),
        Problem(7, 2, "Search algorithm", date(2024, 12, 20))
    ]
    
    assignments = [
        Assignment(1, 1, "7_1", 9.5),
        Assignment(2, 1, "7_2", 8.0),
        Assignment(3, 2, "7_1", 9.0),
        Assignment(4, 3, "7_1", 7.5),
        Assignment(5, 3, "7_2", None)  # Ungraded
    ]
    
    # Test statistics calculator
    calc = StatisticsCalculator(students, problems, assignments)
    
    # Test student statistics
    student_stats = calc.calculate_student_statistics()
    assert len(student_stats) == 3
    
    # John should have average of 8.75
    john_stats = next(s for s in student_stats if s.student_id == 1)
    assert john_stats.total_assignments == 2
    assert john_stats.graded_assignments == 2
    assert abs((john_stats.average_grade or 0) - 8.75) < 0.01
    
    # Test problem statistics
    problem_stats = calc.calculate_problem_statistics()
    assert len(problem_stats) == 2
    
    # Problem 7_1 should have 100% completion rate
    prob_7_1 = next(s for s in problem_stats if s.problem_id == "7_1")
    assert prob_7_1.total_assignments == 3
    assert prob_7_1.graded_assignments == 3
    assert prob_7_1.completion_rate == 100.0
    
    # Test group report
    group_917_report = calc.generate_group_report(917)
    assert group_917_report.total_students == 2
    assert group_917_report.students_with_assignments == 2
    
    # Test empty group
    empty_group = calc.generate_group_report(999)
    assert empty_group.total_students == 0