class ProblemStatistic:
    """DTO class for problem statistics data used in reports"""
    
    def __init__(self, problem_id: str, lab_number: int, problem_number: int,
                 description: str, total_assignments: int, graded_assignments: int):
        self._problem_id = problem_id
        self._lab_number = lab_number
        self._problem_number = problem_number
        self._description = description
        self._total_assignments = total_assignments
        self._graded_assignments = graded_assignments
    
    def get_problem_id(self) -> str:
        return self._problem_id
    
    def get_lab_number(self) -> int:
        return self._lab_number
    
    def get_problem_number(self) -> int:
        return self._problem_number
    
    def get_description(self) -> str:
        return self._description
    
    def get_total_assignments(self) -> int:
        return self._total_assignments
    
    def get_graded_assignments(self) -> int:
        return self._graded_assignments
    
    def __repr__(self) -> str:
        return (f"ProblemStatistic(id='{self._problem_id}', "
                f"description='{self._description[:30]}...', "
                f"assignments={self._graded_assignments}/{self._total_assignments})")


def test_module():
    # Test basic creation
    stat = ProblemStatistic("7_1", 7, 1, "Sort array problem", 15, 12)
    assert stat.get_problem_id() == "7_1"
    assert stat.get_lab_number() == 7
    assert stat.get_problem_number() == 1
    assert stat.get_description() == "Sort array problem"
    assert stat.get_total_assignments() == 15
    assert stat.get_graded_assignments() == 12
    
    # Test with no graded assignments
    stat_no_grades = ProblemStatistic("8_2", 8, 2, "Advanced algorithms", 5, 0)
    assert stat_no_grades.get_total_assignments() == 5
    assert stat_no_grades.get_graded_assignments() == 0
    
    # Test repr
    repr_str = repr(stat)
    assert "ProblemStatistic" in repr_str
    assert "7_1" in repr_str
    assert "Sort array problem" in repr_str
    assert "12/15" in repr_str


if __name__ == "__main__":
    test_module()