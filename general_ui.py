# Name: Rongbing Lai 
# Student ID: 69071949

from connectfour import *
from collections import namedtuple

def create_board(columns: int, rows: int) -> GameState:
    '''
    creates a new board with given columns and rows
    '''
    while True:
        try:
            state = new_game(columns, rows)
            _print_board(state)
            break
        except ValueError:
            print("ERROR: The columns and rows must be an int between 1 and 20.")
            return None
    return state

def welcome_banner() -> None:
    '''
    shows the welcome banner
    '''
    print("------------------------------—--------------")
    print("Welcome to Connect Four Game!")
    print("------------------------------—--------------")
    print("In this game, 'R' represents RED's piece and ")
    print("'Y' represents YELLOW's piece. RED plays first")
    print("------------------------------—--------------")
    print("Please enter your name and the size of the")
    print("board follow the format: name columns rows")
    print("EXAMPLE: Boo 7 6")
    print("NOTE: The maximum columns and rows are 20")
    print("and your name should not contain spaces")
    print("------------------------------—--------------")
    

def initialize_input() -> 'command':
    '''
    gets the player's name and the size of the board
    '''
    while True:
        try:
            command = input().split()
            name = command[0]
            columns = int(command[1])
            rows = int(command[2])
        except:
            print("------------------------------—--------------")
            print("ERROR: The name format or size format is invalid.")
            print("Try again.")
            continue
        return name, columns, rows

def make_move_command(state: GameState) -> 'move_command':
    '''
    asks the player to drop or pop
    '''
    while True:
        print("------------------------------—--------------")
        print(f"{_transform_char(state.turn)}'s turn")
        print(f"Enter the column number (1 to {columns(state)})")
        print("that you want to move.")
        print("You can either drop or pop a piece.")
        print("------------------------------—--------------")
        print("column number: ")
        try:
            column_num = int(input()) - 1
        except ValueError:
            print("------------------------------—--------------")
            print("ERROR: the column number is invalid. Try another one.")
            continue
        print("drop or pop: ")
        action = input()
        if action != 'drop' and action != 'pop':
            print("------------------------------—--------------")
            print("ERROR: action is invalid. Please try again.")
            continue
        break

    return action, column_num

def drop_command(state: GameState, column_num: int) -> GameState:
    '''
    drops a piece in the state in the given column
    and prints the board
    '''
    state = drop(state, column_num)
    _print_board(state)

    return state

def pop_command(state: GameState, column_num: int) -> GameState:
    '''
    pops a piece in the state in the givn column
    and prints the board
    '''
    state = pop(state, column_num)
    _print_board(state)

    return state

def game_over_banner(state: GameState) -> None:
    '''
    shows the game over banner if the game is over,
    else if the game ends unexpectedly, it shows the
    error message
    '''
    if winner(state) == EMPTY:
        print("ERROR: game error")
        return
    print("------------------------------—--------------")
    print(f"The winner is {_transform_char(winner(state))}.")
    print()
    print("GAME OVER")
    print("------------------------------—--------------")

def _print_board(state: GameState) -> GameState:
    '''
    prints the board 
    '''
    # prints the number of columns
    for col in range(columns(state)):
        if col == columns(state) - 1:
            print(col+1)
        elif col >= 8:
            print(col+1, end = " ")
        else:
            print(col+1, end = "  ")
    
    # prints the 'grids'
    for row in range(rows(state)):
        for col in range(columns(state)):
            if col == columns(state) - 1:
                print(_transform_char(state.board[col][row]))
            else:
                print(_transform_char(state.board[col][row]), end = "  ")
    
    return state

def _transform_char(num: int) -> str:
    '''
    transform numbers EMPTY, RED, YELLOW into '.', 'R', 'Y'
    '''
    if num == RED:
        return 'R'
    elif num == YELLOW:
        return 'Y'
    
    return '.'