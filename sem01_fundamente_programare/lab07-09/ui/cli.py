import os
import shlex
from datetime import datetime, date
from services.problem import ProblemService
from services.student import StudentService
from services.assignment import AssignmentService
from services.persistence_service import PersistenceService
from repos.student import StudentRepository
from repos.problem import ProblemRepository
from repos.assignment import AssignmentRepository

class CLI:
    def __init__(self):
        self._problem_service = ProblemService()
        self._student_service = StudentService()
        self._assignment_service = AssignmentService()
        
        # Initialize persistence service
        self._persistence_service = None
        try:
            import sys
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            sys.path.insert(0, parent_dir)
            
            from services.persistence_service import PersistenceService
            self._persistence_service = PersistenceService()
            print("Persistence service initialized successfully.")
        except Exception as e:
            print(f"Warning: Could not initialize persistence service: {e}")
        
        # Share repositories between services for data consistency
        self._assignment_service.set_student_repo(self._student_service._student_repo)
        self._assignment_service.set_problem_repo(self._problem_service._problem_repo)
        
        self.running = True

        self.commands = {
            # Basic CRUD operations
            "add_student": self._handle_add_student,
            "list_students": self._handle_list_students,
            "add_problem": self._handle_add_problem,
            "list_problems": self._handle_list_problems,
            "create_assignment": self._handle_create_assignment,
            "grade_assignment": self._handle_grade_assignment,
            "list_assignments": self._handle_list_assignments,
            
            # Reports
            "raport": self._handle_raport,
            
            # Data persistence
            "save_data": self._handle_save_data,
            "load_data": self._handle_load_data,
            
            # Helpers
            'help': self._handle_help,
            'exit': self._handle_exit,
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

    def _process_command(self, user_input: str):
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

Students:
  add_student <name> <group>        - Add a new student
  list_students                     - List all students

Problems:
  add_problem <lab_problem> <description> <deadline>  - Add a new problem
                                                      Format: lab_problem as '7_1', deadline as 'YYYY-MM-DD'
  list_problems                     - List all problems

Assignments:
  create_assignment <student_id> <problem_id>  - Assign a problem to a student
  grade_assignment <assignment_id> <grade>     - Grade an assignment (0-10)
  list_assignments                             - List all assignments

Reports:
  raport [k]                        - Generate k*k matrix report (default: 3)

Data:
  save_data                         - Save all data to CSV files
  load_data                         - Load data from CSV files

Other:
  help                              - Show this message
  clear                             - Clear screen
  exit                              - Exit application
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

    def _handle_list_students(self, args):
        """Handle list_students command"""
        try:
            students = self._student_service.list_students()
            if not students:
                print("No students found.")
                return
            
            print("STUDENTS:")
            print("-" * 50)
            print(f"{'ID':<5} {'Name':<20} {'Group':<8}")
            print("-" * 50)
            for student in students:
                print(f"{student.get_id():<5} {student.get_name():<20} {student.get_group():<8}")
                
        except Exception as e:
            print(f"Error listing students: {e}")

    def _handle_add_problem(self, args):
        """Handle add_problem command"""
        if len(args) != 3:
            print("Usage: add_problem <lab_problem> <description> <deadline>")
            print("Example: add_problem 7_1 'Sort array problem' 2024-12-15")
            return
        
        try:
            lab_problem = args[0]
            description = args[1]
            deadline_str = args[2]
            
            # Parse lab_problem format (e.g., "7_1")
            parts = lab_problem.split('_')
            if len(parts) != 2:
                print("Lab problem format should be 'lab_problem' (e.g., '7_1')")
                return
            
            lab_number = int(parts[0])
            problem_number = int(parts[1])
            
            # Parse deadline
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            
            problem = self._problem_service.add_problem(lab_number, problem_number, description, deadline)
            print(f"Problem added successfully: {lab_number}_{problem_number} - {description}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_problems(self, args):
        """Handle list_problems command"""
        try:
            problems = self._problem_service.list_problems()
            if not problems:
                print("No problems found.")
                return
            
            print("PROBLEMS:")
            print("-" * 80)
            print(f"{'Lab':<5} {'Problem':<8} {'Description':<30} {'Deadline':<15}")
            print("-" * 80)
            for problem in problems:
                deadline_str = problem.get_deadline().strftime("%Y-%m-%d") if problem.get_deadline() else "N/A"
                print(f"{problem.get_lab_number():<5} {problem.get_problem_number():<8} {problem.get_description():<30} {deadline_str:<15}")
                
        except Exception as e:
            print(f"Error listing problems: {e}")

    def _handle_create_assignment(self, args):
        """Handle create_assignment command"""
        if len(args) != 2:
            print("Usage: create_assignment <student_id> <problem_id>")
            print("Example: create_assignment 1 7_1")
            return
        
        try:
            student_id = int(args[0])
            problem_id = args[1]
            
            assignment = self._assignment_service.assign_problem(student_id, problem_id)
            print(f"Assignment created successfully: ID {assignment.get_assignment_id()}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_grade_assignment(self, args):
        """Handle grade_assignment command"""
        if len(args) != 2:
            print("Usage: grade_assignment <assignment_id> <grade>")
            print("Grade should be between 0 and 10")
            return
        
        try:
            assignment_id = int(args[0])
            grade = float(args[1])
            
            if not (0 <= grade <= 10):
                print("Grade must be between 0 and 10")
                return
            
            self._assignment_service.grade_assignment(assignment_id, grade)
            print(f"Assignment {assignment_id} graded successfully with grade {grade}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _handle_list_assignments(self, args):
        """Handle list_assignments command"""
        try:
            assignments = self._assignment_service.list_assignments()
            if not assignments:
                print("No assignments found.")
                return
            
            print("ASSIGNMENTS:")
            print("-" * 90)
            print(f"{'ID':<5} {'Student':<20} {'Problem':<10} {'Description':<25} {'Grade':<10}")
            print("-" * 90)
            
            for assignment in assignments:
                # Get student name
                try:
                    student = self._student_service._student_repo.find_student_by_id(assignment.get_student_id())
                    student_name = student.get_name() if student else f"ID {assignment.get_student_id()}"
                except:
                    student_name = f"ID {assignment.get_student_id()}"
                
                # Get problem description
                try:
                    problem_id = assignment.get_problem_id()
                    parts = problem_id.split('_')
                    lab_num, prob_num = int(parts[0]), int(parts[1])
                    problem = self._problem_service._problem_repo.find_problem(lab_num, prob_num)
                    description = problem.get_description()[:24] if problem else "Unknown"
                except:
                    description = "Unknown"
                
                grade_str = f"{assignment.get_grade()}" if assignment.has_grade() else "Not graded"
                
                print(f"{assignment.get_assignment_id():<5} {student_name:<20} {assignment.get_problem_id():<10} {description:<25} {grade_str:<10}")
                
        except Exception as e:
            print(f"Error listing assignments: {e}")

    def _handle_raport(self, args):
        try:
            k = 3  # default
            if args and len(args) > 0:
                k = int(args[0])
            
            assignments = self._assignment_service.list_assignments()
            top_students = self._student_service.get_top_students(assignments, k)
            top_problems = self._problem_service.get_top_problems(assignments, k)
            
            if not top_students or not top_problems:
                print("Not enough data for generating report.")
                return
                
            print(f"TOP {k} STUDENTS vs TOP {k} PROBLEMS REPORT:")
            print("=" * (20 + k * 15))
            
            # Print header with problem IDs
            header = f"{'Student':<20}"
            for problem_stat in top_problems:
                header += f"{problem_stat.get_problem_id():<15}"
            print(header)
            print("-" * (20 + k * 15))
            
            # Generate and print matrix data
            for student_stat in top_students:
                student_id = student_stat.get_student_id()
                student_name = student_stat.get_student_name()
                line = f"{student_name[:19]:<20}"
                
                for problem_stat in top_problems:
                    problem_id = problem_stat.get_problem_id()
                    
                    # Find assignment for this student and problem
                    assignment = None
                    for a in assignments:
                        if a.get_student_id() == student_id and a.get_problem_id() == problem_id:
                            assignment = a
                            break
                    
                    if assignment is None:
                        cell = "Not assigned"
                    elif assignment.has_grade():
                        grade = assignment.get_grade()
                        cell = f"{grade:.1f}"
                    else:
                        cell = "Ungraded"
                    
                    line += f"{cell:<15}"
                print(line)
            
            # Print summary statistics
            print("\n" + "=" * 60)
            print("SUMMARY:")
            print(f"Top {k} Students (by average grade):")
            for i, student in enumerate(top_students, 1):
                avg_grade = student.get_average_grade()
                avg_str = f"{avg_grade:.2f}" if avg_grade is not None else "N/A"
                print(f"  {i}. {student.get_student_name()} (Group {student.get_group()}) - {avg_str}")
                
            print(f"\nTop {k} Problems (by number of assignments):")
            for i, problem in enumerate(top_problems, 1):
                print(f"  {i}. {problem.get_problem_id()}: {problem.get_description()[:40]} - {problem.get_total_assignments()} assignments")
                
        except ValueError:
            print("Error: k must be a valid number")
        except Exception as e:
            print(f"Error generating report: {e}")

    def _handle_save_data(self, args):
        """Handle save_data command"""
        if self._persistence_service is None:
            print("Error: Persistence service not available")
            return
        
        try:
            self._persistence_service.save_application_data(
                self._student_service, 
                self._problem_service, 
                self._assignment_service
            )
        except Exception as e:
            print(f"Error saving data: {e}")

    def _handle_load_data(self, args):
        """Handle load_data command"""
        if self._persistence_service is None:
            print("Error: Persistence service not available")
            return
        
        try:
            students, problems, assignments = self._persistence_service.load_application_data()
            
            # Clear current data and load new data
            self._student_service._student_repo = StudentRepository(students)
            self._problem_service._problem_repo = ProblemRepository(problems)
            self._assignment_service._assignment_repo = AssignmentRepository(assignments)
            
            # Update shared repositories
            self._assignment_service.set_student_repo(self._student_service._student_repo)
            self._assignment_service.set_problem_repo(self._problem_service._problem_repo)
            
            print(f"Data loaded successfully: {len(students)} students, {len(problems)} problems, {len(assignments)} assignments")
            
        except Exception as e:
            print(f"Error loading data: {e}")