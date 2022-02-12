import Data_Processing.process
import Data_Processing.sparse_matrix
# from simple_term_menu import TerminalMenu


def main():
    # options = ["Create Data Frame", "Create Sparse Matrix", "exit"]
    # terminal_menu = TerminalMenu(options)
    # menu_entry_index = int(terminal_menu.show())  # type: ignore

    # if options[menu_entry_index] == options[0]:
    # Data_Processing.process.start()

    # if options[menu_entry_index] == options[1]:
    Data_Processing.sparse_matrix.start()

    # if options[menu_entry_index] == options[2]:
    # exit()


if __name__ == "__main__":
    main()
