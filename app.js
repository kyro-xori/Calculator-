"use strict";

const menuScreen = document.querySelector("#menu-screen");
const gameScreen = document.querySelector("#game-screen");
const gamePanel = document.querySelector("#game-panel");
const gameTitle = document.querySelector("#game-title");
const gameSubtitle = document.querySelector("#game-subtitle");
const gameEyebrow = document.querySelector("#game-eyebrow");
const themeToggle = document.querySelector("#theme-toggle");
const randomBetween = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

let activeGame = null;
let reactionTimeout = null;
let snakeInterval = null;
let pongFrame = null;
let keyHandler = null;
let pongKeyUpHandler = null;

const hangmanWords = [
  "APPLE", "ORANGE", "BANANA", "GRAPE", "PEACH", "TIGER", "DOLPHIN",
  "TURTLE", "COMPUTER", "KEYBOARD", "MOUNTAIN", "WATERFALL", "VOLCANO",
  "BACKPACK", "DIAMOND", "WIZARD", "SPACESHIP", "GALAXY", "RAINBOW",
  "CHOCOLATE", "POPCORN", "AIRPORT", "MUSEUM", "MYSTERIOUS", "AVALANCHE",
  "LABYRINTH", "CHAMELEON", "BROCCOLI", "NIGHTMARE", "PHOTOGRAPHY",
];

const hangmanStages = [
  "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
  "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
  "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
  "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
  "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
  "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
  "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
];

const games = {
  rps: {
    title: "Rock Paper Scissors",
    subtitle: "First to 5 wins. Pick your move.",
    render: renderRps,
  },
  hangman: {
    title: "Hangman",
    subtitle: "Guess a letter or try the whole word. You have 6 tries.",
    render: renderHangman,
  },
  reaction: {
    title: "Reaction Time",
    subtitle: "Wait for green, then click as quickly as you can.",
    render: renderReaction,
  },
  tic: {
    title: "Tic Tac Toe",
    subtitle: "Take turns with a friend. Get three in a row.",
    render: renderTicTacToe,
  },
  snake: {
    title: "Snake",
    subtitle: "Eat the red food, grow longer, and avoid the walls.",
    render: renderSnake,
  },
  pong: {
    title: "Pong",
    subtitle: "Two-player Pong. First to 5 points wins.",
    render: renderPong,
  },
};

document.querySelectorAll("[data-open]").forEach((button) => {
  button.addEventListener("click", () => openGame(button.dataset.open));
});

document.querySelectorAll("[data-home]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showMenu();
  });
});

document.querySelector("#back-to-menu").addEventListener("click", showMenu);

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("light");
  themeToggle.textContent = document.body.classList.contains("light")
    ? "Switch to dark"
    : "Switch theme";
});

function openGame(name) {
  const game = games[name];
  if (!game) return;
  stopActiveGame();
  activeGame = name;
  gameTitle.textContent = game.title;
  gameSubtitle.textContent = game.subtitle;
  gameEyebrow.textContent = "NOW PLAYING";
  gamePanel.replaceChildren();
  menuScreen.hidden = true;
  gameScreen.hidden = false;
  game.render();
  document.querySelector("#back-to-menu").focus();
}

function showMenu() {
  stopActiveGame();
  activeGame = null;
  gamePanel.replaceChildren();
  gameScreen.hidden = true;
  menuScreen.hidden = false;
  document.querySelector("[data-open]").focus();
}

function stopActiveGame() {
  if (reactionTimeout !== null) {
    window.clearTimeout(reactionTimeout);
    reactionTimeout = null;
  }
  if (snakeInterval !== null) {
    window.clearInterval(snakeInterval);
    snakeInterval = null;
  }
  if (pongFrame !== null) {
    window.cancelAnimationFrame(pongFrame);
    pongFrame = null;
  }
  if (keyHandler) {
    document.removeEventListener("keydown", keyHandler);
    keyHandler = null;
  }
  if (pongKeyUpHandler) {
    document.removeEventListener("keyup", pongKeyUpHandler);
    pongKeyUpHandler = null;
  }
}

function makeElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function makeButton(text, className, onClick) {
  const button = makeElement("button", `game-button ${className || ""}`, text);
  button.type = "button";
  button.addEventListener("click", onClick);
  return button;
}

function makeStatus(text = "") {
  const status = makeElement("p", "status", text);
  status.setAttribute("aria-live", "polite");
  return status;
}

