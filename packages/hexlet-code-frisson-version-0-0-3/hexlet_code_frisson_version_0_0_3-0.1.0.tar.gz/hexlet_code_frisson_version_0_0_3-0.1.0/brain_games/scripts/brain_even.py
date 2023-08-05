#!/usr/bin/env python3
from random import random
import prompt


def main():
    user_answer = ''
    random_num = int(random()*100)
    print("Welcome to the Brain Games!")
    name = prompt.string('May I have your name? ')
    print(f'Hello, {name}!')
    print('Answer "yes" if the number is even, otherwise answer "no".')
    count_correct = 0
    while count_correct < 3:
        correct_answer = 'yes' if random_num % 2 == 0 else 'no'
        print(f"Question:{random_num}")
        user_answer = prompt.string('Your answer:')
        if user_answer.lower() == correct_answer:
            random_num = int(random()*100)
            count_correct += 1
            print('Correct!')
        else:
            print("'yes' is wrong answer ;(. Correct answer was 'no'.)")
            print(f"Let's try again, {name}!")
            return
    print(f'Congratulations, {name}!')


if __name__ == '__main__':
    main()
