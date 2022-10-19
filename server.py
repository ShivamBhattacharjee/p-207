import socket
import time
from  threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None
playerNames=[]
CLIENTS = {}



def handleClient(player_socket,player_name):
    global CLIENTS
    global playerNames

    # Sending Initial message
    playerType =CLIENTS[player_name]["player_type"]
    if(playerType== 'player1'):
        CLIENTS[player_name]['turn'] = True
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'] }).encode())
    else:
        CLIENTS[player_name]['turn'] = False
        player_socket.send(str({'player_type' : CLIENTS[player_name]["player_type"] , 'turn': CLIENTS[player_name]['turn'] }).encode())

    playerNames.append({"name": player_name, "type": CLIENTS[player_name]["player_type"]})

    time.sleep(2)
    if(len(playerNames) > 0 and len(playerNames) <= 2):
        for cName in CLIENTS:
            cSocket = CLIENTS[cName]["player_socket"]
            cSocket.send(str({"player_names" : playerNames}).encode("utf-8"))

    while True:
        try:
            message = player_socket.recv(2048)
            if(message):
                for cName in CLIENTS:
                    cSocket = CLIENTS[cName]["player_socket"]
                    cSocket.send(message)
        except:
            pass


def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name=player_socket.recv(2048).decode("utf-8")
        
        if (len(CLIENTS.keys())==0):
            CLIENTS[player_name]={"player_type":"player 1"}
        else:
            CLIENTS[player_name]={"player_type":"player 2"}

        CLIENTS[player_name]["player_socket"]=player_socket
        CLIENTS[player_name]["address"]=addr
        CLIENTS[player_name]["player_name"]=player_name
        CLIENTS[player_name]["turn"]=False

        print(CLIENTS)
        print(f"connection established with {player_name}:{addr}")
        thread = Thread(target = handleClient, args=(player_socket,player_name,))
        thread.start()

def setup():
    print("\n")
    print("\t\t\t\t\t\t*** LUDO LADDER ***")


    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup()