function renderRps() {
  const score = { wins: 0, losses: 0, ties: 0 };
  let finished = false;
  const scoreRow = makeElement("div", "score-row");
  const scoreText = makeStatus("Choose rock, paper, or scissors.");
  const choices = makeElement("div", "choice-row");
  const buttons = [];
  const scorePills = [
    makeElement("span", "score-pill"),
    makeElement("span", "score-pill"),
    makeElement("span", "score-pill"),
  ];
  scorePills.forEach((pill) => scoreRow.append(pill));
  const updateScore = () => {
    scorePills[0].textContent = `You: ${score.wins}`;
    scorePills[1].textContent = `Computer: ${score.losses}`;
    scorePills[2].textContent = `Ties: ${score.ties}`;
  };
  updateScore();
  const replay = makeButton("Play again", "primary", () => {
    score.wins = 0;
    score.losses = 0;
    score.ties = 0;
    finished = false;
    scoreText.textContent = "Choose rock, paper, or scissors.";
    buttons.forEach((button) => { button.disabled = false; });
    replay.hidden = true;
    updateScore();
  });
  replay.hidden = true;
  ["rock", "paper", "scissors"].forEach((choice) => {
    const button = makeButton("", "choice-button", () => {
      if (finished) return;
      const computer = ["rock", "paper", "scissors"][randomBetween(0, 2)];
      let result;
      if (choice === computer) {
        score.ties += 1;
        result = "It's a tie!";
      } else if (
        (choice === "rock" && computer === "scissors")
        || (choice === "paper" && computer === "rock")
        || (choice === "scissors" && computer === "paper")
      ) {
        score.wins += 1;
        result = "You win this round!";
      } else {
        score.losses += 1;
        result = "Computer wins this round!";
      }
      scoreText.textContent = `You chose ${choice}; computer chose ${computer}. ${result}`;
      if (score.wins >= 5 || score.losses >= 5) {
        finished = true;
        scoreText.textContent += score.wins >= 5 ? " You won the game!" : " Game over.";
        buttons.forEach((item) => { item.disabled = true; });
        replay.hidden = false;
      }
      updateScore();
    });
    button.innerHTML = `${{ rock: "✊", paper: "✋", scissors: "✌️" }[choice]}<span>${choice}</span>`;
    button.setAttribute("aria-label", choice);
    buttons.push(button);
    choices.append(button);
  });
  gamePanel.append(scoreRow, scoreText, choices, replay);
}

function renderHangman() {
  let word = hangmanWords[randomBetween(0, hangmanWords.length - 1)];
  let misses = 0;
  const guessedLetters = new Set();
  const guessedWords = new Set();
  let finished = false;
  const art = makeElement("pre", "hangman-art");
  const display = makeElement("p", "word-display");
  const status = makeStatus("Guess a letter or the whole word.");
  const form = makeElement("form", "guess-form");
  const input = makeElement("input", "text-input");
  input.type = "text";
  input.maxLength = word.length;
  input.autocomplete = "off";
  input.setAttribute("aria-label", "Enter a letter or word");
  input.placeholder = "Type a letter or word";
  const guessButton = makeButton("Guess", "primary", () => form.requestSubmit());
  form.append(input, guessButton);
  const newWord = makeButton("New word", "", reset);
  const update = () => {
    art.textContent = hangmanStages[6 - misses];
    display.textContent = [...word].map((letter) => guessedLetters.has(letter) ? letter : "_").join(" ");
    input.disabled = finished;
    guessButton.disabled = finished;
  };
  function reset() {
    word = hangmanWords[randomBetween(0, hangmanWords.length - 1)];
    misses = 0;
    guessedLetters.clear();
    guessedWords.clear();
    finished = false;
    input.maxLength = word.length;
    input.value = "";
    status.textContent = "Guess a letter or the whole word.";
    update();
    input.focus();
  }
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (finished) return;
    const guess = input.value.trim().toUpperCase();
    input.value = "";
    if (!/^[A-Z]+$/.test(guess)) {
      status.textContent = "Enter letters only.";
      return;
    }
    if (guess.length === 1) {
      if (guessedLetters.has(guess)) {
        status.textContent = `You already guessed ${guess}.`;
        return;
      }
      guessedLetters.add(guess);
      if (word.includes(guess)) {
        status.textContent = `${guess} is in the word!`;
      } else {
        misses += 1;
        status.textContent = `${guess} is not in the word. ${6 - misses} tries left.`;
      }
    } else {
      if (guessedWords.has(guess)) {
        status.textContent = "You already guessed that word.";
        return;
      }
      guessedWords.add(guess);
      if (guess === word) {
        [...word].forEach((letter) => guessedLetters.add(letter));
        status.textContent = "You guessed the word! You win!";
      } else {
        misses += 1;
        status.textContent = `That is not the word. ${6 - misses} tries left.`;
      }
    }
    if ([...word].every((letter) => guessedLetters.has(letter))) {
      status.textContent = "You guessed the word! You win!";
      finished = true;
    } else if (misses >= 6) {
      status.textContent = `Game over. The word was ${word}.`;
      finished = true;
    }
    update();
  });
  gamePanel.append(art, display, status, form, newWord);
  update();
  input.focus();
}

