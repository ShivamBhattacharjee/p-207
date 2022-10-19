import socket
from tkinter import *
from threading import Thread
from PIL import ImageTk, Image
import random

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None


canvas1 = None
canvas2 = None

playerName = None
nameEntry = None
nameWindow = None
gamewindow = None

rollButton = None

player1Name = 'joining'
player2Name = 'joining'

player1Label = None
player2Label = None

player1Score = 0
player2Score = 0

player1ScoreLabel = None
player2ScoreLabel = None

dice = None

playerType = None
playerTurn = None

leftBoxes = []
rightBoxes = []
finishBoxes = None
resetButton = None
winning_msg = None
reset = None
winingFunctionCall = 0


# Teacher write code here for askPlayerName()


def checkColorBoxPosition(boxes, color):
    for i in boxes:
        boxColor = i.cget("bg")
        if boxColor == color:
            return boxes.index(i)
    return False


def movePlayer1(steps):
    global leftBoxes
    boxPosition = checkColorBoxPosition(leftBoxes[1:], "red")
    if boxPosition:
        diceValue = steps
        coloredBoxIndex = boxPosition
        total_steps = 10
        remaining_steps = total_steps-coloredBoxIndex
        if steps == remaining_steps:
            for i in leftBoxes[1:]:
                i.configure(bg="white")
            global finishBoxes
            finishBoxes.configure(bg="red")
            global SERVER
            global playerName
            greet_msg = f"red wins the game"
            SERVER.send(greet_msg.encode("utf-8"))
        elif steps < remaining_steps:
            for i in leftBoxes[1:]:
                i.configure(bg="white")
            next_step = (coloredBoxIndex+1)+diceValue
            leftBoxes[next_step].configure(bg="red")
        else:
            print("No move")
    else:
        leftBoxes[steps].configure(bg="red")


def movePlayer2(steps):
    global rightBoxes
    reverse_boxes = rightBoxes[-2::-1]
    boxPosition = checkColorBoxPosition(reverse_boxes, "green")
    if boxPosition:
        diceValue = steps
        coloredBoxIndex = boxPosition
        total_steps = 10
        remaining_steps = total_steps-coloredBoxIndex
        if steps == remaining_steps:
            for i in rightBoxes[-2::-1]:
                i.configure(bg="white")
            global finishBoxes
            finishBoxes.configure(bg="green")
            global SERVER
            global playerName
            greet_msg = f"green wins the game"
            SERVER.send(greet_msg.encode("utf-8"))
        elif steps < remaining_steps:
            for i in rightBoxes[-2::-1]:
                i.configure(bg="white")
            next_step = (coloredBoxIndex+1)+diceValue
            rightBoxes[::-1][next_step].configure(bg="green")
        else:
            print("No move")
    else:
        rightBoxes[len(rightBoxes)-(steps+1)].configure(bg="green")


def rollingButton():
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    diceFace = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
    value = random.choice(diceFace)
    print(value)
    rollButton.destroy()
    playerTurn = False
    if playerType == "player1":
        SERVER.send(f"{value}player2Turn".encode("utf-8"))
    elif playerType == "player2":
        SERVER.send(f"{value}player1Turn".encode("utf-8"))


def leftBoard():
    global gamewindow
    global leftBoxes
    global screen_width
    global screen_height
    x1 = 10
    for i in range(0, 11):
        if i == 0:
            box_label = Label(gamewindow, width=1, height=1,
                              borderwidth=2, bg="red", font=("Chalkboard SE", 30))
            box_label.place(x=x1, y=screen_height/2-30)
            leftBoxes.append(box_label)
            x1 += 30
        else:
            box_label = Label(gamewindow, width=1, height=1,
                              borderwidth=2, bg="white", font=("Chalkboard SE", 30))
            box_label.place(x=x1, y=screen_height/2-30)
            leftBoxes.append(box_label)
            x1 += 50


