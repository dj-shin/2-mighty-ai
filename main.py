import tensorflow as tf
import numpy as np

from select_policy import SelectPolicy


NUM_CARDS = 53
TURNS = 13


def main():
    batch_size = 16
    cards = tf.placeholder(shape=(batch_size, NUM_CARDS), dtype=tf.int64)

    select_policy_model = None
    players_select = [SelectPolicy(select_policy_model) for _ in range(2)]

    # card selection phase
    for turn in range(TURNS):
        for i, p in enumerate(players_select):
            card1 = tf.slice(cards, [0, (turn * 2 + i) * 2], [batch_size, 1])
            card2 = tf.slice(cards, [0, (turn * 2 + i) * 2 + 1], [batch_size, 1])
            pick = p.decide(card1, card2)

            other_p = players_select[1 - i]
            other_p.on_opponent_pick(pick)

    card_left = tf.slice(cards, [0, NUM_CARDS - 1], [batch_size, 1])


if __name__ == '__main__':
    main()
