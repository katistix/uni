import ui
import storage


def handle_add_complex_number(data_storage):
    """Handle adding a new complex number to the list"""
    print("\n=== ADAUGARE NUMAR COMPLEX ===")
    try:
        new_number = ui.get_complex_number_input()
        data_storage.append_number(new_number)
        module = new_number.get_module()
        print(f"Numar adaugat: {new_number.get_string()} cu modulul = {module:.3f}")
        print(f"Lista are acum {len(data_storage.get_numbers())} elemente")
    except Exception as e:
        print(f"Eroare la adaugarea numarului: {e}")


def handle_show_current_list(data_storage):
    """Handle displaying the current list of numbers"""
    print("\n=== LISTA CURENTA ===")
    ui.show_numbers_with_modules(data_storage.get_numbers())


def handle_show_imaginary_parts_interval(data_storage):
    """Handle displaying imaginary parts from an interval"""
    print("\n=== PARTI IMAGINARE DIN INTERVAL ===")
    numbers = data_storage.get_numbers()
    if not numbers:
        print("Lista este goala")
    else:
        ui.show_numbers_with_modules(numbers)
        try:
            start, end = ui.get_interval_input(len(numbers) - 1)
            parts = data_storage.get_imaginary_parts_interval(start, end)
            ui.show_imaginary_parts(numbers, parts, start, end)
        except Exception as e:
            print(f"Eroare: {e}")


def handle_show_numbers_module_less_than_ten(data_storage):
    """Handle displaying numbers with module less than 10"""
    print("\n=== NUMERE CU MODULUL MAI MIC DECAT 10 ===")
    filtered_numbers = data_storage.get_numbers_module_less_than(10.0)
    ui.show_filtered_numbers(filtered_numbers, "Numere cu modul < 10")
    
    # Afiseaza si numerele excluse pentru claritate
    all_numbers = data_storage.get_numbers()
    excluded = [n for n in all_numbers if n.get_module() >= 10.0]
    if excluded:
        print("\nNumere excluse (modul >= 10):")
        for number in excluded:
            module = number.get_module()
            print(f"{number.get_string()} modul = {module:.3f}")


def handle_show_numbers_module_equal_ten(data_storage):
    """Handle displaying numbers with module equal to 10"""
    print("\n=== NUMERE CU MODULUL EGAL CU 10 ===")
    filtered_numbers = data_storage.get_numbers_module_equal(10.0)
    ui.show_filtered_numbers(filtered_numbers, "Numere cu modul = 10")
    
    if not filtered_numbers:
        print("Sugestii pentru numere cu modul = 10: 6+8i, 10+0i, 0+10i, 8+6i")


def handle_show_help():
    """Handle displaying help information"""
    ui.show_help()


def handle_exit():
    """Handle application exit"""
    print("La revedere!")
    return True


def handle_insert_at_position(data_storage):
    """Handle inserting a complex number at a given position"""
    print("\n=== INSERARE NUMAR LA POZITIE ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala. Adaugati primul numar.")
        handle_add_complex_number(data_storage)
        return
    
    ui.show_numbers_with_modules(numbers)
    try:
        position = ui.get_position_input(len(numbers), "inserare")
        new_number = ui.get_complex_number_input()
        
        data_storage.insert_number_at_position(position, new_number)
        module = new_number.get_module()
        print(f"Numar {new_number.get_string()} inserat la pozitia {position}")
        print(f"Lista are acum {len(data_storage.get_numbers())} elemente")
        
        print("\nLista actualizata:")
        ui.show_numbers_with_modules(data_storage.get_numbers())
        
    except (ValueError, Exception) as e:
        print(f"Eroare: {e}")


