import tensorflow as tf
import numpy as np

from select_policy import SelectPolicy
from manifest_policy import ManifestPolicy


NUM_CARDS = 53
TURNS = 13


def init_manifest():
    # TODO: depends on the representation
    return None


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

    # election phase
    manifest_model = None
    prob_model = None
    players_manifest = [ManifestPolicy(p.hand, p.prob, manifest_model, prob_model) for p in players_select]

    state = init_manifest()
    current_player = tf.constant(False, dtype=tf.bool)

    def _proposed(state, _):
        '''
        return not (state is a give-up)
        '''
        return False

    def _body(state, player):
        next_state = tf.cond(
            player,
            lambda: players_manifest[0].propose(state),
            lambda: players_manifest[1].propose(state))
        next_player = tf.logical_not(player)
        return (next_state, next_player)

    manifesto, lord = tf.while_loop(_proposed, _body, loop_vars=[state, current_player])
    tf.cond(
        lord,
        lambda: players_manifest[0].add_and_drop(card_left),
        lambda: players_manifest[1].add_and_drop(card_left))


if __name__ == '__main__':
    main()
