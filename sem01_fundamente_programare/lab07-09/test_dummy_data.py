#!/usr/bin/env python3
"""
Test script to load the dummy data and display raport
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from persistence.data_manager import DataManager
from stats.statistics_calculator import StatisticsCalculator

def test_dummy_data():
    print("=== Loading Dummy Data ===\n")
    
    # Load data from data/ directory
    data_manager = DataManager("data")
    
    try:
        # Load all data
        students, problems, assignments = data_manager.load_all_data()
        print(f"Loaded {len(students)} students")
        print(f"Loaded {len(problems)} problems")
        print(f"Loaded {len(assignments)} assignments")
        
        print("\n=== Sample Data ===")
        print("Top 5 Students:")
        for i, student in enumerate(students[:5]):
            print(f"  {student.get_id()}. {student.get_name()} (Group {student.get_group()})")
            
        print("\nSample Problems:")
        for i, problem in enumerate(problems[:5]):
            print(f"  {problem.get_lab_number()}_{problem.get_problem_number()}: {problem.get_description()}")
            
        print(f"\nSample Assignments (showing first 10 of {len(assignments)}):")
        for i, assignment in enumerate(assignments[:10]):
            grade_str = f"{assignment.get_grade()}" if assignment.has_grade() else "Not graded"
            print(f"  ID {assignment.get_assignment_id()}: Student {assignment.get_student_id()} -> Problem {assignment.get_problem_id()} (Grade: {grade_str})")
        
        # Test statistics and raport
        print("\n=== Testing Raport Functionality ===")
        calc = StatisticsCalculator(students, problems, assignments)
        
        print("\nTop 5 Students by Average Grade:")
        top_students = calc.get_top_students(5)
        for i, student_stat in enumerate(top_students, 1):
            avg_str = f"{student_stat.average_grade:.2f}" if student_stat.average_grade is not None else "N/A"
            print(f"  {i}. {student_stat.student_name} (Group {student_stat.group}) - Avg: {avg_str}")
        
        print("\nTop 5 Most Popular Problems:")
        top_problems = calc.get_top_problems(5)
        for i, problem_stat in enumerate(top_problems, 1):
            print(f"  {i}. {problem_stat.problem_id}: {problem_stat.description} - {problem_stat.total_assignments} assignments")
        
        print("\n=== 3x3 Matrix Raport ===")
        report = calc.generate_top_report(3)
        
        # Print matrix header
        header = f"{'Student':<15}"
        for problem_stat in report['top_problems']:
            header += f"{problem_stat.problem_id:<12}"
        print(header)
        print("-" * (15 + 12 * len(report['top_problems'])))
        
        # Print matrix data  
        for student_row in report['matrix_data']:
            line = f"{student_row['student_name']:<15}"
            for problem_stat in report['top_problems']:
                problem_id = problem_stat.problem_id
                problem_data = student_row['problem_data'][problem_id]
                
                if problem_data['status'] == "Not assigned":
                    cell = "N/A"
                elif problem_data['status'] == "Assigned":
                    cell = "Ungraded"
                else:
                    grade = problem_data['grade']
                    if isinstance(grade, (int, float)):
                        cell = f"{grade:.1f}"
                    else:
                        cell = str(grade)
                
                line += f"{cell:<12}"
            print(line)
        
        print(f"\n✅ Success! Dummy data loaded and raport generated successfully!")
        print(f"📊 Total: {len(students)} students, {len(problems)} problems, {len(assignments)} assignments")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dummy_data()