def handle_delete_at_position(data_storage):
    """Handle deleting a complex number from a given position"""
    print("\n=== STERGERE NUMAR DE LA POZITIE ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    ui.show_numbers_with_modules(numbers)
    try:
        position = ui.get_position_input(len(numbers) - 1, "stergere")
        deleted_number = data_storage.delete_number_at_position(position)
        
        print(f"Numar {deleted_number.get_string()} sters de la pozitia {position}")
        print(f"Lista are acum {len(data_storage.get_numbers())} elemente")
        
        if data_storage.get_numbers():
            print("\nLista actualizata:")
            ui.show_numbers_with_modules(data_storage.get_numbers())
        else:
            print("Lista este acum goala")
            
    except (ValueError, Exception) as e:
        print(f"Eroare: {e}")


def handle_sum_subsequence(data_storage):
    """Handle calculating sum of numbers from a subsequence"""
    print("\n=== SUMA NUMERELOR DINTR-O SUBSECVENTA ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    ui.show_numbers_with_modules(numbers)
    try:
        start, end = ui.get_interval_input(len(numbers) - 1)
        result_sum = data_storage.sum_numbers_interval(start, end)
        ui.show_sum_result(numbers, result_sum, start, end)
        
    except (ValueError, Exception) as e:
        print(f"Eroare: {e}")


def handle_delete_interval(data_storage):
    """Handle deleting numbers from an interval of positions"""
    print("\n=== STERGERE NUMERE DINTR-UN INTERVAL ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    ui.show_numbers_with_modules(numbers)
    try:
        start, end = ui.get_interval_input(len(numbers) - 1)
        deleted_count = data_storage.delete_numbers_interval(start, end)
        
        print(f"Sterse {deleted_count} numere din intervalul [{start}, {end}]")
        print(f"Lista are acum {len(data_storage.get_numbers())} elemente")
        
        if data_storage.get_numbers():
            print("\nLista actualizata:")
            ui.show_numbers_with_modules(data_storage.get_numbers())
        else:
            print("Lista este acum goala")
            
    except (ValueError, Exception) as e:
        print(f"Eroare: {e}")


def handle_replace_all_occurrences(data_storage):
    """Handle replacing all occurrences of a complex number"""
    print("\n=== INLOCUIRE TOATE APARITIILE ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    ui.show_numbers_with_modules(numbers)
    try:
        print("Introduceti numarul complex de inlocuit:")
        old_number = ui.get_complex_number_input()
        
        print("Introduceti numarul complex nou:")
        new_number = ui.get_complex_number_input()
        
        replacement_count = data_storage.replace_all_occurrences(old_number, new_number)
        ui.show_replacement_result(old_number, new_number, replacement_count)
        
        if replacement_count > 0:
            print("\nLista actualizata:")
            ui.show_numbers_with_modules(data_storage.get_numbers())
            
    except (ValueError, Exception) as e:
        print(f"Eroare: {e}")


def handle_product_subsequence(data_storage):
    """Handle calculating product of numbers from a subsequence"""
    print("\n=== PRODUSUL NUMERELOR DINTR-O SUBSECVENTA ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    ui.show_numbers_with_modules(numbers)
    try:
        start, end = ui.get_interval_input(len(numbers) - 1)
        result_product = data_storage.product_numbers_interval(start, end)
        ui.show_product_result(numbers, result_product, start, end)
        
    except (ValueError, Exception) as e:
        print(f"Eroare: {e}")


def handle_sort_by_imaginary(data_storage):
    """Handle displaying list sorted by imaginary part"""
    print("\n=== LISTA SORTATA DUPA PARTEA IMAGINARA ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    sorted_numbers = data_storage.get_sorted_by_imaginary(descending=True)
    ui.show_sorted_numbers(sorted_numbers, "Lista sortata descrescator dupa partea imaginara")


def handle_filter_prime_real(data_storage):
    """Handle filtering numbers with prime real parts"""
    print("\n=== FILTRARE NUMERE CU PARTEA REALA PRIMA ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    print("Lista inainte de filtrare:")
    ui.show_numbers_with_modules(numbers)
    
    try:
        removed_count = data_storage.filter_real_part_prime()
        remaining_count = len(data_storage.get_numbers())
        
        ui.show_filter_result("Filtrare partea reala prima", removed_count, remaining_count)
        
        if remaining_count > 0:
            print("\nLista dupa filtrare:")
            ui.show_numbers_with_modules(data_storage.get_numbers())
        else:
            print("Lista este acum goala")
            
    except Exception as e:
        print(f"Eroare: {e}")


def handle_filter_by_module(data_storage):
    """Handle filtering numbers by module with operator"""
    print("\n=== FILTRARE NUMERE DUPA MODUL ===")
    numbers = data_storage.get_numbers()
    
    if not numbers:
        print("Lista este goala")
        return
    
    print("Lista inainte de filtrare:")
    ui.show_numbers_with_modules(numbers)
    
    try:
        operator = ui.get_operator_input()
        value = ui.get_float_input("Introduceti valoarea pentru comparatie: ")
        
        removed_count = data_storage.filter_by_module(operator, value)
        remaining_count = len(data_storage.get_numbers())
        
        filter_description = f"Eliminare numere cu modul {operator} {value}"
        ui.show_filter_result(filter_description, removed_count, remaining_count)
        
        if remaining_count > 0:
            print("\nLista dupa filtrare:")
            ui.show_numbers_with_modules(data_storage.get_numbers())
        else:
            print("Lista este acum goala")
            
    except Exception as e:
        print(f"Eroare: {e}")


def handle_undo(data_storage):
    """Handle undo last operation"""
    print("\n=== UNDO ULTIMA OPERATIE ===")
    
    success = data_storage.undo_last_operation()
    ui.show_undo_result(success)
    
    if success:
        print("Lista dupa undo:")
        ui.show_numbers_with_modules(data_storage.get_numbers())


# Menu option mapping
MENU_HANDLERS = {
    '1': handle_add_complex_number,
    '2': handle_show_current_list,
    '3': handle_show_imaginary_parts_interval,
    '4': handle_show_numbers_module_less_than_ten,
    '5': handle_show_numbers_module_equal_ten,
    '6': handle_insert_at_position,
    '7': handle_delete_at_position,
    '8': handle_sum_subsequence,
    '9': handle_delete_interval,
    '10': handle_replace_all_occurrences,
    '11': handle_product_subsequence,
    '12': handle_sort_by_imaginary,
    '13': handle_filter_prime_real,
    '14': handle_filter_by_module,
    '15': handle_undo,
    'h': lambda data_storage: handle_show_help(),
    '0': lambda data_storage: handle_exit()
}


def process_menu_option(option, data_storage):
    """Process a menu option and return True if should exit"""
    if option in MENU_HANDLERS:
        handler = MENU_HANDLERS[option]
        result = handler(data_storage)
        return result is True  # Only exit handler returns True
    else:
        print("Optiune invalida. Incercati din nou.")
        return False