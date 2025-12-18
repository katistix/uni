"""
Demonstrație funcții recursive și analiza complexității

1. Funcție analizată pentru complexitate: search_students() - O(n)
2. Funcții implementate recursiv:
   - search_students_recursive() - O(n) timp, O(n) spațiu
   - calculate_total_assignments_recursive() - O(n) timp, O(n) spațiu
   - find_problems_by_lab_recursive() - O(n) timp, O(n) spațiu
"""

from services.student import StudentService
from services.problem import ProblemService
from services.assignment import AssignmentService
from domain.student import Student
from domain.problem import Problem
from domain.assignment import Assignment
from datetime import date

def demo_recursive_functions():
    """Demonstrează funcționarea funcțiilor recursive implementate"""
    
    # Setup services
    student_service = StudentService()
    problem_service = ProblemService()
    assignment_service = AssignmentService()
    
    # Add test data
    print("=== Adding test data ===")
    
    # Add students
    student1 = student_service.add_student("Ana Popescu", 917)
    student2 = student_service.add_student("Ion Ionescu", 918)
    student3 = student_service.add_student("Maria Georgescu", 917)
    
    # Add problems
    problem1 = problem_service.add_problem(1, 1, "Suma numerelor", date(2024, 1, 15))
    problem2 = problem_service.add_problem(1, 2, "Numere pare", date(2024, 1, 15))
    problem3 = problem_service.add_problem(2, 1, "Fibonacci recursiv", date(2024, 1, 22))
    
    # Sync repositories for assignment service
    assignment_service.set_student_repo(student_service._student_repo)
    assignment_service.set_problem_repo(problem_service._problem_repo)
    
    # Add assignments
    assignments = []
    assignments.append(assignment_service.create_assignment(student1.get_id(), "1_1"))
    assignments.append(assignment_service.create_assignment(student1.get_id(), "1_2"))
    assignments.append(assignment_service.create_assignment(student2.get_id(), "1_1"))
    assignments.append(assignment_service.create_assignment(student3.get_id(), "2_1"))
    
    print(f"Added {len(student_service.list_students())} students")
    print(f"Added {len(problem_service.list_problems())} problems")
    print(f"Added {len(assignments)} assignments")
    
    print("\n=== Demonstrare funcții recursive ===")
    
    # 1. Recursive search demo
    print("\n1. Search students recursive (caută grupa 917):")
    recursive_results = student_service.search_students_recursive("917", "group")
    print(f"Găsiți {len(recursive_results)} studenți în grupa 917:")
    for student in recursive_results:
        print(f"  - {student.get_name()} (ID: {student.get_id()})")
    
    # 2. Recursive assignment counting demo
    print(f"\n2. Calculate assignments recursive pentru studentul {student1.get_name()}:")
    total_assignments = student_service.calculate_total_assignments_recursive(assignments, student1.get_id())
    print(f"  Total assignments: {total_assignments}")
    
    # 3. Recursive problem finding by lab demo
    print("\n3. Find problems by lab recursive (lab 1):")
    lab1_problems = problem_service.find_problems_by_lab_recursive(1)
    print(f"Găsite {len(lab1_problems)} probleme în lab 1:")
    for problem in lab1_problems:
        print(f"  - {problem.get_lab_number()}_{problem.get_problem_number()}: {problem.get_description()}")

def analyze_complexity():
    """Analiză detaliată a complexității"""
    print("\n=== ANALIZĂ COMPLEXITATE ===")
    print("\n1. Funcție analizată: search_students() din repos/student.py")
    print("   - Complexitate timp: O(n), unde n = numărul de studenți")
    print("   - Complexitate spațiu: O(k), unde k = numărul de rezultate")
    print("   - Explicație: Parcurge toată lista de studenți pentru căutare")
    
    print("\n2. Funcții implementate recursiv:")
    
    print("\n   a) search_students_recursive():")
    print("      - Complexitate timp: O(n)")
    print("      - Complexitate spațiu: O(n) datorită stack-ului de apeluri")
    print("      - Fiecare apel recursiv adaugă un frame pe stack")
    
    print("\n   b) calculate_total_assignments_recursive():")
    print("      - Complexitate timp: O(n), unde n = numărul de assignments")
    print("      - Complexitate spațiu: O(n) datorită stack-ului recursiv")
    print("      - Parcurge recursiv toate assignment-urile")
    
    print("\n   c) find_problems_by_lab_recursive():")
    print("      - Complexitate timp: O(n), unde n = numărul de probleme")
    print("      - Complexitate spațiu: O(n) datorită stack-ului recursiv")
    print("      - Construiește recursiv lista de rezultate")

if __name__ == "__main__":
    demo_recursive_functions()
    analyze_complexity()