function renderReaction() {
  let state = "idle";
  let startedAt = 0;
  const status = makeStatus("Press start, then wait for the green signal.");
  const pad = makeElement("button", "reaction-pad", "Start");
  pad.type = "button";
  const onClick = () => {
    if (state === "idle") {
      state = "waiting";
      pad.className = "reaction-pad waiting";
      pad.textContent = "Wait for green...";
      status.textContent = "Wait for green...";
      reactionTimeout = window.setTimeout(() => {
        reactionTimeout = null;
        if (activeGame !== "reaction") return;
        state = "go";
        startedAt = performance.now();
        pad.className = "reaction-pad go";
        pad.textContent = "CLICK!";
        status.textContent = "Click now!";
      }, randomBetween(1500, 3500));
    } else if (state === "waiting") {
      window.clearTimeout(reactionTimeout);
      reactionTimeout = null;
      state = "idle";
      pad.className = "reaction-pad";
      pad.textContent = "Try again";
      status.textContent = "Too soon! Press to try again.";
    } else if (state === "go") {
      const elapsed = Math.round(performance.now() - startedAt);
      state = "idle";
      pad.className = "reaction-pad";
      pad.textContent = "Try again";
      status.textContent = `Your reaction time: ${elapsed} ms`;
    }
  };
  pad.addEventListener("click", onClick);
  gamePanel.append(status, pad);
}

function renderTicTacToe() {
  let board = Array(9).fill("");
  let turn = "X";
  let finished = false;
  const status = makeStatus("X's turn");
  const grid = makeElement("div", "board");
  grid.setAttribute("role", "group");
  grid.setAttribute("aria-label", "Tic Tac Toe board");
  const cells = board.map((_, index) => {
    const cell = makeButton("", "board-cell", () => play(index));
    cell.setAttribute("aria-label", `Square ${index + 1}, empty`);
    grid.append(cell);
    return cell;
  });
  const restart = makeButton("Restart", "primary", reset);
  function play(index) {
    if (finished || board[index]) return;
    board[index] = turn;
    cells[index].textContent = turn;
    cells[index].classList.add(turn === "X" ? "mark-x" : "mark-o");
    cells[index].setAttribute("aria-label", `Square ${index + 1}, ${turn}`);
    const line = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6],
    ].find(([a, b, c]) => board[a] && board[a] === board[b] && board[b] === board[c]);
    if (line) {
      finished = true;
      status.textContent = `${turn} is the winner!`;
      line.forEach((position) => cells[position].classList.add("primary"));
    } else if (board.every(Boolean)) {
      finished = true;
      status.textContent = "It's a tie!";
    } else {
      turn = turn === "X" ? "O" : "X";
      status.textContent = `${turn}'s turn`;
    }
  }
  function reset() {
    board = Array(9).fill("");
    turn = "X";
    finished = false;
    status.textContent = "X's turn";
    cells.forEach((cell, index) => {
      cell.textContent = "";
      cell.classList.remove("mark-x", "mark-o", "primary");
      cell.setAttribute("aria-label", `Square ${index + 1}, empty`);
    });
  }
  gamePanel.append(status, grid, makeElement("div", "action-row"));
  gamePanel.lastElementChild.append(restart);
}

