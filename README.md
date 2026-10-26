# Mini Games

A small mini-games project with a Python desktop app and a browser version.

## Play in a web browser

Play the [browser version online](https://kyro-xori.github.io/Calculator-/), or
open `index.html` in a browser. It is a static site and does not need Python, an
install, or a server. The web version includes Rock Paper Scissors, Hangman,
Reaction Time, Tic Tac Toe, Snake, and Pong.

## Run the game picker

Run the Python GUI game picker from the project folder:

```powershell
python rock_paper_scissors_gui.py
```

The app menu includes Rock Paper Scissors, Hangman, Reaction Time, Tic Tac Toe,
Snake, and Pong. In Reaction Time, wait for the button to turn green, then
click it as quickly as you can. Pong is a two-player game: use W/S for the
left paddle and O/L for the right paddle.

The menu also displays a typing welcome message and has a button to toggle
between dark and light blue. Closing the main window displays a thank-you page.

The GUI uses Python's built-in Tkinter library. If Tkinter is missing from your
Python installation, install or select a Python distribution that includes
Tkinter.

## Other examples

- `hangman.py` contains the word list and Hangman helpers used by the GUI and
  command-line game.
- `rock_paper_scissors.py` is a command-line Rock Paper Scissors game.
- `main.py` is a command-line calculator.
