import random

score = 0
choices = ["rock", "paper", "scissors"]

print("Let's play Rock, Paper, Scissors!")
player = input("Choose rock, paper, or scissors: ").strip().lower()

if player not in choices:
    print("Invalid choice! Please choose rock, paper, or scissors.")
else:
    computer = random.choice(choices)
    print("You chose:", player)
    print("The computer chose:", computer)

    if player == computer:
        print("It's a tie!")
    elif (
        (player == "rock" and computer == "scissors")
        or (player == "paper" and computer == "rock")
        or (player == "scissors" and computer == "paper")
    ):
        print("You win! Congratulations!")
        score += 1
    else:
        print("You lose! Better luck next time.")

print("Your score is:", score)
import tkinter as tk
# button = you click it, then it does stuff
def click():
    print("reset the score!")

window = tk.Tk()
button = tk.Button(
    window,
    text="Reset Score",
    command=click,
    font=("Comic Sans MS", 55, "bold"),
    fg="red",
    bg="black",
)
button.pack()

window.mainloop()


import tkinter #tk-interface (graphical user interface libary)

def set_tile(row, column):
    global curr_player
    button = board[row][column]
    if button["text"]:
        return

    button.config(
        text=curr_player,
        foreground=color_blue if curr_player == playerX else color_yellow,
    )
    curr_player = playerO if curr_player == playerX else playerX
    label.config(text=curr_player + "'s turn")

#game stepup
playerX="x"
playerO="o"
curr_player=playerX
board=[[0,0,0],
       [0,0,0],
       [0,0,0]]

color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"

#window setup
window = tkinter.Tk() #create the game window
window.title("Tic Tac Toe")
window.resizable(False,False)

frame= tkinter.Frame(window)
label= tkinter.Label(frame,text=curr_player+"'s turn", font=("consolas",20), background=color_gray,
                     foreground="white")
label.grid(row=0,column=0)
for row in range(3):
    for column in range(3):
        board[row][column]=tkinter.Button(
            frame,
            text="",
            font=("consolas",50,"bold"),
            background=color_gray,
            foreground=color_blue,
            width=4,
            height=1,
            command=lambda row=row,column=column: set_tile(row,column),
        )
        board[row][column].grid(row=row+1,column=column)
frame.pack()
window.mainloop()