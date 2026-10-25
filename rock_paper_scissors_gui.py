import tkinter as tk
from tkinter import messagebox
import random
import time

from hangman import display_hangman, get_word

window = tk.Tk()
window.title("Choose a Game")
window.geometry("420x470")
window.configure(bg="#1e1e2f")
window.resizable(False, False)

menu_frame = tk.Frame(window, bg="#1e1e2f")
menu_frame.pack(fill="both", expand=True)

game_frame = tk.Frame(window, bg="#1e1e2f")
tic_tac_toe_frame = tk.Frame(window, bg="#1e1e2f")
hangman_frame = tk.Frame(window, bg="#1e1e2f")
reaction_time_frame = tk.Frame(window, bg="#1e1e2f")
pong_frame = tk.Frame(window, bg="#1e1e2f")
thank_you_frame = tk.Frame(window, bg="#1e1e2f")

hangman_word = ""
hangman_guessed_letters = set()
hangman_guessed_words = set()
hangman_tries = 6
hangman_finished = False
REACTION_MIN_DELAY_MS = 1500
REACTION_MAX_DELAY_MS = 3500
reaction_state = "idle"
reaction_after_id = None
reaction_started_at = None
welcome_message = "Welcome to the game chooser menu!"
DEFAULT_MENU_COLOR = "#1e1e2f"
ALTERNATE_MENU_COLOR = "lightblue"


menu_title_label = tk.Label(
    menu_frame,
    text="Choose a game",
    font=("Arial", 20, "bold"),
    bg="#1e1e2f",
    fg="white",
)
menu_title_label.pack(pady=(20, 8))
welcome_label = tk.Label(
    menu_frame,
    text="",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="white",
)
welcome_label.pack(pady=(0, 10))


def show_rock_paper_scissors():
    menu_frame.pack_forget()
    window.title("Rock Paper Scissors")
    window.geometry("420x460")
    game_frame.pack(fill="both", expand=True)


def show_hangman():
    menu_frame.pack_forget()
    window.title("Hangman")
    window.geometry("440x580")
    reset_hangman_game()
    hangman_frame.pack(fill="both", expand=True)


def show_reaction_time():
    menu_frame.pack_forget()
    window.title("Reaction Time")
    window.geometry("440x360")
    reset_reaction_test()
    reaction_time_frame.pack(fill="both", expand=True)


def show_pong_game():
    menu_frame.pack_forget()
    window.title("Pong")
    window.geometry("680x460")
    pong_game.restart()
    pong_frame.pack(fill="both", expand=True)
    pong_game.start()
    pong_game.canvas.focus_set()


def type_text(index=0):
    welcome_label.config(text=welcome_message[:index])
    if index < len(welcome_message):
        window.after(80, type_text, index + 1)


def change_color():
    menu_color = (
        ALTERNATE_MENU_COLOR
        if menu_frame.cget("bg") == DEFAULT_MENU_COLOR
        else DEFAULT_MENU_COLOR
    )
    text_color = "#1e1e2f" if menu_color == ALTERNATE_MENU_COLOR else "white"
    window.configure(bg=menu_color)
    menu_frame.configure(bg=menu_color)
    menu_title_label.configure(bg=menu_color, fg=text_color)
    welcome_label.configure(bg=menu_color, fg=text_color)


def show_game_menu():
    global reaction_after_id, reaction_state, snake_after_id
    game_frame.pack_forget()
    hangman_frame.pack_forget()
    reaction_time_frame.pack_forget()
    pong_frame.pack_forget()
    if "pong_game" in globals():
        pong_game.stop()
    if reaction_after_id is not None:
        window.after_cancel(reaction_after_id)
        reaction_after_id = None
    reaction_state = "idle"
    if "tic_tac_toe_window" in globals():
        tic_tac_toe_window.withdraw()
    if "snake_window" in globals():
        if snake_after_id is not None:
            snake_window.after_cancel(snake_after_id)
            snake_after_id = None
        snake_window.withdraw()
    window.deiconify()
    window.title("Choose a Game")
    window.geometry("420x470")
    menu_frame.pack(fill="both", expand=True)


