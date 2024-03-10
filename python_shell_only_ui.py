# Name: Rongbing Lai 
# Student ID: 69071949

from connectfour import *
from general_ui import *

def main():
    welcome_banner()
    while True:
        name, columns, rows = initialize_input()    
        state = create_board(columns, rows)
        if state == None:
            continue
        break
    while True:
        try:
            action, column_num = make_move_command(state)
            if action == "drop":
                state = drop_command(state, column_num)
            elif action == "pop":
                state = pop_command(state, column_num)
            if winner(state) != EMPTY:
                break
        except InvalidMoveError:
            print("------------------------------")
            print("ERROR: this move is invalid. Try another one.")
            continue
        except GameOverError:
            print("------------------------------")
            print("ERROR: the game is over.")
            break

    game_over_banner(state)

if __name__ == "__main__":
    main()
