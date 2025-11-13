import student.model
import student.repository  
import student.service
import problem.model
import problem.repository


def run_all_tests():
    """Run all module tests"""
    print("Running Student Model tests...")
    student.model.test_module()
    print("✓ Student Model tests passed")
    
    print("Running Student Repository tests...")
    student.repository.test_module()
    print("✓ Student Repository tests passed")
    
    print("Running Student Service tests...")
    student.service.test_module()
    print("✓ Student Service tests passed")
    
    print("Running Problem Model tests...")
    problem.model.test_module()
    print("✓ Problem Model tests passed")
    
    print("Running Problem Repository tests...")
    problem.repository.test_module()
    print("✓ Problem Repository tests passed")
    
    print("\nAll tests passed! ✅")


if __name__ == "__main__":
    run_all_tests()