def show_thank_you():
    global reaction_after_id, reaction_state, snake_after_id
    if "pong_game" in globals():
        pong_game.stop()
    if reaction_after_id is not None:
        window.after_cancel(reaction_after_id)
        reaction_after_id = None
    reaction_state = "idle"
    if "tic_tac_toe_window" in globals():
        tic_tac_toe_window.withdraw()
    if "snake_window" in globals():
        if snake_after_id is not None:
            snake_window.after_cancel(snake_after_id)
            snake_after_id = None
        snake_window.withdraw()

    for frame in (
        menu_frame,
        game_frame,
        hangman_frame,
        reaction_time_frame,
        pong_frame,
    ):
        frame.pack_forget()

    window.title("Thank You!")
    window.geometry("400x300")
    window.configure(bg="#1e1e2f")
    thank_you_frame.pack(fill="both", expand=True)
    window.protocol("WM_DELETE_WINDOW", window.destroy)


def reset_reaction_test():
    global reaction_after_id, reaction_started_at, reaction_state
    if reaction_after_id is not None:
        window.after_cancel(reaction_after_id)
        reaction_after_id = None
    reaction_state = "idle"
    reaction_started_at = None
    reaction_status_label.config(
        text="Click Start, then click again when the button turns green."
    )
    reaction_button.config(
        text="Start",
        command=start_reaction_test,
        bg="#646464",
        activebackground="#646464",
    )


def start_reaction_test():
    global reaction_after_id, reaction_state, reaction_started_at
    reaction_state = "waiting"
    reaction_started_at = None
    reaction_status_label.config(text="Wait for green...")
    reaction_button.config(
        text="Wait...",
        command=handle_reaction_click,
        bg="#b33a3a",
        activebackground="#b33a3a",
    )
    delay = random.randint(REACTION_MIN_DELAY_MS, REACTION_MAX_DELAY_MS)
    reaction_after_id = window.after(delay, show_reaction_signal)


def show_reaction_signal():
    global reaction_after_id, reaction_started_at, reaction_state
    reaction_after_id = None
    reaction_state = "go"
    reaction_started_at = time.perf_counter()
    reaction_status_label.config(text="Click now!")
    reaction_button.config(
        text="CLICK!",
        command=handle_reaction_click,
        bg="#39a852",
        activebackground="#39a852",
    )


def handle_reaction_click():
    global reaction_after_id, reaction_state, reaction_started_at
    if reaction_state == "waiting":
        if reaction_after_id is not None:
            window.after_cancel(reaction_after_id)
            reaction_after_id = None
        reaction_state = "idle"
        reaction_status_label.config(text="Too soon! Click Try again to restart.")
        reaction_button.config(
            text="Try again",
            command=start_reaction_test,
            bg="#646464",
            activebackground="#646464",
        )
    elif reaction_state == "go" and reaction_started_at is not None:
        reaction_time_ms = (time.perf_counter() - reaction_started_at) * 1000
        reaction_state = "idle"
        reaction_started_at = None
        reaction_status_label.config(
            text=f"Your reaction time: {reaction_time_ms:.0f} ms"
        )
        reaction_button.config(
            text="Try again",
            command=start_reaction_test,
            bg="#646464",
            activebackground="#646464",
        )


def update_hangman_display():
    hangman_drawing_label.config(text=display_hangman(hangman_tries))
    hangman_word_label.config(
        text=" ".join(
            letter if letter in hangman_guessed_letters else "_"
            for letter in hangman_word
        )
    )


