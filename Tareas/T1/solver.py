from Enigma import abc


class Solver:
    def __init__(self, enigma, confs, texts, cifrs):
        self.enigma = enigma
        self.size = len(enigma.discs)

        self.training_set = {i: [] for i in range(6)}
        for conf, text, cifr in zip(confs, texts, cifrs):
            self.training_set[conf].append((text, cifr))

        self.answer = [[-1 for _ in range(abc)] for _ in enigma.discs]
        self.i = 0  # disc being solved

        self.offsets = [0 for _ in enigma.discs]

    def get_inverse(self, disc_i):
        inverse = [0 for _ in range(len(abc))]
        for i, x in enumerate(self.answer[disc_i]):
            inverse[x] = i
        return inverse

    def half_output(self, pred, offset=0):
        i_to_process = self.i
        while i_to_process > 0:
            i_to_process -= 1

            local_offset = int(offset/(len(abc)**i_to_process))

            pred = (pred + local_offset) % len(abc)
            pred = self.answer[i_to_process][pred] - local_offset
            pred = pred % len(abc)

        pred = self.enigma.reflector[pred]

        while i_to_process < self.i:
            inv = self.get_inverse(self.answer[i_to_process])

            local_offset = int(offset/(len(abc)**i_to_process))

            pred = (pred + local_offset) % len(abc)
            pred = inv[i_to_process][pred] - local_offset
            pred = pred % len(abc)

            i_to_process += 1

        return pred

    def solve_next_disc(self):
        answer = self.answer[self.i].copy()

        to_choose = set([i for i in range(abc)])
        chosen = set()

        # Choose hypothesis
        hyp = 0

        # Choose prediction
        for pred in range(abc):
            if pred not in to_choose:

                answer[hyp] = pred
                chosen.add(to_choose.pop(pred))

                half_output = self.half_output(pred)

                for text, cifr in self.training_set[self.i]:
                    letter = abc.index(text[0])
                    if letter == hyp:
                        code = abc.index(cifr[0])
                        answer[code] = half_output
                        chosen.add(to_choose.pop(half_output))
                        break

                valid = True
                while answer.count(-1) != 0:
                    for text, cifr in self.training_set[self.i]:
                        for i in range(text):
                            letter = abc.index(text[i])
                            code = abc.index(cifr[i])

                            # TODO: i is offset

                            if answer[letter] != -1:
                                half_output = self.half_output(answer[letter],
                                                               offset=i)

                                if half_output in chosen:
                                    if answer[code] != half_output:
                                        valid = False
                                        break
                                else:
                                    chosen.add(to_choose.pop(half_output))

                        if not valid:
                            break
                    if not valid:
                        break
                if valid:
                    break
                else:
                    answer = self.answer[self.i].copy()
                    to_choose = set([i for i in range(abc)])
                    chosen = set()

        self.answer = answer

        self.i += 1
        if self.i < self.size:
            self.solve_next_disc()

    def solve(self):
        self.solve_next_disc()
        return self.answer
