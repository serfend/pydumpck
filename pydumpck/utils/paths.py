import random


def get_random_path(src_path: str, char_count: int = 6) -> str:
    start = 10 ** char_count
    return f'{src_path}_{random.Random().randint(int(start),int(start*10)-1)}'