def reset_hangman_game():
    global hangman_word, hangman_guessed_letters, hangman_guessed_words
    global hangman_tries, hangman_finished
    hangman_word = get_word()
    hangman_guessed_letters = set()
    hangman_guessed_words = set()
    hangman_tries = 6
    hangman_finished = False
    hangman_status_label.config(text="Guess a letter or the whole word.")
    hangman_entry.config(state="normal")
    hangman_guess_button.config(state="normal")
    hangman_entry.delete(0, tk.END)
    update_hangman_display()


def submit_hangman_guess(_event=None):
    global hangman_tries, hangman_finished
    if hangman_finished:
        return "break"

    guess = hangman_entry.get().strip().upper()
    hangman_entry.delete(0, tk.END)
    if not guess.isalpha():
        hangman_status_label.config(text="Enter letters only.")
        return "break"

    if len(guess) == 1:
        if guess in hangman_guessed_letters:
            hangman_status_label.config(text=f"You already guessed {guess}.")
            return "break"
        hangman_guessed_letters.add(guess)
        if guess in hangman_word:
            hangman_status_label.config(text=f"{guess} is in the word!")
        else:
            hangman_tries -= 1
            hangman_status_label.config(
                text=f"{guess} is not in the word. {hangman_tries} tries left."
            )
    else:
        if guess in hangman_guessed_words:
            hangman_status_label.config(text="You already guessed that word.")
            return "break"
        hangman_guessed_words.add(guess)
        if guess == hangman_word:
            hangman_guessed_letters.update(hangman_word)
            hangman_status_label.config(text="You guessed the word! You win!")
        else:
            hangman_tries -= 1
            hangman_status_label.config(
                text=f"That is not the word. {hangman_tries} tries left."
            )

    update_hangman_display()
    if all(letter in hangman_guessed_letters for letter in hangman_word):
        hangman_status_label.config(text="You guessed the word! You win!")
        hangman_finished = True
    elif hangman_tries == 0:
        hangman_status_label.config(text=f"Game over. The word was {hangman_word}.")
        hangman_finished = True

    if hangman_finished:
        hangman_entry.config(state="disabled")
        hangman_guess_button.config(state="disabled")
    return "break"


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
    menu_frame.pack_forget()
    window.withdraw()
    tic_tac_toe_window.deiconify()
    tic_tac_toe_window.lift()


def open_snake_game():
    global snake_after_id
    menu_frame.pack_forget()
    window.withdraw()
    reset_snake_game()
    snake_window.deiconify()
    snake_window.lift()
    if snake_after_id is None:
        snake_after_id = snake_window.after(100, snake_game_loop)


# Tic Tac Toe setup
playerX = "x"
playerO = "o"
curr_player = playerX
board = [[None, None, None] for _ in range(3)]

color_blue = "#4584b6"
color_yellow = "#ffde57"
color_gray = "#343434"
color_light_gray = "#646464"

turns = 0
tic_tac_toe_game_over = False


def set_tile(row, column):
    global curr_player, turns, tic_tac_toe_game_over
    if tic_tac_toe_game_over or board[row][column]["text"] != "":
        return

    board[row][column].config(text=curr_player)
    turns += 1
    if check_winner():
        return
    if turns == 9:
        tic_tac_toe_game_over = True
        label.config(text="Tie!", foreground=color_yellow)
        return

    curr_player = playerO if curr_player == playerX else playerX
    label.config(text=curr_player + "'s turn")


def check_winner():
    global tic_tac_toe_game_over
    winning_lines = [
        [(row, column) for column in range(3)]
        for row in range(3)
    ] + [
        [(row, column) for row in range(3)]
        for column in range(3)
    ] + [
        [(index, index) for index in range(3)],
        [(index, 2 - index) for index in range(3)],
    ]

    for line in winning_lines:
        row, column = line[0]
        mark = board[row][column]["text"]
        if mark and all(board[r][c]["text"] == mark for r, c in line):
            label.config(text=mark + " is the winner!", foreground=color_yellow)
            for r, c in line:
                board[r][c].config(
                    foreground=color_yellow,
                    background=color_light_gray,
                )
            tic_tac_toe_game_over = True
            return True
    return False


