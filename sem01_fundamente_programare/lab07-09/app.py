from problem.repository import ProblemRepository
from student.repository import StudentRepository
from ui.cli import CLI

class StudentAssignmentsAPP:
    def __init__(self):
        self.problem_repo = ProblemRepository([])
        self.student_repo = StudentRepository([])

    def run(self):
        """Run the application loop as a CLI"""
        cli_interface = CLI(self.problem_repo, self.student_repo)
        cli_interface.run()