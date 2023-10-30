#!/usr/bin/python

"""
A simple Hangman game implementation.
"""

import random

def get_words_from_file(fname, encoding='utf-8'):
    """
    This function takes a filename as input, reads the words from the file, 
    and returns a list containing those words.
    """
    words_list = []
    with open(fname, encoding=encoding) as file:
        for line in file:
            words_list.append(line.strip())
    return words_list

def get_random_word(words_list):
    """
    This function takes a list of words as input and returns a random word from that list. 
    """
    word = random.choice(words_list)
    return word

def display_hangman(tries):
    """
    This function takes the number of remaining attempts (tries) as input
    and returns the corresponding ASCII art representation of the hangman figure
    based on the number of tries left.
    """
    situations = [
       # 6 attempt
        '''
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / \\
           |
          ---
        ''',
        # 5 attempt
        '''
           --------
           |      |
           |      O
           |     \|/
           |      |
           |       \\
           |
          ---
        ''',
        # 4 attempt
        '''
           --------
           |      |
           |      O
           |     \|/
           |      |
           |
           |
          ---
        ''',
        # 3 attempt
        '''
           --------
           |      |
           |      O
           |      |/
           |      |
           |
           |
          ---
        ''',
        # 2 attempt
        '''
           --------
           |      |
           |      O
           |      |
           |      |
           |
           |
          ---
        ''',
        # 1 attempt
        '''
           --------
           |      |
           |      O
           |
           |
           |
           |
          ---
        ''',
        # initial state
        '''
           --------
           |      |
           |
           |
           |
           |
           |
          ---
        ''']
    return situations[tries] 
  
def display_current_state(tries, word_completion):
    """
    This functin takes the number of remaining attempts (tries)
    and the current state of word completion (word_completion)
    as input and prints the hangman figure 
    and the current state of the word being guessed.
    """
    print(display_hangman(tries))
    print(word_completion)
    print("\n")

def handle_letter_guess(guess, guessed_letters, word, word_completion, tries):
    """
    This function handles a valid letter guess. It checks if the letter has been guessed before.
    If not, it checks if the letter is in the word. It updates the guessed letters, word completion, 
    and the number of tries left accordingly.
    """
    if guess in guessed_letters:
        print("You already guessed the letter", guess)
    elif guess not in word:
        print(guess, "isn't in the word.")
        tries -= 1
        guessed_letters.append(guess)
    else:
        print(guess, "is in the word!")
        guessed_letters.append(guess)
        word_completion = update_word_completion(word, word_completion, guess)
    return tries, word_completion

def update_word_completion(word, word_completion, guess):
    """
    This function takes the correct word, the current state of word completion,
    and the correctly guessed letter and updates the word completion with the correctly 
    guessed letter in its corresponding positions.
    """
    word_as_list = list(word_completion)
    for el in range(len(word)):
        if word[el] == guess:
            word_as_list[el] = guess
    return "".join(word_as_list)

def play_game(word):
    """
    This is the main function for playing the Hangman game.
    It takes a random word as input and manages the game flow. 
    It allows the player to make guesses, handles letter and word guesses, updates the game state, 
    and displays appropriate messages based on the player's guesses and progress.
    """
    word_completion = "_" * len(word)
    guessed_letters = []
    tries = 6
    display_current_state(tries, word_completion)
    while tries > 0 and "_" in word_completion:
        guess = input("Please guess a letter: ") 
        if len(guess) == 1 and guess.isalpha():
            tries, word_completion = handle_letter_guess(guess, guessed_letters, word, word_completion, tries)
        else:
            print("Not a valid guess.")       
        display_current_state(tries, word_completion)
    if "_" not in word_completion:
        print("Congratulations, you guessed the word!")
    else:
        print("Sorry, you ran out of tries. The word was ", word)

def main():
    """
    Main function to run the game
    """
    fname = "words.txt"
    print("Welcome to Hangman game!  Let's play ")
    words_list = get_words_from_file(fname)
    while True:
        word = get_random_word(words_list)
        play_game(word)
        play_again = input("Play Again? (yes/no): ")
        if play_again.lower() != "yes":
            break

if __name__ == "__main__":
    main()