function renderSnake() {
  const canvas = makeElement("canvas", "game-canvas");
  canvas.width = 500;
  canvas.height = 500;
  canvas.setAttribute("aria-label", "Snake game board");
  const wrap = makeElement("div", "canvas-wrap");
  wrap.append(canvas);
  const context = canvas.getContext("2d");
  const status = makeStatus("Use arrow keys or the buttons to steer.");
  const tile = 20;
  let snake;
  let direction;
  let nextDirection;
  let food;
  let score;
  let ended;
  const resetButton = makeButton("Restart", "primary", reset);
  const dpad = makeElement("div", "dpad");
  [["↑", "up"], ["←", "left"], ["↓", "down"], ["→", "right"]].forEach(([label, dir]) => {
    const button = makeButton(label, dir, () => steer(dir));
    button.setAttribute("aria-label", `Move ${dir}`);
    dpad.append(button);
  });
  function placeFood() {
    do {
      food = { x: randomBetween(0, 24), y: randomBetween(0, 24) };
    } while (snake.some((part) => part.x === food.x && part.y === food.y));
  }
  function reset() {
    snake = [{ x: 5, y: 5 }];
    direction = { x: 0, y: 0 };
    nextDirection = { x: 0, y: 0 };
    score = 0;
    ended = false;
    status.textContent = "Use arrow keys or the buttons to steer.";
    placeFood();
    draw();
  }
  function steer(dir) {
    const moves = {
      up: { x: 0, y: -1 },
      down: { x: 0, y: 1 },
      left: { x: -1, y: 0 },
      right: { x: 1, y: 0 },
    };
    const move = moves[dir];
    const currentDirection = nextDirection.x || nextDirection.y ? nextDirection : direction;
    if (move && !(move.x === -currentDirection.x && move.y === -currentDirection.y)) {
      nextDirection = move;
    }
  }
  function draw() {
    context.fillStyle = "#080a0d";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "#f26b68";
    context.fillRect(food.x * tile + 2, food.y * tile + 2, tile - 4, tile - 4);
    snake.forEach((part, index) => {
      context.fillStyle = index === 0 ? "#a4edb6" : "#51c97c";
      context.fillRect(part.x * tile + 1, part.y * tile + 1, tile - 2, tile - 2);
    });
    context.fillStyle = "#f5f3ef";
    context.font = "14px monospace";
    context.fillText(`SCORE: ${score}`, 12, 22);
  }
  function tick() {
    if (ended || activeGame !== "snake") return;
    if (nextDirection.x || nextDirection.y) direction = nextDirection;
    if (direction.x === 0 && direction.y === 0) return;
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };
    const ate = head.x === food.x && head.y === food.y;
    const body = ate ? snake : snake.slice(0, -1);
    if (
      head.x < 0 || head.x >= 25 || head.y < 0 || head.y >= 25
      || body.some((part) => part.x === head.x && part.y === head.y)
    ) {
      ended = true;
      status.textContent = `Game over! Your score: ${score}. Press Restart to play again.`;
      return;
    }
    snake.unshift(head);
    if (ate) {
      score += 1;
      if (snake.length === 25 * 25) {
        ended = true;
        status.textContent = "You filled the whole board! You win.";
        draw();
        return;
      }
      placeFood();
      status.textContent = `Score: ${score}`;
    } else {
      snake.pop();
    }
    draw();
  }
  keyHandler = (event) => {
    const map = {
      ArrowUp: "up", w: "up", ArrowDown: "down", s: "down",
      ArrowLeft: "left", a: "left", ArrowRight: "right", d: "right",
    };
    const move = map[event.key];
    if (move) {
      event.preventDefault();
      steer(move);
    }
  };
  document.addEventListener("keydown", keyHandler);
  gamePanel.append(status, wrap, dpad, makeElement("div", "action-row"));
  gamePanel.lastElementChild.append(resetButton);
  reset();
  snakeInterval = window.setInterval(tick, 100);
}

