import os
import random

module_dir = os.path.dirname(__file__)

def q():
    with open(os.path.join(module_dir, "quotes.txt"), "r") as file:
        lines = file.readlines()

    new_lines = [s for s in lines if s.strip() != ""]
    return random.choice(new_lines)

def x():
    with open(os.path.join(module_dir, "sorry.txt"), "r") as file:
        content = file.read()
    return content

if __name__ == "__main__":
    print(x())