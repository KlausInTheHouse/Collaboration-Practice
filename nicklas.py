import random
import sys
import time

def slow_print(text, delay=0.02):
    """Print text with a tiny delay between characters (just for fun)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def play_game():
    slow_print("🎮 Welcome to the Number Guessing Game!")
    slow_print("I'm thinking of a number between 1 and 100...")
    slow_print("You have 7 tries to guess it.\n")

    secret = random.randint(1, 100)
    attempts = 7

    for attempt in range(1, attempts + 1):
        while True:
            guess_str = input(f"Attempt {attempt}/{attempts} – Your guess: ")
            if guess_str.strip().isdigit():
                guess = int(guess_str)
                break
            else:
                print("Please enter a valid integer!")

        if guess == secret:
            slow_print("\n🎉 Correct! You guessed the number!")
            slow_print(f"You did it in {attempt} attempt(s). Nice job 😎")
            break
        elif guess < secret:
            print("Too low! 📉")
        else:
            print("Too high! 📈")

        # Give a little hint if they are close
        if abs(guess - secret) <= 5:
            print("🔥 You're very close!\n")
        else:
            print("Try again...\n")
    else:
        slow_print("\n😢 Out of attempts!")
        slow_print(f"The number was: {secret}")

def main():
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing! 👋")
            sys.exit()

if __name__ == "__main__":
    main()
