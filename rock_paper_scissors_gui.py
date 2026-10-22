import tkinter as tk
from tkinter import messagebox
import random

window = tk.Tk()
window.title("Choose a Game")
window.geometry("360x240")
window.configure(bg="#1e1e2f")
window.resizable(False, False)

menu_frame = tk.Frame(window, bg="#1e1e2f")
menu_frame.pack(fill="both", expand=True)

game_frame = tk.Frame(window, bg="#1e1e2f")
tk.Label(
    menu_frame,
    text="Choose a game",
    font=("Arial", 20, "bold"),
    bg="#1e1e2f",
    fg="white",
).pack(pady=25)

def show_rock_paper_scissors():
    menu_frame.pack_forget()
    window.title("Rock Paper Scissors")
    window.geometry("420x460")
    game_frame.pack(fill="both", expand=True)

def show_game_menu():
    game_frame.pack_forget()
    window.title("choose a game")
    window.geometry("360x240")
    menu_frame.pack(fill="both", expand=True)

label = tk.Label(
    game_frame,
    text="First to 5 wins!\nChoose rock, paper, or scissors:",
    font=("Arial", 18, "bold"),
    bg="#1e1e2f",
    fg="white",
    pady=20,
)
label.pack()

result_label = tk.Label(
    game_frame,
    text="",
    font=("Arial", 14),
    bg="#1e1e2f",
    fg="white",
    wraplength=380,
    pady=12,
)
result_label.pack()

score = {"wins": 0, "losses": 0, "ties": 0}
game_over = False
score_label = tk.Label(
    game_frame,
    text="Score — You: 0 | Computer: 0 | Ties: 0",
    font=("Arial", 14, "bold"),
    bg="#1e1e2f",
    fg="white",
    pady=12,
)
score_label.pack()


def play(player_choice):
    global game_over
    if game_over:
        return

    computer_choice = random.choice(["rock", "paper", "scissors"])
    if player_choice == computer_choice:
        outcome = "It's a tie!"
        score["ties"] += 1
    elif (
        (player_choice == "rock" and computer_choice == "scissors")
        or (player_choice == "paper" and computer_choice == "rock")
        or (player_choice == "scissors" and computer_choice == "paper")
    ):
        outcome = "You win!"
        score["wins"] += 1
    else:
        outcome = "The computer wins!"
        score["losses"] += 1

    result_text = (
        f"You chose {player_choice}. The computer chose {computer_choice}.\n"
        f"{outcome}"
    )
    if score["wins"] >= 5:
        result_text += "\nYou reached 5 wins! You won the game."
        game_over = True
    elif score["losses"] >= 5:
        result_text += "\nThe computer reached 5 wins. Game over."
        game_over = True

    result_label.config(text=result_text)
    score_label.config(
        text=f"Score — You: {score['wins']} | Computer: {score['losses']} | "
        f"Ties: {score['ties']}"
    )
    if game_over:
        play_again_button.pack(before=reset_button, pady=8)


def start_new_game():
    global game_over
    score["wins"] = 0
    score["losses"] = 0
    score["ties"] = 0
    game_over = False
    result_label.config(text="")
    score_label.config(text="Score — You: 0 | Computer: 0 | Ties: 0")
    play_again_button.pack_forget()


def reset_score():
    confirmed = messagebox.askyesno(
        "Reset score", "Are you sure you want to reset the score?"
    )
    if confirmed:
        start_new_game()


def open_tic_tac_toe():
    game_window = tk.Toplevel(window)
    game_window.title("Tic Tac Toe")
    game_window.geometry("400x400")
    game_window.configure(bg="#1e1e2f")

    tk.Label(
        game_window,
        text="Tic Tac Toe",
        font=("Arial", 18, "bold"),
        bg="#1e1e2f",
        fg="white",
    ).pack(pady=20)
    tk.Label(
        game_window,
        text="Your Tic Tac Toe game will go here.",
        font=("Arial", 12),
        bg="#1e1e2f",
        fg="white",
    ).pack(pady=10)

    tk.Button(
        game_window,
        text="Back to Main Menu",
        command=game_window.destroy,
    ).pack(pady=10)

tk.Button(
    menu_frame,
    text="Rock Paper Scissors",
    command=show_rock_paper_scissors,
    font=("Arial", 14),
    width=22,
).pack(pady=5)
for choice in ["rock", "paper", "scissors"]:
    tk.Button(
        game_frame,
        text=choice.title(),
        command=lambda picked=choice: play(picked),
        font=("Arial", 12),
        width=12,
    ).pack(pady=3)

tic_tac_toe_button = tk.Button(
    menu_frame,
    text="Tic Tac Toe",
    command=open_tic_tac_toe,
    font=("Arial", 14),
    width=22,
)
tic_tac_toe_button.pack(pady=5)

play_again_button = tk.Button(
    game_frame, text="Play Again", command=start_new_game, font=("Arial", 12, "bold")
)
reset_button = tk.Button(game_frame, text="Reset Score", command=reset_score)
reset_button.pack(pady=8)
tk.Button(
    game_frame,
    text="Back to Main Menu",
    command=show_game_menu,
).pack(pady=5)
tk.Label(
    game_frame,
    text="Thanks for playing! Hope you had fun!",
    bg="#1e1e2f",
    fg="white",
).pack()
window.mainloop()

import turtle

turtle.speed(250)
turtle.bgcolor("black")
turtle.pensize(3)


def draw_heart():
    for _ in range(200):
        turtle.right(1)
        turtle.forward(1)


turtle.color("red", "pink")
turtle.begin_fill()
turtle.left(140)
draw_heart()
turtle.left(120)
draw_heart()
turtle.forward(111.65)
turtle.end_fill()
turtle.hideturtle()
turtle.done()
