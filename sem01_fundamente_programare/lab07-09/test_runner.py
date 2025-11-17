import domain.student
import repos.student  
import services.student
import domain.problem
import repos.problem
import services.problem
import domain.assignment
import repos.assignment
import services.assignment


def run_all_tests():
    """Run all module tests"""
    print("Running Student Model tests...")
    domain.student.test_module()
    print("✓ Student Model tests passed")
    
    print("Running Student Repository tests...")
    repos.student.test_module()
    print("✓ Student Repository tests passed")
    
    print("Running Student Service tests...")
    services.student.test_module()
    print("✓ Student Service tests passed")
    
    print("Running Problem Model tests...")
    domain.problem.test_module()
    print("✓ Problem Model tests passed")
    
    print("Running Problem Repository tests...")
    repos.problem.test_module()
    print("✓ Problem Repository tests passed")
    
    print("Running Problem Service tests...")
    services.problem.test_module()
    print("✓ Problem Service tests passed")
    
    print("Running Assignment Model tests...")
    domain.assignment.test_module()
    print("✓ Assignment Model tests passed")
    
    print("Running Assignment Repository tests...")
    repos.assignment.test_module()
    print("✓ Assignment Repository tests passed")
    
    print("Running Assignment Service tests...")
    services.assignment.test_module()
    print("✓ Assignment Service tests passed")
    
    print("\nAll tests passed! ✅")


if __name__ == "__main__":
    run_all_tests()