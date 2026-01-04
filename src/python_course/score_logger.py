import random
def score_logger():
    name = input("Enter your name: ")
    score = input("Enter your score: ")

    with open("scores.txt", "a") as file:
        file.write(name + " : " + score)
        content = file.read()
        print(content)

score_logger()