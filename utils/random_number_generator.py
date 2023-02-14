from random import randint

def generate_random_number(length):
    return ''.join(["{}".format(randint(0, 9)) for num in range(0, length)])