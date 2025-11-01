import test_runner
import app


def main():
    # Run all tests before starting the application
    test_runner.run_all_tests()

    
    # Create and run the application
    application = app.create_app()
    application.run()


if __name__ == "__main__":
    main()