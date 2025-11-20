import os
import shlex
from datetime import datetime, date
from services.problem import ProblemService
from services.student import StudentService
from services.assignment import AssignmentService

class CLI:
    def __init__(self):
        self._problem_service = ProblemService()
        self._student_service = StudentService()
        self._assignment_service = AssignmentService()
        
        # Share repositories between services for data consistency
        self._assignment_service.set_student_repo(self._student_service._student_repo)
        self._assignment_service.set_problem_repo(self._problem_service._problem_repo)
        
        self.running = True

        self.commands = {
            "add_student": self._handle_add_student,
            "remove_student": self._handle_remove_student,
            "list_students": self._handle_list_students,
            "search_student": self._handle_search_student,
            "add_problem": self._handle_add_problem,
            "remove_problem": self._handle_remove_problem,
            "list_problems": self._handle_list_problems,
            "search_problem": self._handle_search_problem,
            
            # Assignment operations
            "create_assignment": self._handle_create_assignment,
            "grade_assignment": self._handle_grade_assignment,
            "list_assignments": self._handle_list_assignments,

            # Helpers
            'help': self._handle_help,
            'exit': self._handle_exit,
            'quit': self._handle_exit,
            'clear': self._handle_clear,
        }


    def run(self):

        while self.running:
            try:
                user_input = input("StudentAssignmentsCLI >>> ").strip()
                if user_input:
                    self._process_command(user_input)
            except KeyboardInterrupt:
                print("\nSee you later!")
                break
            except EOFError:
                print("\nSee you later!")
                break


    def _process_command(self, user_input:str):
        """Process a single command"""
        try:
            # Parse command and arguments
            parts = shlex.split(user_input)
            if not parts:
                return
                
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Execute command
            if command in self.commands:
                self.commands[command](args)
            else:
                print(f"Unknown command: '{command}'. Type 'help' for a full list of commands.")
                
        except ValueError as e:
            print(f"Parsing error: {e}")
        except Exception as e:
            print(f"Execution error: {e}")

    def _handle_help(self, args):
        """Handle help command"""
        print("""
AVAILABLE COMMANDS:

Student related operations:
  add_student <name> <group>                - Add a new student in the database
  remove_student <student_id>               - Remove a student by ID
  list_students                             - List all students
  search_student <search_type> <search_term> - Search students by name, id, or group
                                              Examples: search_student name "John"
                                                       search_student id 123
                                                       search_student group 917

Problem related operations:
  add_problem <lab_problem> <description> <deadline>    - Add a new problem
                                                        Format: lab_problem as '7_1', deadline as 'YYYY-MM-DD'
  remove_problem <lab_problem>                          - Remove a problem by lab_problem format
  list_problems                                         - List all problems
  search_problem <lab_problem_id>                       - Search problem by ID (format: '7_1')

Assignment operations:
  create_assignment <student_id> <problem_id>           - Assign a problem to a student
                                                        Format: problem_id as '7_1'
  grade_assignment <assignment_id> <grade>              - Grade an assignment (0-10)
  list_assignments                                      - List all assignments

Random generation:
  generate_student                                      - Generate and add a random student
  generate_problem                                      - Generate and add a random problem

Others:
  clear                                   - Clear the screen
  help                                    - Show this message
  exit, quit                              - Exit the application
""")  

    def _handle_clear(self, args):
        """Handle clear command"""
        os.system('cls' if os.name == 'nt' else 'clear')


    def _handle_exit(self, args):
        """Handle exit command"""
        print("La revedere!")
        self.running = False

    def _handle_add_student(self, args):
        """Handle add_student command"""
        if len(args) != 2:
            print("Usage: add_student <name> <group>")
            return
        
        try:
            name = args[0]
            group = int(args[1])
            student = self._student_service.add_student(name, group)
            print(f"Student added successfully: ID {student.id}, Name: {name}, Group: {group}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_remove_student(self, args):
        """Handle remove_student command"""
        if len(args) != 1:
            print("Usage: remove_student <student_id>")
            return
        
        try:
            student_id = int(args[0])
            self._student_service.remove_student(student_id)
            print(f"Student with ID {student_id} removed successfully")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_students(self, args):
        """Handle list_students command"""
        students = self._student_service.list_students()
        
        if not students:
            print("No students found.")
            return
        
        print("STUDENTS:")
        print("-" * 50)
        print(f"{'ID':<5} {'Name':<20} {'Group':<10}")
        print("-" * 50)
        
        for student in students:
            print(f"{student.get_id():<5} {student.get_name():<20} {student.get_group():<10}")

    def _handle_add_problem(self, args):
        """Handle add_problem command"""
        if len(args) < 3:
            print("Usage: add_problem <lab_problem> <description> <deadline_YYYY-MM-DD>")
            print("Example: add_problem 7_1 'Sort array problem' 2024-12-15")
            return
        
        try:
            lab_problem = args[0]
            if '_' not in lab_problem:
                print("Error: lab_problem must be in format <labnumber>_<problemnumber>")
                return
            
            lab_number, problem_number = lab_problem.split('_', 1)
            lab_number = int(lab_number)
            problem_number = int(problem_number)
            
            description = args[1]
            deadline_str = args[2]
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()
            
            problem = self._problem_service.add_problem(lab_number, problem_number, description, deadline)
            print(f"Problem added successfully: Lab {lab_number}, Problem {problem_number}, Deadline: {deadline}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_remove_problem(self, args):
        """Handle remove_problem command"""
        if len(args) != 1:
            print("Usage: remove_problem <lab_problem>")
            print("Example: remove_problem 7_1")
            return
        
        try:
            lab_problem = args[0]
            if '_' not in lab_problem:
                print("Error: lab_problem must be in format <labnumber>_<problemnumber>")
                return
            
            lab_number, problem_number = lab_problem.split('_', 1)
            lab_number = int(lab_number)
            problem_number = int(problem_number)
            
            self._problem_service.remove_problem(lab_number, problem_number)
            print(f"Problem {lab_number}_{problem_number} removed successfully")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_problems(self, args):
        """Handle list_problems command"""
        problems = self._problem_service.list_problems()
        
        if not problems:
            print("No problems found.")
            return
        
        print("PROBLEMS:")
        print("-" * 80)
        print(f"{'Lab':<5} {'Problem':<8} {'Description':<30} {'Deadline':<15}")
        print("-" * 80)
        
        for problem in problems:
            print(f"{problem.get_lab_number():<5} {problem.get_problem_number():<8} {problem.get_description():<30} {problem.get_deadline():<15}")

    def _handle_search_student(self, args):
        """Handle search_student command"""
        if len(args) != 2:
            print("Usage: search_student <search_type> <search_term>")
            print("Search types: name, id, group")
            print("Examples:")
            print("  search_student name John")
            print("  search_student id 123")
            print("  search_student group 917")
            return
        
        try:
            search_type = args[0].lower()
            search_term = args[1]
            
            if search_type not in ['name', 'id', 'group']:
                print("Error: search_type must be 'name', 'id', or 'group'")
                return
            
            results = self._student_service.search_students(search_term, search_type)
            
            if not results:
                print(f"No students found with {search_type} '{search_term}'")
                return
            
            print(f"STUDENTS MATCHING {search_type.upper()}: '{search_term}'")
            print("-" * 50)
            print(f"{'ID':<5} {'Name':<20} {'Group':<10}")
            print("-" * 50)
            
            for student in results:
                print(f"{student.get_id():<5} {student.get_name():<20} {student.get_group():<10}")
                
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_search_problem(self, args):
        """Handle search_problem command"""
        if len(args) != 1:
            print("Usage: search_problem <lab_problem_id>")
            print("Format: lab_problem_id as 'lab_problem' (e.g., '7_1')")
            print("Example: search_problem 7_1")
            return
        
        try:
            lab_problem_id = args[0]
            
            if '_' not in lab_problem_id:
                print("Error: lab_problem_id must be in format <labnumber>_<problemnumber>")
                return
            
            results = self._problem_service.search_problems_by_id(lab_problem_id)
            
            if not results:
                print(f"No problem found with ID '{lab_problem_id}'")
                return
            
            print(f"PROBLEM MATCHING ID: '{lab_problem_id}'")
            print("-" * 80)
            print(f"{'Lab':<5} {'Problem':<8} {'Description':<30} {'Deadline':<15}")
            print("-" * 80)
            
            for problem in results:
                print(f"{problem.get_lab_number():<5} {problem.get_problem_number():<8} {problem.get_description():<30} {problem.get_deadline():<15}")
                
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_create_assignment(self, args):
        """Handle create_assignment command"""
        if len(args) != 2:
            print("Usage: create_assignment <student_id> <problem_id>")
            print("Example: create_assignment 1 7_1")
            return
        
        try:
            student_id = int(args[0])
            problem_id = args[1]
            
            if '_' not in problem_id:
                print("Error: problem_id must be in format <labnumber>_<problemnumber>")
                return
            
            assignment = self._assignment_service.create_assignment(student_id, problem_id)
            student_name = self._assignment_service.get_student_name(student_id)
            problem_desc = self._assignment_service.get_problem_description(problem_id)
            
            print(f"Assignment created: Student {student_name} (ID: {student_id}) assigned to Problem {problem_id} ({problem_desc})")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_grade_assignment(self, args):
        """Handle grade_assignment command"""
        if len(args) != 2:
            print("Usage: grade_assignment <assignment_id> <grade>")
            print("Example: grade_assignment 1 9.5")
            print("Grade must be between 0 and 10")
            return
        
        try:
            assignment_id = int(args[0])
            grade = float(args[1])
            
            # Get assignment info for confirmation message
            assignment = self._assignment_service.get_assignment_by_id(assignment_id)
            if assignment is None:
                print(f"Error: Assignment with ID {assignment_id} not found")
                return
            
            student_name = self._assignment_service.get_student_name(assignment.get_student_id())
            problem_desc = self._assignment_service.get_problem_description(assignment.get_problem_id())
            
            self._assignment_service.grade_assignment(assignment_id, grade)
            print(f"Assignment graded: Student {student_name} - Problem {assignment.get_problem_id()} ({problem_desc}) - Grade: {grade}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_assignments(self, args):
        """Handle list_assignments command"""
        assignments = self._assignment_service.list_assignments()
        
        if not assignments:
            print("No assignments found.")
            return
        
        print("ASSIGNMENTS:")
        print("-" * 90)
        print(f"{'ID':<5} {'Student':<20} {'Problem':<10} {'Description':<25} {'Grade':<10}")
        print("-" * 90)
        
        for assignment in assignments:
            student_name = self._assignment_service.get_student_name(assignment.get_student_id())
            problem_desc = self._assignment_service.get_problem_description(assignment.get_problem_id())
            grade_str = str(assignment.get_grade()) if assignment.has_grade() else "Not graded"
            
            print(f"{assignment.get_assignment_id():<5} {student_name:<20} {assignment.get_problem_id():<10} {problem_desc[:25]:<25} {grade_str:<10}")