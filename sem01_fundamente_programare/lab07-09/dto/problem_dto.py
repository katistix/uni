from domain.problem import Problem
from datetime import datetime, date

class ProblemDTO:
    def __init__(self, lab_number: int, problem_number: int, description: str, deadline: date):
        self.lab_number = lab_number
        self.problem_number = problem_number
        self.description = description
        self.deadline = deadline

    @staticmethod
    def from_domain(problem: Problem) -> 'ProblemDTO':
        return ProblemDTO(
            problem.get_lab_number(),
            problem.get_problem_number(),
            problem.get_description(),
            problem.get_deadline()
        )

    def to_domain(self) -> Problem:
        return Problem(
            self.lab_number,
            self.problem_number,
            self.description,
            self.deadline
        )

    def to_csv_row(self) -> str:
        deadline_str = self.deadline.strftime("%Y-%m-%d")
        return f"{self.lab_number},{self.problem_number},{self.description},{deadline_str}"

    @staticmethod
    def from_csv_row(row: str) -> 'ProblemDTO':
        parts = row.strip().split(',')
        lab_number = int(parts[0])
        problem_number = int(parts[1])
        description = parts[2]
        deadline = datetime.strptime(parts[3], "%Y-%m-%d").date()
        return ProblemDTO(lab_number, problem_number, description, deadline)
