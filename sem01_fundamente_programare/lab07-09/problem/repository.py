from . import model
from datetime import date

class ProblemRepository:
    def __init__(self, problem_list: list[model.Problem]):
        self._problem_list = problem_list

    def add_problem(self, lab_number: int, problem_number: int, description: str, deadline: date) -> model.Problem:
        new_problem = model.Problem(lab_number, problem_number, description, deadline)
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

    def list_problems(self) -> list[model.Problem]:
        """Return a copy of all problems in the repository."""
        return self._problem_list.copy()

    def search_problems_by_id(self, lab_problem_id: str) -> list[model.Problem]:
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


def test_module():
    repo = ProblemRepository([])
    assert repo.list_problems() == []
    
    problem_date = date(2024, 12, 15)
    problem1 = repo.add_problem(7, 1, "Sort array problem", problem_date)
    assert problem1.get_lab_number() == 7
    assert problem1.get_problem_number() == 1
    assert len(repo.list_problems()) == 1
    
    problem2 = repo.add_problem(7, 2, "Search problem", problem_date)
    assert len(repo.list_problems()) == 2
    
    new_date = date(2024, 12, 20)
    repo.modify_problem(7, 1, "Updated sort problem", new_date)
    modified_problem = repo.list_problems()[0]
    assert modified_problem.get_description() == "Updated sort problem"
    assert modified_problem.get_deadline() == new_date
    
    try:
        repo.modify_problem(99, 99, "Test", new_date)
        assert False
    except ValueError as e:
        assert "not found" in str(e)
    
    results = repo.search_problems_by_id("7_1")
    assert len(results) == 1
    assert results[0].get_lab_number() == 7
    assert results[0].get_problem_number() == 1
    
    results = repo.search_problems_by_id("invalid")
    assert len(results) == 0
    
    results = repo.search_problems_by_id("99_99")
    assert len(results) == 0
    
    repo.remove_problem(7, 1)
    assert len(repo.list_problems()) == 1
    
    try:
        repo.remove_problem(99, 99)
        assert False
    except ValueError as e:
        assert "not found" in str(e)