def rightBoard():
    global gamewindow
    global rightBoxes
    global screen_width
    global screen_height
    x2 = 748
    for i in range(0, 11):
        if i == 10:
            box_label = Label(gamewindow, width=1, height=1,
                              borderwidth=2, bg="green", font=("Chalkboard SE", 30))
            box_label.place(x=x2, y=screen_height/2-30)
            rightBoxes.append(box_label)
            x2 += 30
        else:
            box_label = Label(gamewindow, width=1, height=1,
                              borderwidth=2, bg="white", font=("Chalkboard SE", 30))
            box_label.place(x=x2, y=screen_height/2-30)
            rightBoxes.append(box_label)
            x2 += 50


def finishLine():
    global gamewindow
    global finishBoxes
    global screen_width
    global screen_height
    finishBoxes = Label(gamewindow, width=8, height=4, text="HOME",
                        bg="brown", fg="white", font=("Chalkboard SE", 30))
    finishBoxes.place(x=screen_width/2-100, y=screen_height/2-100)


def playWindow():
    global SERVER
    global gamewindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global rollButton
    global playerName
    global playerType
    global playerTurn
    global winning_msg
    global reset
    global player1Label
    global player2Label
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel

    gamewindow = Tk()
    gamewindow.title("Ludo game")
    gamewindow.attributes("-fullscreen", True)

    screen_width = gamewindow.winfo_screenwidth()
    screen_height = gamewindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="assets/background.png")

    canvas2 = Canvas(gamewindow, width=screen_width, height=500)
    canvas2.pack(fill="both", expand=True)

    canvas2.create_image(0, 0, image=bg, anchor="nw")
    canvas2.create_text(screen_width/2, screen_height/5,
                        text="Ludo game", font=("Chalkboard SE", 100), fill="white")
    winning_msg = canvas2.create_text(
        screen_width/2+10, screen_height/2+250, font=("Chalkboard SE", 100), fill="white", text=" ")
    reset = Button(gamewindow, text="reset game", fg="black", width=20,
                   height=5, font=("Chalkboard SE", 100), bg="grey", command=resetGame)

    leftBoard()
    rightBoard()
    finishLine()

    rollButton = Button(gamewindow, text="Roll the dice", bg="lightcyan", fg="black", font=(
        "monospace", 15), width=20, height=2, command=rollingButton)
    # rollButton.place(x=screen_width/2-120, y=screen_height/2+280)
    if (playerType == "player1" and playerTurn):
        rollButton.place(x=screen_width/2-80, y=screen_height/2+250)
    else:
        rollButton.pack_forget()

    dice = canvas2.create_text(screen_width/2-10, screen_height /
                               2+185, text="\u2680", font=("monospace", 200), fill="white")

    player1Label = canvas2.create_text(400, screen_height/2+100, text=player1Name, font=("monospace", 15), fill="white")
    player2Label = canvas2.create_text(screen_width-400, screen_height/2+100, text=player2Name, font=("monospace", 15), fill="white")

    player1ScoreLabel = canvas2.create_text(400, screen_height/2-160, font=("monospace", 15), fill="white", text=player1Score)
    player2ScoreLabel = canvas2.create_text(screen_width-400, screen_height/2-160, text=player2Score, font=("monospace", 15), fill="white")

    gamewindow.resizable(True, True)

    gamewindow.mainloop()


def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()
    playWindow()
    SERVER.send(playerName.encode("utf-8"))


def askPlayerName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    nameWindow = Tk()
    nameWindow.title("Ludo ladder game")
    nameWindow.attributes('-fullscreen', True)

    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file="assets/background.png")

    canvas1 = Canvas(nameWindow, width=500, height=500)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(screen_width/2, screen_height/5,
                        text="Ludo Ladder Game", font=("Chalkboard SE", 100), fill="white")

    nameEntry = Entry(nameWindow, width=10, justify="center",
                      font=("Chalkboard SE", 100), bg="white")
    nameEntry.place(x=screen_width/2-370, y=screen_height/4+100)

    button = Button(nameWindow, text="save", font=(
        "Chalkboard SE", 40), bg="grey", bd=3, width=5, command=saveName)
    button.place(x=screen_width/2-120, y=screen_height/2+100)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


