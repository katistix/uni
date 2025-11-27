#!/usr/bin/env python3
"""
Demo script showing the new raport functionality
"""

from datetime import date
from domain.student import Student  
from domain.problem import Problem
from domain.assignment import Assignment
from stats.statistics_calculator import StatisticsCalculator

def demo_raport_functionality():
    print("=== DEMO: Raport Functionality ===\n")
    
    # Create sample data
    students = [
        Student(1, 'Alice Johnson', 917),
        Student(2, 'Bob Smith', 917), 
        Student(3, 'Carol Wilson', 918),
        Student(4, 'David Brown', 918),
        Student(5, 'Eva Martinez', 919)
    ]

    problems = [
        Problem(7, 1, 'Array Sorting', date(2024, 12, 15)),
        Problem(7, 2, 'Binary Search', date(2024, 12, 20)),
        Problem(8, 1, 'Hash Tables', date(2024, 12, 25)),
        Problem(8, 2, 'Graph Algorithms', date(2024, 12, 30)),
        Problem(9, 1, 'Dynamic Programming', date(2025, 1, 5))
    ]

    assignments = [
        # Alice - top student
        Assignment(1, 1, '7_1', 9.5),
        Assignment(2, 1, '7_2', 9.0), 
        Assignment(3, 1, '8_1', 9.5),
        Assignment(4, 1, '8_2', 9.0),
        
        # Bob - good student  
        Assignment(5, 2, '7_1', 8.5),
        Assignment(6, 2, '7_2', 8.0),
        Assignment(7, 2, '8_1', 8.5),
        
        # Carol - average student
        Assignment(8, 3, '7_1', 7.5),
        Assignment(9, 3, '7_2', 7.0),
        Assignment(10, 3, '8_1', 8.0),
        Assignment(11, 3, '9_1', 7.5),
        
        # David - struggling student
        Assignment(12, 4, '7_1', 6.0),
        Assignment(13, 4, '7_2', 6.5),
        
        # Eva - new student, few assignments
        Assignment(14, 5, '7_1', 8.0),
    ]

    # Create calculator
    calc = StatisticsCalculator(students, problems, assignments)
    
    print("1. Top 3 Students:")
    top_students = calc.get_top_students(3)
    for i, student in enumerate(top_students, 1):
        avg_str = f"{student.average_grade:.2f}" if student.average_grade is not None else "N/A"
        print(f"   {i}. {student.student_name} (Group {student.group}) - Avg: {avg_str}")
    
    print("\n2. Top 3 Problems (by number of assignments):")
    top_problems = calc.get_top_problems(3)
    for i, problem in enumerate(top_problems, 1):
        print(f"   {i}. {problem.problem_id}: {problem.description} - {problem.total_assignments} assignments")
    
    print("\n3. 3x3 Matrix Report:")
    report = calc.generate_top_report(3)
    
    print("=" * 80)
    # Print header
    header = f"{'Student':<20}"
    for problem_stat in report['top_problems']:
        header += f"{problem_stat.problem_id:<15}"
    print(header)
    print("-" * 80)
    
    # Print matrix data
    for student_row in report['matrix_data']:
        line = f"{student_row['student_name'][:19]:<20}"
        for problem_stat in report['top_problems']:
            problem_id = problem_stat.problem_id
            problem_data = student_row['problem_data'][problem_id]
            
            if problem_data['status'] == "Not assigned":
                cell = "Not assigned"
            elif problem_data['status'] == "Assigned":
                cell = "Ungraded"
            else:
                grade = problem_data['grade']
                if isinstance(grade, (int, float)):
                    cell = f"{grade:.1f}"
                else:
                    cell = str(grade)
            
            line += f"{cell:<15}"
        print(line)
    
    print("\n=== CLI Usage ===")
    print("You can now use the following command in the CLI:")
    print("  raport 3        # Generate 3x3 report")
    print("  raport 5        # Generate 5x5 report")
    print("  raport          # Generate 3x3 report (default)")

if __name__ == "__main__":
    demo_raport_functionality()