def new_game():
    global turns, tic_tac_toe_game_over, curr_player
    turns = 0
    tic_tac_toe_game_over = False
    curr_player = playerX
    label.config(text=curr_player + "'s turn", foreground="white")
    for row in range(3):
        for column in range(3):
            board[row][column].config(
                text="",
                foreground=color_blue,
                background=color_gray,
            )


# Window setup

tic_tac_toe_window = tk.Toplevel(window)
tic_tac_toe_window.title("Tic Tac Toe")
tic_tac_toe_window.resizable(False, False)
tic_tac_toe_window.withdraw()

frame = tk.Frame(tic_tac_toe_window)
label = tk.Label(
    frame,
    text=curr_player + "'s turn",
    font=("consolas", 20),
    background=color_gray,
    foreground="white",
)
label.grid(row=0, column=0, columnspan=3)
for row in range(3):
    for column in range(3):
        board[row][column] = tk.Button(
            frame,
            text="",
            font=("consolas", 50, "bold"),
            background=color_gray,
            foreground=color_blue,
            width=4,
            height=1,
            command=lambda row=row, column=column: set_tile(row, column),
        )
        board[row][column].grid(row=row + 1, column=column)

button = tk.Button(
    frame,
    text="restart",
    font=("consolas", 20),
    background=color_gray,
    foreground="white",
    command=new_game,
)
button.grid(row=4, column=0, columnspan=3, sticky="we")
tk.Button(
    frame,
    text="Back to Main Menu",
    command=show_game_menu,
).grid(row=5, column=0, columnspan=3, sticky="we")
frame.pack()
tic_tac_toe_window.update_idletasks()
window_width = tic_tac_toe_window.winfo_width()
window_height = tic_tac_toe_window.winfo_height()
screen_width = tic_tac_toe_window.winfo_screenwidth()
screen_height = tic_tac_toe_window.winfo_screenheight()

window_x = int((screen_width - window_width) / 2)
window_y = int((screen_height - window_height) / 2)
tic_tac_toe_window.geometry(
    f"{window_width}x{window_height}+{window_x}+{window_y}"
)
tic_tac_toe_window.protocol("WM_DELETE_WINDOW", show_game_menu)

# Snake game setup
SNAKE_ROWS = 25
SNAKE_COLS = 25
SNAKE_TILE_SIZE = 25
SNAKE_WINDOW_WIDTH = SNAKE_TILE_SIZE * SNAKE_COLS
SNAKE_WINDOW_HEIGHT = SNAKE_TILE_SIZE * SNAKE_ROWS


class SnakeTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


snake = [SnakeTile(5 * SNAKE_TILE_SIZE, 5 * SNAKE_TILE_SIZE)]
food = SnakeTile(10 * SNAKE_TILE_SIZE, 10 * SNAKE_TILE_SIZE)
snake_velocity_x = 0
snake_velocity_y = 0
snake_game_over = False
snake_score = 0
snake_after_id = None


def spawn_snake_food():
    global food
    food = SnakeTile(
        random.randint(0, SNAKE_COLS - 1) * SNAKE_TILE_SIZE,
        random.randint(0, SNAKE_ROWS - 1) * SNAKE_TILE_SIZE,
    )
    while any(segment.x == food.x and segment.y == food.y for segment in snake):
        food = SnakeTile(
            random.randint(0, SNAKE_COLS - 1) * SNAKE_TILE_SIZE,
            random.randint(0, SNAKE_ROWS - 1) * SNAKE_TILE_SIZE,
        )


