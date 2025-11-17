from repos.problem import ProblemRepository
from domain.problem import Problem
from datetime import date


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


def test_module():
    service = ProblemService()
    
    problem_date = date(2024, 12, 15)
    problem1 = service.add_problem(7, 1, "Sort array problem", problem_date)
    assert problem1.get_lab_number() == 7
    assert problem1.get_problem_number() == 1
    assert problem1.get_description() == "Sort array problem"
    
    problems = service.list_problems()
    assert len(problems) == 1
    assert problems[0].get_description() == "Sort array problem"
    
    problem2 = service.add_problem(7, 2, "Search problem", problem_date)
    assert len(service.list_problems()) == 2
    
    new_date = date(2024, 12, 20)
    service.modify_problem(7, 1, "Updated sort problem", new_date)
    updated_problems = service.list_problems()
    updated_problem = next(p for p in updated_problems if p.get_problem_number() == 1)
    assert updated_problem.get_description() == "Updated sort problem"
    assert updated_problem.get_deadline() == new_date
    
    results = service.search_problems_by_id("7_1")
    assert len(results) == 1
    assert results[0].get_lab_number() == 7
    assert results[0].get_problem_number() == 1
    
    results = service.search_problems_by_id("invalid")
    assert len(results) == 0
    
    service.remove_problem(7, 1)
    assert len(service.list_problems()) == 1
    
    try:
        service.remove_problem(99, 99)
        assert False
    except ValueError as e:
        assert "not found" in str(e)
    
    try:
        service.modify_problem(99, 99, "Test", new_date)
        assert False
    except ValueError as e:
        assert "not found" in str(e)