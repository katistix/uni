from domain.student import Student

class StudentDTO:
    def __init__(self, id: int, name: str, group: int):
        self.id = id
        self.name = name
        self.group = group

    @staticmethod
    def from_domain(student: Student) -> 'StudentDTO':
        return StudentDTO(student.get_id(), student.get_name(), student.get_group())

    def to_domain(self) -> Student:
        return Student(self.id, self.name, self.group)

    def to_csv_row(self) -> str:
        return f"{self.id},{self.name},{self.group}"

    @staticmethod
    def from_csv_row(row: str) -> 'StudentDTO':
        parts = row.strip().split(',')
        return StudentDTO(int(parts[0]), parts[1], int(parts[2]))
