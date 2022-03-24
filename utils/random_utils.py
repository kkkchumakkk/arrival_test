import random
import string


class RandomUtils:

    @staticmethod
    def gen_random_from_set(required_set):
        return random.choice(required_set)

    @staticmethod
    def gen_random_string(string_length):
        return ''.join(random.choices(string.ascii_letters, k=string_length))

    @staticmethod
    def gen_random_float(interval_start, interval_end, precision=2):
        return round(random.uniform(interval_start, interval_end), precision)