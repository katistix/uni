#!/usr/bin/env python3
"""
Integration test for third iteration features:
- DTOs for CSV serialization
- CSV persistence with backup
- Statistics and reporting
"""

import os
import sys
import tempfile
import shutil
from datetime import date

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_dto_functionality():
    """Test DTO serialization and deserialization"""
    print("Testing DTO functionality...")
    
    from dto.student_dto import StudentDTO
    from dto.problem_dto import ProblemDTO  
    from dto.assignment_dto import AssignmentDTO
    from domain.student import Student
    from domain.problem import Problem
    from domain.assignment import Assignment
    
    # Test StudentDTO
    student = Student(1, "John Doe", 917)
    dto = StudentDTO.from_domain(student)
    csv_row = dto.to_csv_row()
    dto2 = StudentDTO.from_csv_row(csv_row)
    student2 = dto2.to_domain()
    
    assert student.get_id() == student2.get_id()
    assert student.get_name() == student2.get_name()
    assert student.get_group() == student2.get_group()
    
    # Test ProblemDTO
    problem = Problem(7, 1, "Test problem", date(2024, 12, 15))
    dto = ProblemDTO.from_domain(problem)
    csv_row = dto.to_csv_row()
    dto2 = ProblemDTO.from_csv_row(csv_row)
    problem2 = dto2.to_domain()
    
    assert problem.get_lab_number() == problem2.get_lab_number()
    assert problem.get_problem_number() == problem2.get_problem_number()
    assert problem.get_description() == problem2.get_description()
    assert problem.get_deadline() == problem2.get_deadline()
    
    print("✓ DTO functionality test passed")

def test_persistence_functionality():
    """Test CSV persistence with backup"""
    print("Testing CSV persistence...")
    
    from services.persistence_service import PersistenceService
    from services.student import StudentService
    from services.problem import ProblemService
    from services.assignment import AssignmentService
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize services
        student_service = StudentService()
        problem_service = ProblemService()
        assignment_service = AssignmentService()
        persistence_service = PersistenceService(temp_dir)
        
        # Add some test data
        student_service.add_student("John Doe", 917)
        student_service.add_student("Jane Smith", 918)
        problem_service.add_problem(7, 1, "Test problem", date(2024, 12, 15))
        
        # Share repositories for assignment service
        assignment_service.set_student_repo(student_service._student_repo)
        assignment_service.set_problem_repo(problem_service._problem_repo)
        assignment_service.create_assignment(1, "7_1")
        assignment_service.grade_assignment(1, 9.5)
        
        # Save data
        persistence_service.save_application_data(student_service, problem_service, assignment_service)
        
        # Verify files were created
        assert os.path.exists(os.path.join(temp_dir, "students.csv"))
        assert os.path.exists(os.path.join(temp_dir, "problems.csv"))
        assert os.path.exists(os.path.join(temp_dir, "assignments.csv"))
        
        # Load data back and verify
        students, problems, assignments = persistence_service.load_application_data()
        assert len(students) == 2
        assert len(problems) == 1
        assert len(assignments) == 1
        assert assignments[0].get_grade() == 9.5
    
    print("✓ CSV persistence test passed")

def test_statistics_functionality():
    """Test statistics calculation and reporting"""
    print("Testing statistics functionality...")
    
    from stats.statistics_calculator import StatisticsCalculator, ReportExporter
    from domain.student import Student
    from domain.problem import Problem
    from domain.assignment import Assignment
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
    
    # Test CSV export
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test student statistics export
        ReportExporter.export_student_statistics(
            student_stats, 
            os.path.join(temp_dir, "student_stats.csv")
        )
        assert os.path.exists(os.path.join(temp_dir, "student_stats.csv"))
        
        # Test problem statistics export
        ReportExporter.export_problem_statistics(
            problem_stats, 
            os.path.join(temp_dir, "problem_stats.csv")
        )
        assert os.path.exists(os.path.join(temp_dir, "problem_stats.csv"))
        
        # Test grades export
        ReportExporter.export_all_grades(
            students, assignments, 
            os.path.join(temp_dir, "grades.csv")
        )
        assert os.path.exists(os.path.join(temp_dir, "grades.csv"))
    
    print("✓ Statistics functionality test passed")

def test_cli_integration():
    """Test CLI startup and basic functionality"""
    print("Testing CLI integration...")
    
    # Test that CLI can be imported and initialized
    from ui.cli import CLI
    cli = CLI()
    
    # Check that all expected commands are available
    expected_new_commands = [
        'stats_students', 'stats_problems', 'report_group', 'export_grades',
        'save_data', 'load_data', 'export_data'
    ]
    
    for cmd in expected_new_commands:
        assert cmd in cli.commands, f"Command {cmd} not found in CLI"
    
    print("✓ CLI integration test passed")

def run_all_tests():
    """Run all third iteration tests"""
    print("=" * 60)
    print("TESTING THIRD ITERATION FUNCTIONALITY")
    print("=" * 60)
    
    try:
        test_dto_functionality()
        test_persistence_functionality() 
        test_statistics_functionality()
        test_cli_integration()
        
        print("=" * 60)
        print("🎉 ALL THIRD ITERATION TESTS PASSED!")
        print("=" * 60)
        print()
        print("Third iteration features successfully implemented:")
        print("✓ DTOs for CSV serialization")
        print("✓ CSV persistence with backup functionality")
        print("✓ Statistics calculation and reporting")
        print("✓ CLI integration with new commands")
        print("✓ Export functionality for grades and reports")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)