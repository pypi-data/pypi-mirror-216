import os
import random

def quote():
    module_dir = os.path.dirname(__file__)

    with open(os.path.join(module_dir, "quotes.txt"), "r") as file:
        lines = file.readlines()

    new_lines = [s for s in lines if s.strip() != ""]
    return random.choice(new_lines)

if __name__ == "__main__":
    print(quote())