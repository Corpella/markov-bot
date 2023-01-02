
from scipy.sparse import lil_matrix
import numpy as np


class Markov:
    def __init__(self):
        self.k = 3
        self.model = []
        self.state_index = dict()
        self.distinct_states = []

    def get_tokens(self):
        text = ""
        with open('./clean_messages.txt', 'r', encoding="utf8") as f:
            text += f.read()
        return text.lower().split()

    def fill_model(self):
        tokens = self.get_tokens()
        states = [tuple(tokens[i:i+self.k])
                  for i in range(len(tokens)-self.k+1)]

        self.distinct_states = list(set(states))

        self.model = lil_matrix(
            (len(self.distinct_states), len(self.distinct_states)), dtype=float)

        self.state_index = dict(
            [(state, idx_num)
             for idx_num, state in enumerate(self.distinct_states)])

        for i in range(len(tokens)-self.k):
            state = tuple(tokens[i:i+self.k])
            next_state = tuple(tokens[i+1:i+1+self.k])
            row = self.state_index[state]
            col = self.state_index[next_state]
            self.model[row, col] += 1

    def generate_sentence(self):
        start_state_index = np.random.randint(len(self.distinct_states))
        state = self.distinct_states[start_state_index]

        max_words = np.random.randint(1, 20)
        output = ' '.join(state)

        for _ in range(max_words):
            row = self.model[self.state_index[state], :]
            probabilities = row / row.sum()
            probabilities = probabilities.toarray()[0]

            next_state_index = np.random.choice(
                len(self.distinct_states),
                1,
                p=probabilities
            )

            next_state = self.distinct_states[next_state_index[0]]

            output += " " + next_state[-1]
            state = next_state
        print(output)

    def menu(self):
        while True:
            command = input(
                "Write 'start' to generate a sentence, 'stop' to exit: \n")
            if command == "start":
                self.generate_sentence()
            if command == "stop":
                print("Goodbye!")
                break


def main():
    markov_bot = Markov()
    markov_bot.fill_model()
    markov_bot.menu()


if __name__ == '__main__':
    main()
