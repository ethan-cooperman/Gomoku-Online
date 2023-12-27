import socket
import _thread
import pickle
from game import *
import bz2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "IP ADDRESS HERE"
port = 5555
print(server)
try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print('Server started. Waiting for a connection.')

connected = set()
games = {}
id_count = 0


def threaded_client(conn, p, game_id):
    """creates a new thread for each client

    :param conn: the socket connection
    :param p: the player number
    :param game_id: the game id on the current thread
    """
    global id_count
    conn.sendall(pickle.dumps(p))
    while True:
        try:
            data = pickle.loads(conn.recv(2 ** 30))

            if game_id in games:
                game = games[game_id]

                if not data:
                    print('No data received')
                    break
                else:
                    if data == 'reset':
                        game.reset()
                    elif data != 'get' and game.turn == p:
                        game.make_move(data[0], data[1])
                    conn.sendall(bz2.compress(pickle.dumps(game)))
            else:
                break
        except Exception as e:
            print(e)
            break

    try:
        del games[game_id]
        print(f'Closing game {game_id} due to lost connection')
    except Exception as e:
        print(e)
    id_count -= 1
    conn.close()


while True:
    conn, address = s.accept()
    print('Connected to', address)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print('Creating a new game...')
    else:
        games[game_id].connected = True
        p = 1

    _thread.start_new_thread(threaded_client, (conn, p, game_id))
