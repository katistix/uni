import random
from services.student import StudentService


random.seed(123)

studentSvc = StudentService()

print(studentSvc.generate_random_name())
print(studentSvc.generate_random_name())
print(studentSvc.generate_random_name())

print(studentSvc.generate_random_group())
print(studentSvc.generate_random_group())
print(studentSvc.generate_random_group())



