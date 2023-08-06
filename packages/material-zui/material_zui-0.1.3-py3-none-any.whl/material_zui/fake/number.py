import random
from time import sleep


def int_number(min: int, max: int) -> int: return random.randint(min, max)


def random_sleep(min: int = 1, max: int = 5, sec: float = 0) -> None:
    time = sec if sec > 0 else int_number(min, max)
    sleep(time)
