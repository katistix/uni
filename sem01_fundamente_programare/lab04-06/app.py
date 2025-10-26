import ui
import storage
import menu_handler


class ComplexNumberApp:
    """Main application class for managing complex numbers"""
    
    def __init__(self):
        self.data_storage = storage.Storage([])
    
    def run(self):
        """Run the main application loop"""
        while True:
            ui.show_menu()
            option = ui.get_menu_option()
            
            should_exit = menu_handler.process_menu_option(option, self.data_storage)
            if should_exit:
                break
            
            input("\nApasati Enter pentru a continua...")
            ui.clear_screen()


def create_app():
    """Factory function to create and configure the application"""
    return ComplexNumberApp()