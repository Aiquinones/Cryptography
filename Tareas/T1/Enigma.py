abc = "abcdefghijklmnopqrstuvwxyz ,"


class Disc:
    def __init__(self, key):
        self.key = key
        self.counter = 0
        self.next_disc = None
        self.prev_disc = None

        self.inverse = None
        self.get_inverse()

    def add_counter(self):
        self.counter += 1
        if self.counter == len(abc):
            self.counter = 0
            if self.next_disc:
                self.next_disc.add_counter()

    def get_inverse(self):
        self.inverse = [0 for _ in range(len(abc))]
        for i, x in enumerate(self.key):
            self.inverse[x] = i

    def get_value(self, letter, inverse=False):

        lis = self.inverse if inverse else self.key

        inp = (letter + self.counter) % len(abc)
        outp = lis[inp] - self.counter

        return outp % len(abc)


class Enigma:
    def __init__(self, keys):
        self.discs = [Disc(key) for key in keys]
        self.i = 0

        for i in range(1, len(self.discs)):
            self.discs[i].next_disc = self.discs[i - 1]

        for i in range(len(self.discs) - 1):
            self.discs[i].prev_disc = self.discs[i + 1]

        self.reflector = [1,
                          0,
                          3,
                          2,
                          5,
                          4,
                          7,
                          6,
                          9,
                          8,
                          11,
                          10,
                          13,
                          12,
                          15,
                          14,
                          17,
                          16,
                          19,
                          18,
                          21,
                          20,
                          23,
                          22,
                          25,
                          24,
                          27,
                          26]

    def process_letter(self, letter):

        # Get Letter #

        letter = letter.lower()  # a lowercase
        letter = abc.index(letter)  # a número

        # Forward #

        disc = self.discs[-1]
        letter = disc.get_value(letter)
        while disc.next_disc:
            disc = disc.next_disc
            letter = disc.get_value(letter)

        # Reflector #

        letter = self.reflector[letter]

        # Backward #

        disc = self.discs[0]
        letter = disc.get_value(letter, inverse=True)
        while disc.prev_disc:
            disc = disc.prev_disc
            letter = disc.get_value(letter, inverse=True)

        # Spin #

        self.discs[-1].add_counter()

        self.i += 1

        return letter

    def process_text(self, text):
        return "".join([abc[self.process_letter(letter)] for letter in text])
