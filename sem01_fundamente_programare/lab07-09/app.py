from ui.cli import CLI

class StudentAssignmentsAPP:
    def __init__(self):
        pass

    def run(self):
        """Run the application loop as a CLI"""
        cli_interface = CLI()
        cli_interface.run()