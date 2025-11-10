import os
import shlex
from datetime import datetime, date
from problem.repository import ProblemRepository
from student.repository import StudentRepository

class CLI:
    def __init__(self, problem_repo: ProblemRepository, student_repo: StudentRepository):
        self._problem_repo = problem_repo
        self._student_repo = student_repo
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
            student = self._student_repo.add_student(name, group)
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
            self._student_repo.remove_student(student_id)
            print(f"Student with ID {student_id} removed successfully")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_students(self, args):
        """Handle list_students command"""
        students = self._student_repo.list_students()
        
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
            
            problem = self._problem_repo.add_problem(lab_number, problem_number, description, deadline)
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
            
            self._problem_repo.remove_problem(lab_number, problem_number)
            print(f"Problem {lab_number}_{problem_number} removed successfully")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_problems(self, args):
        """Handle list_problems command"""
        problems = self._problem_repo.list_problems()
        
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
            
            results = self._student_repo.search_students(search_term, search_type)
            
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
            
            results = self._problem_repo.search_problems_by_id(lab_problem_id)
            
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