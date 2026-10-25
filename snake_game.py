import random
import tkinter as tk

ROWS = 25
COLS = 25
TILE_SIZE = 25
WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


window = tk.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tk.Canvas(
    window,
    bg="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    borderwidth=0,
    highlightthickness=0,
)
canvas.pack()

snake = [Tile(5 * TILE_SIZE, 5 * TILE_SIZE)]
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
velocity_x = 0
velocity_y = 0
game_over = False
score = 0


def spawn_food():
    global food
    food = Tile(
        random.randint(0, COLS - 1) * TILE_SIZE,
        random.randint(0, ROWS - 1) * TILE_SIZE,
    )
    while any(segment.x == food.x and segment.y == food.y for segment in snake):
        food = Tile(
            random.randint(0, COLS - 1) * TILE_SIZE,
            random.randint(0, ROWS - 1) * TILE_SIZE,
        )


def change_direction(event):
    global velocity_x, velocity_y, game_over
    if game_over:
        return

    key = event.keysym
    if key == "Up" and velocity_y != 1:
        velocity_x = 0
        velocity_y = -1
    elif key == "Down" and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1
    elif key == "Left" and velocity_x != 1:
        velocity_x = -1
        velocity_y = 0
    elif key == "Right" and velocity_x != -1:
        velocity_x = 1
        velocity_y = 0


def move():
    global game_over, score
    if game_over:
        return

    head = snake[0]
    next_head = Tile(head.x + velocity_x * TILE_SIZE, head.y + velocity_y * TILE_SIZE)

    if (
        next_head.x < 0
        or next_head.x >= WINDOW_WIDTH
        or next_head.y < 0
        or next_head.y >= WINDOW_HEIGHT
    ):
        game_over = True
        return

    for segment in snake[1:]:
        if segment.x == next_head.x and segment.y == next_head.y:
            game_over = True
            return

    snake.insert(0, next_head)
    if next_head.x == food.x and next_head.y == food.y:
        score += 1
        spawn_food()
    else:
        snake.pop()


def draw():
    global game_over
    canvas.delete("all")
    canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill="black")

    canvas.create_rectangle(
        food.x,
        food.y,
        food.x + TILE_SIZE,
        food.y + TILE_SIZE,
        fill="red",
    )

    for segment in snake:
        canvas.create_rectangle(
            segment.x,
            segment.y,
            segment.x + TILE_SIZE,
            segment.y + TILE_SIZE,
            fill="lime green",
        )

    if game_over:
        canvas.create_text(
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2,
            font=("Arial", 20),
            text=f"Game Over: {score}",
            fill="white",
        )
    else:
        canvas.create_text(
            30,
            20,
            font=("Arial", 10),
            text=f"Score: {score}",
            fill="white",
        )

    if not game_over:
        window.after(100, game_loop)


def game_loop():
    move()
    draw()


window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.bind("<KeyRelease>", change_direction)
window.after(100, game_loop)
window.mainloop()
