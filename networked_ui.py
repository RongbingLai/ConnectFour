# Name: Rongbing Lai 
# Student ID: 69071949

from general_ui import *
from socket_handling import *

#HOST = 'circinus-32.ics.uci.edu'
#PORT = 4444

def main() -> None:
    '''
    runs the online version of connect four user interface
    '''
    # connects to the connect 4 server, if 
    # the it cannot connect to the server then 
    # print the error message
    print("Please enter the host and the port of Connect Four Server")
    try:
        host = input("Host:")
        port = int(input("Port:"))
        connection = connect(host, port)
    except:
        print("ERROR: cannot connect to the server")
        return

    # connects to the server and show welcome banner
    # gets the name and the board size and print the
    # board
    welcome_banner()
    while True:
        name, columns, rows = initialize_input()
        state = create_board(columns, rows)
        if state == None:
            continue
        break

    try:
        network_initialize(connection, name, columns, rows)
    # avoids the situation where the client successfully 
    # connects to a server that is not Connect Four server
    except:
        print("ERROR: protocol error")
        close(connection)
        return

    # the client and the server plays the game until 
    # the game is over
    while True:
        success, state = client_move(connection, state)
        if not success:
            break
        success, state = server_move(connection, state)
        if not success:
            break

    # closes the connection and show the game over banner
    close(connection)
    game_over_banner(state)
    
def network_initialize(connection: Connect4Connection, name: str, columns: int, rows: int) -> None:
    '''
    sends the player's name, columns and rows to the server
    '''
    hello(connection, name)
    request_game(connection, columns, rows)

def network_good_progress(connection: Connect4Connection, response: str) -> bool:
    '''
    checks the server's response to see if 
    the move of client is invalid 
    '''
    if response != "INVALID":
        return True
    if server_status(connection) == "READY":
        return False
    raise Connect4ProtocolError()

def game_over(response: str) -> bool:
    '''
    checks if the game is over (has a winner)
    '''
    if response.startswith("WINNER_"):
        return True
    else:
        return False

def client_move(connection: Connect4Connection, state: GameState) -> 'move_status':
    '''
    gets the client player's move and sends it to the server.
    If the server responses correct protocol and the local also
    does not catch invalid input, then update the
    client's move in the state and prints the state
    '''
    while True:
        try:
            action, column_num = make_move_command(state)
            if action == "drop":
                response = client_drop(connection, column_num+1)
                if network_good_progress(connection, response):
                    state = drop_command(state, column_num)
                else:
                    print("------------------------------—--------------")
                    print("ERROR: action is invalid. Please try again.")
                    continue
            elif action == "pop":
                response = client_pop(connection, column_num+1)
                if network_good_progress(connection, response):
                    state = pop_command(state, column_num)
                else:
                    print("------------------------------—--------------")
                    print("ERROR: action is invalid. Please try again.")
                    continue
            # to check if the game is over
            if game_over(response):
                return False, state
            else:
                break
        except Connect4ProtocolError:
            print("------------------------------—--------------")
            print("ERROR: protocol error")
            return False, state
        # the server's response is incorrect according to the protocol
        except InvalidMoveError:
            print("------------------------------—--------------")
            print("ERROR: the server has conflict with the client")
            return False, state

    return True, state

def server_move(connection: Connect4Connection, state: GameState) -> 'move_status':
    '''
    gets the server's move. If the move is valid,
    updates the server's move in the local state;
    else stop the game by returning False
    '''
    try:
        response = server_status(connection).split()
        column_num =  int(response[1])-1
        if response[0] == "DROP":
            state = drop_command(state, column_num)
        elif response[0] == "POP":
            state = pop_command(state, column_num)
        else:
            raise ValueError()
        # the final response should be READY
        response = server_status(connection)
        if response != "READY":
            return False, state
    except:
        return False, state

    return True, state

if __name__ == "__main__":
    main()