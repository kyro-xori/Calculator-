import random

from words import word_list


def get_word():
    return random.choice(word_list).upper()


def display_hangman(tries):
    stages = [
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
    ]
    return stages[tries]


def play(word):
    word = word.upper()
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    print("Let's play Hangman!")
    print(display_hangman(tries))
    print(word_completion)
    print()

    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").strip().upper()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
                continue

            guessed_letters.append(guess)
            if guess in word:
                print("Good job,", guess, "is in the word.")
                word_completion = "".join(
                    letter if letter in guessed_letters else "_" for letter in word
                )
                guessed = "_" not in word_completion
            else:
                print(guess, "is not in the word.")
                tries -= 1
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
                continue

            guessed_words.append(guess)
            if guess == word:
                word_completion = word
                guessed = True
            else:
                print(guess, "is not the word.")
                tries -= 1
        else:
            print("Not a valid guess.")

        print(display_hangman(tries))
        print(word_completion)
        print()

    if guessed:
        print("Congrats, you guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries. The word was " + word + ".")


def main():
    while True:
        play(get_word())
        if input("Play again? (Y/N): ").strip().upper() != "Y":
            break


if __name__ == "__main__":
    main()