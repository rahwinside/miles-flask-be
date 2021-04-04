import random
import string


def random_string(str_size):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_size))
