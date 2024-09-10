import random
import string


def generate_unique_string(keys):
    while True:
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        if random_string not in keys:
            return random_string
