import random

choices = ["rock", "paper", "scissors"]
print("Let's play Rock, Paper, Scissors!")
player = input("Choose rock, paper, or scissors: ").lower()
computer = random.choice(choices)

print("You chose:", player)
print("The computer chose:", computer)
if player not in choices:
    print("Invalid choice! Please choose rock, paper, or scissors.")
elif player == computer:
    print("It's a tie! Better luck next time.")
elif (
        (player=="rock" and computer=="scissors")
        or (player == "paper" and computer == "rock")
        or (player == "scissors" and computer == "paper")
    ):
    print ("You win! Congratulations!")
else:
    print("You lose! Better luck next time:p")
