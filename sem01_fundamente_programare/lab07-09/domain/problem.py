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


