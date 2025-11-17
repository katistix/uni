from datetime import date

class Problem:
    def __init__(self, lab_number: int, problem_number: int, description: str, deadline: date):
        self._lab_number = lab_number
        self._problem_number = problem_number
        self._description = description
        self._deadline = deadline

    # --- Getters ---
    def get_lab_number(self) -> int:
        return self._lab_number

    def get_problem_number(self) -> int:
        return self._problem_number

    def get_description(self) -> str:
        return self._description

    def get_deadline(self) -> date:
        return self._deadline

    # --- Setters ---
    def set_lab_number(self, new_lab_number: int):
        self._lab_number = new_lab_number

    def set_problem_number(self, new_problem_number: int):
        self._problem_number = new_problem_number

    def set_description(self, new_description: str):
        self._description = new_description

    def set_deadline(self, new_deadline: date):
        self._deadline = new_deadline


def test_module():
    problem_date = date(2024, 12, 15)
    problem = Problem(7, 1, "Sort array problem", problem_date)
    
    assert problem.get_lab_number() == 7
    assert problem.get_problem_number() == 1
    assert problem.get_description() == "Sort array problem"
    assert problem.get_deadline() == problem_date
    
    problem.set_lab_number(8)
    assert problem.get_lab_number() == 8
    
    problem.set_problem_number(2)
    assert problem.get_problem_number() == 2
    
    problem.set_description("Updated description")
    assert problem.get_description() == "Updated description"
    
    new_date = date(2024, 12, 20)
    problem.set_deadline(new_date)
    assert problem.get_deadline() == new_date
