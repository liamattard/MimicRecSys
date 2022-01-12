from simple_term_menu import TerminalMenu
import Data_Processing.process


def main():
    options = ["Create Data Frame", "Clean Data", "exit"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    if(options[menu_entry_index] == options[0]):
        Data_Processing.process.start()

    if(options[menu_entry_index] == options[1]):
        Data_Processing.process.clean()

    if(options[menu_entry_index] == options[2]):
        exit()


if __name__ == "__main__":
    main()