def reset_snake_game():
    global snake, food, snake_velocity_x, snake_velocity_y, snake_game_over, snake_score, snake_after_id
    if snake_after_id is not None:
        snake_window.after_cancel(snake_after_id)
        snake_after_id = None

    snake[:] = [SnakeTile(5 * SNAKE_TILE_SIZE, 5 * SNAKE_TILE_SIZE)]
    food = SnakeTile(10 * SNAKE_TILE_SIZE, 10 * SNAKE_TILE_SIZE)
    snake_velocity_x = 0
    snake_velocity_y = 0
    snake_game_over = False
    snake_score = 0
    draw_snake_game()
    if snake_window.state() != "withdrawn":
        snake_after_id = snake_window.after(100, snake_game_loop)


def change_snake_direction(event):
    global snake_velocity_x, snake_velocity_y, snake_game_over
    if snake_game_over:
        return

    key = event.keysym
    if key == "Up" and snake_velocity_y != 1:
        snake_velocity_x = 0
        snake_velocity_y = -1
    elif key == "Down" and snake_velocity_y != -1:
        snake_velocity_x = 0
        snake_velocity_y = 1
    elif key == "Left" and snake_velocity_x != 1:
        snake_velocity_x = -1
        snake_velocity_y = 0
    elif key == "Right" and snake_velocity_x != -1:
        snake_velocity_x = 1
        snake_velocity_y = 0


def move_snake():
    global snake_game_over, snake_score
    if snake_game_over:
        return

    head = snake[0]
    next_head = SnakeTile(
        head.x + snake_velocity_x * SNAKE_TILE_SIZE,
        head.y + snake_velocity_y * SNAKE_TILE_SIZE,
    )

    if (
        next_head.x < 0
        or next_head.x >= SNAKE_WINDOW_WIDTH
        or next_head.y < 0
        or next_head.y >= SNAKE_WINDOW_HEIGHT
    ):
        snake_game_over = True
        return

    for segment in snake[1:]:
        if segment.x == next_head.x and segment.y == next_head.y:
            snake_game_over = True
            return

    snake.insert(0, next_head)
    if next_head.x == food.x and next_head.y == food.y:
        snake_score += 1
        spawn_snake_food()
    else:
        snake.pop()


def draw_snake_game():
    global snake_game_over
    snake_canvas.delete("all")
    snake_canvas.create_rectangle(
        0, 0, SNAKE_WINDOW_WIDTH, SNAKE_WINDOW_HEIGHT, fill="black"
    )
    snake_canvas.create_rectangle(
        food.x,
        food.y,
        food.x + SNAKE_TILE_SIZE,
        food.y + SNAKE_TILE_SIZE,
        fill="red",
    )

    for segment in snake:
        snake_canvas.create_rectangle(
            segment.x,
            segment.y,
            segment.x + SNAKE_TILE_SIZE,
            segment.y + SNAKE_TILE_SIZE,
            fill="lime green",
        )

    if snake_game_over:
        snake_canvas.create_text(
            SNAKE_WINDOW_WIDTH / 2,
            SNAKE_WINDOW_HEIGHT / 2,
            font=("Arial", 20),
            text=f"Game Over: {snake_score}",
            fill="white",
        )
    else:
        snake_canvas.create_text(
            30,
            20,
            font=("Arial", 10),
            text=f"Score: {snake_score}",
            fill="white",
        )

def snake_game_loop():
    global snake_after_id
    snake_after_id = None
    move_snake()
    draw_snake_game()
    if not snake_game_over:
        snake_after_id = snake_window.after(100, snake_game_loop)


snake_window = tk.Toplevel(window)
snake_window.title("Snake")
snake_window.resizable(False, False)
snake_window.withdraw()
snake_canvas = tk.Canvas(
    snake_window,
    bg="black",
    width=SNAKE_WINDOW_WIDTH,
    height=SNAKE_WINDOW_HEIGHT,
    borderwidth=0,
    highlightthickness=0,
)
snake_canvas.pack()
snake_controls = tk.Frame(snake_window)
tk.Button(
    snake_controls,
    text="Restart Game",
    command=reset_snake_game,
).pack(side="left", padx=5, pady=5)
tk.Button(
    snake_controls,
    text="Back to Choose Game",
    command=show_game_menu,
).pack(side="left", padx=5, pady=5)
snake_controls.pack()

