from typing import Optional


class StudentStatistic:
    """DTO class for student statistics data used in reports"""
    
    def __init__(self, student_id: int, student_name: str, group: int, 
                 average_grade: Optional[float], total_assignments: int, 
                 graded_assignments: int):
        self._student_id = student_id
        self._student_name = student_name
        self._group = group
        self._average_grade = average_grade
        self._total_assignments = total_assignments
        self._graded_assignments = graded_assignments
    
    def get_student_id(self) -> int:
        return self._student_id
    
    def get_student_name(self) -> str:
        return self._student_name
    
    def get_group(self) -> int:
        return self._group
    
    def get_average_grade(self) -> Optional[float]:
        return self._average_grade
    
    def get_total_assignments(self) -> int:
        return self._total_assignments
    
    def get_graded_assignments(self) -> int:
        return self._graded_assignments
    
    def __repr__(self) -> str:
        avg_str = f"{self._average_grade:.2f}" if self._average_grade is not None else "N/A"
        return (f"StudentStatistic(id={self._student_id}, name='{self._student_name}', "
                f"group={self._group}, avg_grade={avg_str}, "
                f"assignments={self._graded_assignments}/{self._total_assignments})")


def test_module():
    # Test basic creation
    stat = StudentStatistic(1, "John Doe", 917, 9.5, 10, 8)
    assert stat.get_student_id() == 1
    assert stat.get_student_name() == "John Doe"
    assert stat.get_group() == 917
    assert stat.get_average_grade() == 9.5
    assert stat.get_total_assignments() == 10
    assert stat.get_graded_assignments() == 8
    
    # Test with no average grade
    stat_no_grade = StudentStatistic(2, "Jane Smith", 918, None, 5, 0)
    assert stat_no_grade.get_average_grade() is None
    assert stat_no_grade.get_total_assignments() == 5
    assert stat_no_grade.get_graded_assignments() == 0
    
    # Test repr
    repr_str = repr(stat)
    assert "StudentStatistic" in repr_str
    assert "John Doe" in repr_str
    assert "9.50" in repr_str


if __name__ == "__main__":
    test_module()