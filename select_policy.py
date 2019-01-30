import tensorflow as tf
import numpy as np


NUM_CARDS = 53


class SelectPolicy(object):
    '''
    Phase 1: card selection policy
    In the selection phase of 2-Mighty, the player can either choose between
    picking the given card and bury the next one without looking,
    or discard the given card and receive the next one.

    In each turn, the player has the information of the current card
    and the accumulated prior information.
    For simplicity, we manage the probability distribution of cards
    which are not yet distributed.
    If we do not use the information of the opponent's choice, the probability
    distribution is uniform excluding the known cards.
    '''
    def __init__(self, policy_model, batch_size):
        self.batch_size = batch_size
        self._hand = list()     # TODO: apply appropriate data representation method
        self._prob = self._initial_prob()
        self._model = policy_model

    @property
    def hand(self):
        return self._hand

    @property
    def prob(self):
        return self._prob

    def _add_hand(self, card):
        # TODO: make this differentiable tf function
        self._hand.append(card)

    def decide(self, card1, card2, turn):
        self._update_prob(card1, 'turn-{}-decide'.format(turn))
        pick = self._pick(card1, turn)

        def _picked():
            self._add_hand(card1)

        def _skipped():
            self._add_hand(card2)
            self._update_prob(card2, 'turn-{}-bury'.format(turn))

        tf.cond(pick, true_fn=_picked, false_fn=_skipped)
        return pick

    def _pick(self, card, turn):
        with tf.name_scope('turn-{}-pick'.format(turn)):
            # if it picks current card, the probability is fixed
            picked = tf.one_hot(card, NUM_CARDS, dtype=tf.float32)
            winrate_pick = self.eval_winrate(picked)
        with tf.name_scope('turn-{}-skip'.format(turn)):
            # if it skips current card, next card will be chosen
            # from the probability state
            winrate_skip = self.eval_winrate(self._prob)
        return winrate_pick > winrate_skip

    def _initial_prob(self):
        # initially, uniform probability for all cards
        with tf.name_scope('turn-0'):
            prob = tf.constant(np.ones((self.batch_size, NUM_CARDS), dtype=np.float32) / NUM_CARDS, name='prob')
        return prob

    def eval_winrate(self, prob):
        # from the current hand and the probability distribution of the next card,
        # evaluate the probability of winning (somehow magically)
        with tf.variable_scope('winrate', reuse=tf.AUTO_REUSE):
            winrate = self._model(self.hand, prob)
        return winrate

    def _update_prob(self, card, scope):
        # remove the card from the probability distribution and re-distribute
        with tf.name_scope(scope):
            mask = 1.0 - tf.one_hot(card, NUM_CARDS, dtype=tf.float32)
            self._prob = tf.math.multiply(self._prob, mask)
            self._prob = tf.divide(self._prob, tf.reduce_mean(self._prob, axis=-1), name='prob')

    def on_opponent_pick(self, pick):
        '''
        Update the probability distribution based on the opponent's choice of pick or skip.
        Intuitively, the pick would imply the better card has gone to the opponent
        than the skip
        '''
        pass        # TODO: apply opponent's pick and update the probability distribution