snake_window.update_idletasks()
snake_window_width = snake_window.winfo_width()
snake_window_height = snake_window.winfo_height()
snake_screen_width = snake_window.winfo_screenwidth()
snake_screen_height = snake_window.winfo_screenheight()

snake_window_x = int((snake_screen_width - snake_window_width) / 2)
snake_window_y = int((snake_screen_height - snake_window_height) / 2)
snake_window.geometry(
    f"{snake_window_width}x{snake_window_height}+{snake_window_x}+{snake_window_y}"
)
snake_window.protocol("WM_DELETE_WINDOW", show_game_menu)
snake_window.bind("<KeyRelease>", change_snake_direction)
reset_snake_game()

# Main menu buttons

tk.Label(
    hangman_frame,
    text="Hangman",
    font=("Arial", 20, "bold"),
    bg="#1e1e2f",
    fg="white",
).pack(pady=(14, 4))
hangman_drawing_label = tk.Label(
    hangman_frame,
    text="",
    font=("Consolas", 12),
    justify="center",
    bg="#1e1e2f",
    fg="white",
)
hangman_drawing_label.pack(pady=4)
hangman_word_label = tk.Label(
    hangman_frame,
    text="",
    font=("Consolas", 20, "bold"),
    bg="#1e1e2f",
    fg="white",
)
hangman_word_label.pack(pady=8)
hangman_status_label = tk.Label(
    hangman_frame,
    text="",
    font=("Arial", 12),
    wraplength=400,
    bg="#1e1e2f",
    fg="white",
)
hangman_status_label.pack(pady=6)
hangman_input_frame = tk.Frame(hangman_frame, bg="#1e1e2f")
hangman_input_frame.pack(pady=6)
hangman_entry = tk.Entry(hangman_input_frame, font=("Arial", 14), width=16)
hangman_entry.pack(side="left", padx=5)
hangman_guess_button = tk.Button(
    hangman_input_frame,
    text="Guess",
    command=submit_hangman_guess,
)
hangman_guess_button.pack(side="left", padx=5)
hangman_entry.bind("<Return>", submit_hangman_guess)
tk.Button(
    hangman_frame,
    text="New Word",
    command=reset_hangman_game,
).pack(pady=5)
tk.Button(
    hangman_frame,
    text="Back to Main Menu",
    command=show_game_menu,
).pack(pady=5)

