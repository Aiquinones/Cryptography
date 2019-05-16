from functools import reduce
from Enigma import abc


def key_generator():
    alphabet_list = [c for c in range(len(abc))]
    for i in range(len(alphabet_list)):
        alphabet_copy = alphabet_list.copy()
        choice = alphabet_copy.pop(i)
        for post_key in recursive_get_key(alphabet_copy):
            yield choice + post_key


def recursive_get_key(remaining):
    if len(remaining) == 1:
        yield remaining[0]
    for i in range(len(remaining)):
        remaining_popped = remaining.copy()
        choice = remaining_popped.pop(i)
        for post_key in recursive_get_key(remaining_popped):
            yield choice + post_key


def sum(x1, x2): return x1 + x2


for key in key_generator():
    print(reduce(sum, key))
