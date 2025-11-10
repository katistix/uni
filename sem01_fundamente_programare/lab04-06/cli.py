import shlex
import ui
import menu_handler


class CLI:
    def __init__(self, data_storage):
        self.data_storage = data_storage
        self.running = True
        
        # Command mapping from CLI commands to menu handlers
        self.commands = {
            # Basic
            'add': self._handle_add,
            'show': self._handle_show,
            'list': self._handle_show,

            # Extra
            'imaginary': self._handle_imaginary_parts,
            'module': self._handle_module_filter,
            'insert': self._handle_insert,
            'delete': self._handle_delete,
            'del': self._handle_delete,
            'sum': self._handle_sum,
            'replace': self._handle_replace,
            'product': self._handle_product,
            'sort': self._handle_sort,
            'filter': self._handle_filter,
            'undo': self._handle_undo,


            # Helpers
            'help': self._handle_help,
            'exit': self._handle_exit,
            'quit': self._handle_exit,
            'clear': self._handle_clear,
        }

    def run(self):
        """Run the CLI main loop"""
        print("APLICATIE NUMERE COMPLEXE - CLI")
        print("Tastati 'help' pentru lista comenzilor sau 'exit' pentru iesire\n")
        
        while self.running:
            try:
                user_input = input("complex> ").strip()
                if user_input:
                    self._process_command(user_input)
            except KeyboardInterrupt:
                print("\nLa revedere!")
                break
            except EOFError:
                print("\nLa revedere!")
                break

    def _process_command(self, user_input):
        """Process a single command"""
        try:
            # Parse command and arguments
            parts = shlex.split(user_input)
            if not parts:
                return
                
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            # Execute command
            if command in self.commands:
                self.commands[command](args)
            else:
                print(f"Comanda necunoscuta: '{command}'. Tastati 'help' pentru lista comenzilor.")
                
        except ValueError as e:
            print(f"Eroare la parsarea comenzii: {e}")
        except Exception as e:
            print(f"Eroare la executarea comenzii: {e}")

    def _handle_add(self, args):
        """Handle add command: add <complex_number>"""
        if not args:
            print("Folositi: add <numar_complex>")
            print("Exemple: add 3+4i, add 5-2i, add 7+0i")
            return
            
        try:
            complex_str = ' '.join(args)
            new_number = ui.parse_complex_number(complex_str)
            self.data_storage.append_number(new_number)
            module = new_number.get_module()
            print(f"Numar adaugat: {new_number.get_string()} cu modulul = {module:.3f}")
            print(f"Lista are acum {len(self.data_storage.get_numbers())} elemente")
        except ValueError as e:
            print(f"Format invalid: {e}")
            print("Exemple valide: add 3+4i, add 5-2i, add 7+0i")

    def _handle_show(self, args):
        """Handle show/list command"""
        menu_handler.handle_show_current_list(self.data_storage)

    def _handle_imaginary_parts(self, args):
        """Handle imaginary command: imaginary <start> <end>"""
        if len(args) < 2:
            print("Folositi: imaginary <start> <end>")
            print("Exemple: imaginary 0 2")
            return
            
        try:
            start = int(args[0])
            end = int(args[1])
            numbers = self.data_storage.get_numbers()
            if not numbers:
                print("Lista este goala")
                return
            if start < 0 or end >= len(numbers) or start > end:
                print(f"Interval invalid. Trebuie sa fie intre 0 si {len(numbers)-1}, cu start <= end")
                return
            parts = self.data_storage.get_imaginary_parts_interval(start, end)
            ui.show_imaginary_parts(numbers, parts, start, end)
        except ValueError:
            print("Folositi numere intregi pentru interval: imaginary <start> <end>")

    def _handle_module_filter(self, args):
        """Handle module command: module <10 | =10"""
        if len(args) < 1:
            print("Folositi: module <10 sau module =10")
            return
            
        arg = args[0]
        if arg == "<10":
            menu_handler.handle_show_numbers_module_less_than_ten(self.data_storage)
        elif arg == "=10":
            menu_handler.handle_show_numbers_module_equal_ten(self.data_storage)
        else:
            print("Folositi: module <10 sau module =10")

    def _handle_insert(self, args):
        """Handle insert command: insert <position> <complex_number>"""
        if len(args) < 2:
            print("Folositi: insert <pozitie> <numar_complex>")
            print("Exemple: insert 0 3+4i")
            return
            
        try:
            position = int(args[0])
            complex_str = ' '.join(args[1:])
            new_number = ui.parse_complex_number(complex_str)
            self.data_storage.insert_number_at_position(position, new_number)
            print(f"Numar {new_number.get_string()} inserat la pozitia {position}")
            print(f"Lista are acum {len(self.data_storage.get_numbers())} elemente")
        except (ValueError, IndexError) as e:
            print(f"Eroare: {e}")
            print("Folositi: insert <pozitie> <numar_complex>")

    def _handle_delete(self, args):
        """Handle delete command: delete <position> or delete <start> <end>"""
        if len(args) == 0:
            print("Folositi: delete <pozitie> sau delete <start> <end>")
            return
        elif len(args) == 1:
            try:
                position = int(args[0])
                deleted_number = self.data_storage.delete_number_at_position(position)
                print(f"Numar {deleted_number.get_string()} sters de la pozitia {position}")
                print(f"Lista are acum {len(self.data_storage.get_numbers())} elemente")
            except (ValueError, IndexError) as e:
                print(f"Eroare: {e}")
        elif len(args) == 2:
            try:
                start = int(args[0])
                end = int(args[1])
                deleted_count = self.data_storage.delete_numbers_interval(start, end)
                print(f"Sterse {deleted_count} numere din intervalul [{start}, {end}]")
                print(f"Lista are acum {len(self.data_storage.get_numbers())} elemente")
            except (ValueError, IndexError) as e:
                print(f"Eroare: {e}")
        else:
            print("Folositi: delete <pozitie> sau delete <start> <end>")

    def _handle_sum(self, args):
        """Handle sum command: sum <start> <end>"""
        if len(args) < 2:
            print("Folositi: sum <start> <end>")
            print("Exemple: sum 0 2")
            return
            
        try:
            start = int(args[0])
            end = int(args[1])
            numbers = self.data_storage.get_numbers()
            if start < 0 or end >= len(numbers) or start > end:
                print(f"Interval invalid. Trebuie sa fie intre 0 si {len(numbers)-1}")
                return
            result_sum = self.data_storage.sum_numbers_interval(start, end)
            ui.show_sum_result(numbers, result_sum, start, end)
        except ValueError:
            print("Folositi numere intregi: sum <start> <end>")

    def _handle_replace(self, args):
        """Handle replace command: replace <old_number> <new_number>"""
        if len(args) < 2:
            print("Folositi: replace <numar_vechi> <numar_nou>")
            print("Exemple: replace 3+4i 5-2i")
            return
            
        try:
            # Split args in half to get old and new numbers
            mid = len(args) // 2
            old_str = ' '.join(args[:mid])
            new_str = ' '.join(args[mid:])
            
            # Try to parse both numbers
            old_number = ui.parse_complex_number(old_str)
            new_number = ui.parse_complex_number(new_str)
            
            replacement_count = self.data_storage.replace_all_occurrences(old_number, new_number)
            ui.show_replacement_result(old_number, new_number, replacement_count)
            
            if replacement_count > 0:
                print("\nLista actualizata:")
                ui.show_numbers_with_modules(self.data_storage.get_numbers())
                
        except ValueError as e:
            print(f"Format invalid: {e}")
            print("Pentru numere complexe cu mai multe parti, folositi ghilimele:")
            print('Exemple: replace "3+4i" "5-2i"')

    def _handle_product(self, args):
        """Handle product command: product <start> <end>"""
        if len(args) < 2:
            print("Folositi: product <start> <end>")
            print("Exemple: product 0 2")
            return
            
        try:
            start = int(args[0])
            end = int(args[1])
            numbers = self.data_storage.get_numbers()
            if start < 0 or end >= len(numbers) or start > end:
                print(f"Interval invalid. Trebuie sa fie intre 0 si {len(numbers)-1}")
                return
            result_product = self.data_storage.product_numbers_interval(start, end)
            ui.show_product_result(numbers, result_product, start, end)
        except ValueError:
            print("Folositi numere intregi: product <start> <end>")

    def _handle_sort(self, args):
        """Handle sort command"""
        menu_handler.handle_sort_by_imaginary(self.data_storage)

    def _handle_filter(self, args):
        """Handle filter command: filter prime | filter module <op> <value>"""
        if not args:
            print("Folositi: filter prime sau filter module <operator> <valoare>")
            print("Exemple: filter prime, filter module > 5")
            return
            
        if args[0] == "prime":
            menu_handler.handle_filter_prime_real(self.data_storage)
        elif args[0] == "module":
            if len(args) < 3:
                print("Folositi: filter module <operator> <valoare>")
                print("Exemple: filter module > 5, filter module = 10")
                return
            try:
                operator = args[1]
                value = float(args[2])
                if operator not in ['<', '=', '>']:
                    print("Operator invalid. Folositi <, = sau >")
                    return
                removed_count = self.data_storage.filter_by_module(operator, value)
                remaining_count = len(self.data_storage.get_numbers())
                filter_description = f"Eliminare numere cu modul {operator} {value}"
                ui.show_filter_result(filter_description, removed_count, remaining_count)
                if remaining_count > 0:
                    print("\nLista dupa filtrare:")
                    ui.show_numbers_with_modules(self.data_storage.get_numbers())
            except ValueError:
                print("Valoare invalida pentru modul")
        else:
            print("Folositi: filter prime sau filter module <operator> <valoare>")

    def _handle_undo(self, args):
        """Handle undo command"""
        menu_handler.handle_undo(self.data_storage)

    def _handle_help(self, args):
        """Handle help command"""
        print("""
COMENZI DISPONIBILE:

Operatii de baza:
  add <numar>              - Adauga numar complex (ex: add 3+4i)
  show, list               - Afiseaza lista curenta
  insert <pos> <numar>     - Insereaza numar la pozitie (ex: insert 0 3+4i)
  delete <pos>             - Sterge numar de la pozitie (ex: delete 0)
  delete <start> <end>     - Sterge interval de numere (ex: delete 0 2)

Operatii pe intervale:
  imaginary <start> <end>  - Afiseaza parti imaginare din interval (ex: imaginary 0 2)
  sum <start> <end>        - Suma numerelor din interval (ex: sum 0 2)
  product <start> <end>    - Produsul numerelor din interval (ex: product 0 2)

Filtrare si sortare:
  module <10               - Numere cu modul < 10
  module =10               - Numere cu modul = 10
  sort                     - Sorteaza dupa partea imaginara
  filter prime             - Filtreaza partea reala prima
  filter module <op> <val> - Filtreaza dupa modul (ex: filter module > 5)

Alte comenzi:
  replace <vechi> <nou>    - Inlocuieste toate aparitiile (ex: replace 3+4i 5-2i)
  undo                     - Anuleaza ultima operatie
  clear                    - Sterge ecranul
  help                     - Afiseaza acest mesaj
  exit, quit               - Iesire din aplicatie

Format numere complexe: 3+4i, 5-2i, 7+0i, 0+3i, i, -i
Notatie: <argument_obligatoriu> [argument_optional]
""")  

    def _handle_clear(self, args):
        """Handle clear command"""
        ui.clear_screen()

    def _handle_exit(self, args):
        """Handle exit command"""
        print("La revedere!")
        self.running = False