def resetGame():
    global SERVER
    SERVER.send("reset game".encode())


def handleWin(message):
    global playerType
    global rollButton
    global canvas2
    global winning_msg
    global screen_width
    global screen_height
    global resetButton

    # destroying button
    if ('Red' in message):
        if (playerType == 'player2'):
            rollButton.destroy()

    if ('Yellow' in message):
        if (playerType == 'player1'):
            rollButton.destroy()

    # Adding Wining Message
    message = message.split(".")[0] + "."
    canvas2.itemconfigure(winning_msg, text=message)

    # Placing Reset Button
    resetButton.place(x=screen_width / 2 - 80, y=screen_height - 220)


def updateScore(message):
    global canvas2
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel

    if ('Red' in message):
        player1Score += 1

    if ('Yellow' in message):
        player2Score += 1

    canvas2.itemconfigure(player1ScoreLabel, text=player1Score)
    canvas2.itemconfigure(player2ScoreLabel, text=player2Score)


def handleResetGame():
    global canvas2
    global playerType
    global gamewindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global rightBoxes
    global leftBoxes
    global finishBoxes
    global resetButton
    global winning_msg
    global winingFunctionCall

    canvas2.itemconfigure(dice, text='\u2680')

    # Handling Reset Game
    if (playerType == 'player1'):
        # Creating roll dice button
        rollButton = Button(gamewindow, text="Roll Dice", fg='black', font=(
            "Chalkboard SE", 15), bg="grey", command=rollingButton, width=20, height=5)
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2 + 250)
        playerTurn = True

    if (playerType == 'player2'):
        playerTurn = False

    for rBox in rightBoxes[-2::-1]:
        rBox.configure(bg='white')

    for lBox in leftBoxes[1:]:
        lBox.configure(bg='white')

    finishBoxes.configure(bg='green')
    canvas2.itemconfigure(winning_msg, text="")
    resetButton.destroy()

    # Again Recreating Reset Button for next game
    resetButton = Button(gamewindow, text="Reset Game", fg='black', font=(
        "Chalkboard SE", 15), bg="grey", command=resetGame, width=20, height=5)
    winingFunctionCall = 0


def recivedMsg():
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gamewindow
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global winingFunctionCall

    while True:
        message = SERVER.recv(2048).decode()

        if ('player_type' in message):
            recvMsg = eval(message)
            playerType = recvMsg['player_type']
            playerTurn = recvMsg['turn']
        elif ('player_names' in message):

            players = eval(message)
            players = players["player_names"]
            for p in players:
                if (p["type"] == 'player1'):
                    player1Name = p['name']
                if (p['type'] == 'player2'):
                    player2Name = p['name']

        elif ('⚀' in message):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif ('⚁' in message):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif ('⚂' in message):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif ('⚃' in message):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif ('⚄' in message):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif ('⚅' in message):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')

        elif ('wins the game.' in message and winingFunctionCall == 0):
            winingFunctionCall += 1
            handleWin(message)
            # Addition Activity
            updateScore(message)
        elif (message == 'reset game'):
            handleResetGame()

        # creating rollbutton
        if ('player1Turn' in message and playerType == 'player1'):
            playerTurn = True
            rollButton = Button(gamewindow, text="Roll Dice", fg='black', font=(
                "Chalkboard SE", 15), bg="grey", command=rollingButton, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2 + 250)

        elif ('player2Turn' in message and playerType == 'player2'):
            playerTurn = True
            rollButton = Button(gamewindow, text="Roll Dice", fg='black', font=(
                "Chalkboard SE", 15), bg="grey", command=rollingButton, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2 + 260)

        # Creating Name Board
        if (player1Name != 'joining' and canvas2):
            canvas2.itemconfigure(player1Label, text=player1Name)

        if (player2Name != 'joining' and canvas2):
            canvas2.itemconfigure(player2Label, text=player2Name)


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    # Creating First Window
    askPlayerName()


setup()