tk.Button(
    menu_frame,
    text="Rock Paper Scissors",
    command=show_rock_paper_scissors,
    font=("Arial", 14),
    width=22,
).pack(pady=5)
tk.Button(
    menu_frame,
    text="Hangman",
    command=show_hangman,
    font=("Arial", 14),
    width=22,
).pack(pady=5)
tk.Button(
    menu_frame,
    text="Reaction Time",
    command=show_reaction_time,
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

snake_button = tk.Button(
    menu_frame,
    text="Snake",
    command=open_snake_game,
    font=("Arial", 14),
    width=22,
)
snake_button.pack(pady=5)

tk.Button(
    menu_frame,
    text="Pong",
    command=show_pong_game,
    font=("Arial", 14),
    width=22,
).pack(pady=5)
tk.Button(
    menu_frame,
    text="Change Menu Color",
    command=change_color,
    font=("Arial", 12),
).pack(pady=5)

tk.Label(
    reaction_time_frame,
    text="Reaction Time",
    font=("Arial", 20, "bold"),
    bg="#1e1e2f",
    fg="white",
).pack(pady=(35, 12))
reaction_status_label = tk.Label(
    reaction_time_frame,
    text="",
    font=("Arial", 13),
    wraplength=390,
    bg="#1e1e2f",
    fg="white",
)
reaction_status_label.pack(pady=12)
reaction_button = tk.Button(
    reaction_time_frame,
    text="Start",
    command=start_reaction_test,
    font=("Arial", 16, "bold"),
    width=18,
    height=2,
)
reaction_button.pack(pady=12)
tk.Button(
    reaction_time_frame,
    text="Back to Main Menu",
    command=show_game_menu,
).pack(pady=8)
reset_reaction_test()

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

tk.Label(
    thank_you_frame,
    text="THANK YOU FOR PLAYING!",
    font=("Arial", 18, "bold"),
    bg="#1e1e2f",
    fg="white",
).pack(pady=50)
tk.Label(
    thank_you_frame,
    text="Hope you enjoyed the games!",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="white",
).pack(pady=10)
tk.Button(
    thank_you_frame,
    text="Exit Game",
    font=("Arial", 12),
    command=window.destroy,
).pack(pady=20)

class Ball:
    def __init__(self, canvas, width, velocity, board_width, board_height):
        self.canvas = canvas
        self.width = width
        self.velocity = velocity
        self.board_width = board_width
        self.board_height = board_height
        self.item = canvas.create_oval(0, 0, width, width, fill="white")
        self.restart()

    def draw(self):
        self.canvas.coords(
            self.item,
            self.topx,
            self.topy,
            self.topx + self.width,
            self.topy + self.width,
        )

    def restart(self, direction=None):
        self.topx = (self.board_width - self.width) / 2
        self.topy = (self.board_height - self.width) / 2
        self.vx = (direction or random.choice((-1, 1))) * self.velocity
        self.vy = random.choice((-1, 1)) * self.velocity * 0.6
        self.draw()

    def move(self, game):
        self.topx += self.vx
        self.topy += self.vy

        if self.topy <= 0 or self.topy + self.width >= self.board_height:
            self.vy *= -1
            self.topy = max(0, min(self.board_height - self.width, self.topy))

        if self.vx < 0 and game.paddleleft.collide_right(self):
            self.topx = game.paddleleft.topx + game.paddleleft.width
            self.vx = abs(self.vx)
        elif self.vx > 0 and game.paddleright.collide_left(self):
            self.topx = game.paddleright.topx - self.width
            self.vx = -abs(self.vx)

        if self.topx + self.width < 0:
            game.rightpoints += 1
            return 1
        if self.topx > self.board_width:
            game.leftpoints += 1
            return -1

        self.draw()
        return 0


class paddle:
    def __init__(self, canvas, topx, topy, width, height, boardheight):
        self.canvas = canvas
        self.topx = topx
        self.topy = topy
        self.width = width
        self.height = height
        self.boardheight = boardheight
        self.item = canvas.create_rectangle(
            topx, topy, topx + width, topy + height, fill="white"
        )

    def draw(self):
        self.canvas.coords(
            self.item,
            self.topx,
            self.topy,
            self.topx + self.width,
            self.topy + self.height,
        )

    def top(self):
        self.topy = max(0, self.topy - 6)
        self.draw()

    def down(self):
        self.topy = min(self.boardheight - self.height, self.topy + 6)
        self.draw()

    def _overlaps_ball_vertically(self, ball):
        return (
            ball.topy + ball.width >= self.topy
            and ball.topy <= self.topy + self.height
        )

    def collide_right(self, ball):
        return (
            ball.topx + ball.width >= self.topx
            and ball.topx <= self.topx + self.width
            and self._overlaps_ball_vertically(ball)
        )

    def collide_left(self, ball):
        return (
            ball.topx <= self.topx + self.width
            and ball.topx + ball.width >= self.topx
            and self._overlaps_ball_vertically(ball)
        )

# now we can define pong game object
class pong:
    def __init__(self, root, width, height, margin, frame):
        self.root = root
        self.width = width
        self.height = height
        self.margin = margin
        self.paddlewidth = max(8, width // 50)
        self.paddleheight = max(40, height // 8)
        self.leftpoints = 0
        self.rightpoints = 0
        self.leftup = False
        self.leftdown = False
        self.rightup = False
        self.rightdown = False
        self.render = False
        self.timer = None

        self.canvas = tk.Canvas(
            frame, width=width, height=height, bg="black", highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=(10, 4))
        self.paddleleft = paddle(
            self.canvas,
            margin,
            (height - self.paddleheight) / 2,
            self.paddlewidth,
            self.paddleheight,
            height,
        )
        self.paddleright = paddle(
            self.canvas,
            width - margin - self.paddlewidth,
            (height - self.paddleheight) / 2,
            self.paddlewidth,
            self.paddleheight,
            height,
        )
        self.ball = Ball(self.canvas, 14, 5, width, height)
        self.lefttxt = self.canvas.create_text(
            width / 2 - 40, 35, text="0", fill="white", font=("Arial", 24, "bold")
        )
        self.righttxt = self.canvas.create_text(
            width / 2 + 40, 35, text="0", fill="white", font=("Arial", 24, "bold")
        )
        self.drawmiddlelines()
        tk.Label(
            frame,
            text="Left paddle: W/S     Right paddle: O/L     Esc: Main Menu",
            bg="#1e1e2f",
            fg="white",
        ).pack(pady=(0, 6))
        self.root.bind("<KeyPress>", self.keypress)
        self.root.bind("<KeyRelease>", self.keyrelease)

    def drawmiddlelines(self):
        center_x = self.width / 2
        for y in range(0, self.height, 24):
            self.canvas.create_rectangle(
                center_x - 2, y, center_x + 2, min(y + 12, self.height), fill="gray"
            )
        self.canvas.tag_raise(self.lefttxt)
        self.canvas.tag_raise(self.righttxt)

    def drawboard(self):
        self.paddleleft.draw()
        self.paddleright.draw()
        self.ball.draw()
        self.drawpoints()

    def drawpoints(self):
        self.canvas.itemconfig(self.lefttxt, text=str(self.leftpoints))
        self.canvas.itemconfig(self.righttxt, text=str(self.rightpoints))

    def move(self):
        if not self.render:
            return
        if self.leftup:
            self.paddleleft.top()
        if self.leftdown:
            self.paddleleft.down()
        if self.rightup:
            self.paddleright.top()
        if self.rightdown:
            self.paddleright.down()

        point_scored = self.ball.move(self)
        if point_scored:
            self.drawpoints()
            self.ball.restart(direction=point_scored)
        self.timer = self.root.after(16, self.move)

    def start(self):
        if not self.render:
            self.render = True
            self.move()

    def stop(self):
        self.render = False
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None

    def restart(self):
        self.leftpoints = 0
        self.rightpoints = 0
        self.leftup = False
        self.leftdown = False
        self.rightup = False
        self.rightdown = False
        self.paddleleft.topy = (self.height - self.paddleheight) / 2
        self.paddleright.topy = (self.height - self.paddleheight) / 2
        self.paddleleft.draw()
        self.paddleright.draw()
        self.drawpoints()
        self.ball.restart()

    def keypress(self, event):
        if not self.render:
            return
        key = event.keysym.lower()
        if key == "escape":
            show_game_menu()
        elif key == "w":
            self.leftup = True
        elif key == "s":
            self.leftdown = True
        elif key == "o":
            self.rightup = True
        elif key == "l":
            self.rightdown = True

    def keyrelease(self, event):
        key = event.keysym.lower()
        if key == "w":
            self.leftup = False
        elif key == "s":
            self.leftdown = False
        elif key == "o":
            self.rightup = False
        elif key == "l":
            self.rightdown = False

    def killtimer(self):
        self.stop()
        self.root.destroy()


pong_game = pong(window, 640, 380, 24, pong_frame)
type_text()
window.protocol("WM_DELETE_WINDOW", show_thank_you)
window.mainloop()