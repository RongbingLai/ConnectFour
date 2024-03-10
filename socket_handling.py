# Name: Rongbing Lai 
# Student ID: 69071949

from connectfour import *
from collections import namedtuple
import socket

Connect4Connection = namedtuple(
    'Connect4Connection', 
    ['socket', 'input','output'])

DEBUG = False

class Connect4ProtocolError(Exception):
    pass

def connect(host: str, port: int) -> Connect4Connection:
    '''
    connects to the server
    '''
    connect4_socket = socket.socket()
    connect4_socket.connect((host, port))

    connect4_input = connect4_socket.makefile('r')
    connect4_output = connect4_socket.makefile('w')

    return Connect4Connection(
        socket = connect4_socket, 
        input = connect4_input, 
        output = connect4_output)

def hello(connection: Connect4Connection, username: str) -> None:
    '''
    sends hello message to the server with the
    name of the user
    '''
    _protocol_check(connection, f'I32CFSP_HELLO {username}', f'WELCOME {username}')


def request_game(connection: Connect4Connection, columns: int, rows: int) -> None:
    '''
    sends request to the server with the columns and rows
    of the board.
    '''
    _protocol_check(connection, f'AI_GAME {columns} {rows}', 'READY')

def client_drop(connection: Connect4Connection, column_num: int) -> str:
    '''
    sends a drop message to the server to drop
    a piece with the given column number. Return 
    the response from the server
    '''
    return _protocol_check(connection, f"DROP {column_num}", None)
    

def client_pop(connection: Connect4Connection, column_num: int) -> str:
    '''
    sends a pop message to the server to pop
    a piece with the given column number. Return 
    the response from the server
    '''
    return _protocol_check(connection, f"POP {column_num}", None)

def server_status(connection: Connect4Connection) -> str:
    '''
    reads a message from the server
    '''
    return _read_line(connection)

def close(connection: Connect4Connection) -> None:
    '''
    closes all the connections to the server
    '''
    connection.input.close()
    connection.output.close()
    connection.socket.close()

def _protocol_check(connection: Connect4Connection, send: str, expect: str) -> str:
    '''
    writes a protocol and stores a response. 
    checks if the protocol is valid. If the protocol
    is valid, return the response; else raise the protocol
    error. The expect value if None when the expected message
    has more than one possible value
    '''
    _write_line(connection, send)
    response = _read_line(connection)
    if expect == None or response == expect:
        return response
    else:
        raise Connect4ProtocolError()

def _read_line(connection: Connect4Connection) -> str:
    '''
    reads a line from the server
    '''
    line = connection.input.readline()[:-1]
    if DEBUG:
        print("<- ",line)
    return line

def _write_line(connection: Connect4Connection, line: str) -> None:
    '''
    writes a line to the server
    '''
    connection.output.write(line + '\r\n')
    connection.output.flush()
    if DEBUG:
        print("-> ",line)
