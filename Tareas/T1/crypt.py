from Enigma import Enigma, abc
import random
import sys

SEED = 4811
random.seed(SEED)

if len(sys.argv) < 3:
    print('please add message to crypt')
    exit()


def generate_random_key():
    alphabet_list = [c for c in abc]
    random.shuffle(alphabet_list)
    return alphabet_list


keys = [list(generate_random_key()) for _ in range(int(sys.argv[1]))]

# mensaje = "holacomoestasbienytuquebuenosaludospicas"
mensaje = sys.argv[2]

enigma = Enigma(keys)

print("starting crypting ...")
crypted = ''
for letter in mensaje:
    crypted += enigma.process_letter(letter)
print(crypted)