function renderPong() {
  const canvas = makeElement("canvas", "game-canvas");
  canvas.width = 640;
  canvas.height = 380;
  canvas.setAttribute("aria-label", "Pong game board");
  const wrap = makeElement("div", "canvas-wrap");
  wrap.append(canvas);
  const context = canvas.getContext("2d");
  const status = makeStatus("First to 5 points wins.");
  const keys = new Set();
  const paddleHeight = 76;
  const paddleWidth = 10;
  const ballSize = 12;
  let leftY;
  let rightY;
  let ball;
  let score;
  let finished;
  let lastTime = 0;
  const resetButton = makeButton("Restart", "primary", reset);

  function serve(direction = Math.random() < 0.5 ? -1 : 1) {
    ball = {
      x: canvas.width / 2 - ballSize / 2,
      y: canvas.height / 2 - ballSize / 2,
      vx: direction * 280,
      vy: (Math.random() < 0.5 ? -1 : 1) * randomBetween(100, 190),
    };
  }
  function reset() {
    leftY = (canvas.height - paddleHeight) / 2;
    rightY = leftY;
    score = { left: 0, right: 0 };
    finished = false;
    keys.clear();
    status.textContent = "First to 5 points wins.";
    serve();
    draw();
  }
  function draw() {
    context.fillStyle = "#080a0d";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "#69707c";
    for (let y = 0; y < canvas.height; y += 28) {
      context.fillRect(canvas.width / 2 - 2, y, 4, 15);
    }
    context.fillStyle = "#f5f3ef";
    context.fillRect(20, leftY, paddleWidth, paddleHeight);
    context.fillRect(canvas.width - 30, rightY, paddleWidth, paddleHeight);
    context.fillRect(ball.x, ball.y, ballSize, ballSize);
    context.font = "bold 28px monospace";
    context.textAlign = "center";
    context.fillText(score.left, canvas.width / 2 - 46, 42);
    context.fillText(score.right, canvas.width / 2 + 46, 42);
  }
  function frame(now) {
    if (activeGame !== "pong") return;
    const delta = lastTime ? Math.min((now - lastTime) / 1000, 0.04) : 0;
    lastTime = now;
    if (!finished) {
      const paddleSpeed = 280 * delta;
      if (keys.has("w")) leftY -= paddleSpeed;
      if (keys.has("s")) leftY += paddleSpeed;
      if (keys.has("o")) rightY -= paddleSpeed;
      if (keys.has("l")) rightY += paddleSpeed;
      leftY = Math.max(0, Math.min(canvas.height - paddleHeight, leftY));
      rightY = Math.max(0, Math.min(canvas.height - paddleHeight, rightY));
      ball.x += ball.vx * delta;
      ball.y += ball.vy * delta;
      if (ball.y <= 0 || ball.y + ballSize >= canvas.height) {
        ball.vy *= -1;
        ball.y = Math.max(0, Math.min(canvas.height - ballSize, ball.y));
      }
      if (
        ball.vx < 0 && ball.x <= 30 && ball.x + ballSize >= 20
        && ball.y + ballSize >= leftY && ball.y <= leftY + paddleHeight
      ) {
        ball.vx = Math.abs(ball.vx) * 1.04;
        ball.x = 30;
        ball.vy += ((ball.y + ballSize / 2 - (leftY + paddleHeight / 2)) / paddleHeight) * 100;
      } else if (
        ball.vx > 0 && ball.x + ballSize >= canvas.width - 30 && ball.x <= canvas.width - 20
        && ball.y + ballSize >= rightY && ball.y <= rightY + paddleHeight
      ) {
        ball.vx = -Math.abs(ball.vx) * 1.04;
        ball.x = canvas.width - 30 - ballSize;
        ball.vy += ((ball.y + ballSize / 2 - (rightY + paddleHeight / 2)) / paddleHeight) * 100;
      }
      if (ball.x + ballSize < 0) {
        score.right += 1;
        pointScored(-1);
      } else if (ball.x > canvas.width) {
        score.left += 1;
        pointScored(1);
      }
    }
    draw();
    pongFrame = window.requestAnimationFrame(frame);
  }
  function pointScored(direction) {
    if (score.left >= 5 || score.right >= 5) {
      finished = true;
      status.textContent = score.left >= 5 ? "Left player wins! Press Restart to play again." : "Right player wins! Press Restart to play again.";
    } else {
      status.textContent = `Score — Left: ${score.left} | Right: ${score.right}`;
      serve(direction);
    }
  }
  keyHandler = (event) => {
    const key = event.key.toLowerCase();
    if (["w", "s", "o", "l"].includes(key)) {
      event.preventDefault();
      keys.add(key);
    }
  };
  const releaseKeys = (event) => keys.delete(event.key.toLowerCase());
  document.addEventListener("keydown", keyHandler);
  document.addEventListener("keyup", releaseKeys);
  pongKeyUpHandler = releaseKeys;
  const controls = makeElement("div", "pong-controls");
  [
    ["Left", "w", "s"],
    ["Right", "o", "l"],
  ].forEach(([player, up, down]) => {
    const group = makeElement("div", "control-group");
    group.append(makeElement("span", "", player));
    [[up, "↑"], [down, "↓"]].forEach(([key, label]) => {
      const button = makeButton(label, "", () => {});
      button.addEventListener("pointerdown", (event) => {
        event.preventDefault();
        keys.add(key);
      });
      ["pointerup", "pointerleave", "pointercancel"].forEach((name) => {
        button.addEventListener(name, () => keys.delete(key));
      });
      button.setAttribute("aria-label", `${player} paddle ${label === "↑" ? "up" : "down"}`);
      group.append(button);
    });
    controls.append(group);
  });
  gamePanel.append(status, wrap, controls, makeElement("p", "hint", "Keyboard: left W/S · right O/L"));
  const actions = makeElement("div", "action-row");
  actions.append(resetButton);
  gamePanel.append(actions);
  reset();
  pongFrame = window.requestAnimationFrame(frame);
}
