from domain.problem import Problem
from datetime import date

class ProblemRepository:
    def __init__(self, problem_list: list[Problem]):
        self._problem_list = problem_list

    def add_problem(self, lab_number: int, problem_number: int, description: str, deadline: date) -> Problem:
        new_problem = Problem(lab_number, problem_number, description, deadline)
        self._problem_list.append(new_problem)
        return new_problem

    def remove_problem(self, lab_number: int, problem_number: int) -> None:
        """Remove a problem by lab and problem number. Raises ValueError if not found."""
        for problem in self._problem_list:
            if problem.get_lab_number() == lab_number and problem.get_problem_number() == problem_number:
                self._problem_list.remove(problem)
                return
        raise ValueError(f"Problem {lab_number}.{problem_number} not found")

    def modify_problem(self, lab_number: int, problem_number: int, new_description: str, new_deadline: date) -> None:
        """Modify an existing problem's description and deadline. Raises ValueError if not found."""
        for problem in self._problem_list:
            if problem.get_lab_number() == lab_number and problem.get_problem_number() == problem_number:
                problem.set_description(new_description)
                problem.set_deadline(new_deadline)
                return
        raise ValueError(f"Problem {lab_number}.{problem_number} not found")

    def list_problems(self) -> list[Problem]:
        """Return a copy of all problems in the repository."""
        return self._problem_list.copy()

    def search_problems_by_id(self, lab_problem_id: str) -> list[Problem]:
        """Search for problems by id in format 'lab_problem' (e.g., '7_1').
        
        Args:
            lab_problem_id: The problem ID in format 'lab_problem' (e.g., '7_1')
        
        Returns:
            List of matching problems
        """
        results = []
        
        try:
            if '_' not in lab_problem_id:
                return results
            
            lab_number, problem_number = lab_problem_id.split('_', 1)
            lab_number = int(lab_number)
            problem_number = int(problem_number)
            
            for problem in self._problem_list:
                if (problem.get_lab_number() == lab_number and 
                    problem.get_problem_number() == problem_number):
                    results.append(problem)
        except ValueError:
            pass
        
        return results

    def find_problem(self, lab_number: int, problem_number: int) -> Problem | None:
        """Find a problem by lab and problem number. Returns the problem or None if not found."""
        for problem in self._problem_list:
            if (problem.get_lab_number() == lab_number and 
                problem.get_problem_number() == problem_number):
                return problem
        return None

