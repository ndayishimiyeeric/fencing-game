import os

if __name__ == '__main__':
    user_input = input(
        'Do you want to run the terminal or graphic version? (t/g) ').lower()
    if user_input == 't' or user_input == 'g':
        # run the terminal version
        if user_input == 't':
            if os.name == 'posix':
                os.system('python3 terminal.py')
            if os.name == 'nt':
                os.system('python terminal.py')
        # run the graphic version
        else:
            if os.name == 'posix':
                os.system('python3 graphic.py')
            if os.name == 'nt':
                os.system('python graphic.py')
    else:
        print('Invalid input :) run the program again and type t or g')
