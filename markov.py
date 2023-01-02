
from scipy.sparse import lil_matrix
import numpy as np

text = ""

with open('./clean_messages.txt', 'r', encoding="utf8") as f:
    text += f.read()

k = 3

tokens = text.lower().split()
states = [tuple(tokens[i:i+k]) for i in range(len(tokens)-k+1)]
distinct_states = list(set(states))


m = lil_matrix((len(distinct_states), len(distinct_states)), dtype=float)

state_index = dict(
    [(state, idx_num)
     for idx_num, state in enumerate(distinct_states)])


for i in range(len(tokens)-k):
    state = tuple(tokens[i:i+k])
    next_state = tuple(tokens[i+1:i+1+k])
    row = state_index[state]
    col = state_index[next_state]
    m[row, col] += 1


start_state_index = np.random.randint(len(distinct_states))
state = distinct_states[start_state_index]

max_words = np.random.randint(1, 20)
output = ' '.join(state)

for word in range(max_words):
    row = m[state_index[state], :]
    probabilities = row / row.sum()
    probabilities = probabilities.toarray()[0]

    next_state_index = np.random.choice(
        len(distinct_states),
        1,
        p=probabilities
    )

    next_state = distinct_states[next_state_index[0]]

    output += " " + next_state[-1]
    state = next_state

print(output)
