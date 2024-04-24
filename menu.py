from helpers import clear_screen
import sys

class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options

    def display(self):
        print(self.title)
        for index, option in enumerate(self.options, start=1):
            print(f"{index}. {option[0]}")

    def run(self):
        try:
            while True:
                self.display()
                choice = input("> ")
                clear_screen()
                if choice.isdigit() and 1 <= int(choice) <= len(self.options):
                    _, action, args = self.options[int(choice) - 1]
                    
                    if action and 'delete' in action.__name__: 
                        action(*args)
                        break
 
                    if action:
                        action(*args)
                    else:
                        break  # Exit the menu loop if action is None (e.g., 'Exit' option)
                else:
                    print("Invalid option, please try again.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Closing database...")
            sys.exit()