from repos.problem import ProblemRepository
from domain.problem import Problem
from datetime import date
from domain.assignment import Assignment
from domain.problem_statistic import ProblemStatistic
from typing import List



class ProblemService:
    def __init__(self):
        self._problem_repo = ProblemRepository([])

    def add_problem(self, lab_number: int, problem_number: int, description: str, deadline: date) -> Problem:
        """Add a new problem through the service layer"""
        problem = self._problem_repo.add_problem(lab_number, problem_number, description, deadline)
        return problem

    def list_problems(self) -> list[Problem]:
        """Get all problems through the service layer"""
        problems = self._problem_repo.list_problems()
        return problems
    
    def remove_problem(self, lab_number: int, problem_number: int) -> None:
        """Remove a problem by lab and problem number. Raises ValueError if not found."""
        try:
            self._problem_repo.remove_problem(lab_number, problem_number)
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def modify_problem(self, lab_number: int, problem_number: int, new_description: str, new_deadline: date) -> None:
        """Modify an existing problem's description and deadline. Raises ValueError if not found."""
        try:
            self._problem_repo.modify_problem(lab_number, problem_number, new_description, new_deadline)
        except ValueError as e:
            raise ValueError(f"Error: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {e}")

    def search_problems_by_id(self, lab_problem_id: str) -> list[Problem]:
        """Search for problems by id in format 'lab_problem' (e.g., '7_1')"""
        results = self._problem_repo.search_problems_by_id(lab_problem_id)
        return results

    def get_top_problems(self, assignments: list, limit: int = 10) -> List[ProblemStatistic]:
        """Get top problems by number of assignments (popularity)"""
        
        problems = self._problem_repo.list_problems()
        problem_stats = []
        
        for problem in problems:
            problem_id = f"{problem.get_lab_number()}_{problem.get_problem_number()}"
            problem_assignments = [a for a in assignments if a.get_problem_id() == problem_id]
            
            problem_stats.append(ProblemStatistic(
                problem_id=problem_id,
                lab_number=problem.get_lab_number(),
                problem_number=problem.get_problem_number(),
                description=problem.get_description(),
                total_assignments=len(problem_assignments),
                graded_assignments=len([a for a in problem_assignments if a.has_grade()])
            ))
        
        # Sort by total assignments descending (popularity)
        problem_stats.sort(key=lambda x: x.get_total_assignments(), reverse=True)
        return problem_stats[:limit]

