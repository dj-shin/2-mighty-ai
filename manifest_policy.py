import tensorflow as tf


class ManifestPolicy(object):
    def __init__(self, hand, prob, manifest_model, prob_model):
        self._hand = hand
        self._prob = prob
        self._manifest_model = manifest_model
        self._prob_model = prob_model

    def propose(self, history):
        self._update_prob(history)
        manifest = self._manifest_model(self._hand, self._prob)
        return manifest

    def _update_prob(self, history):
        self._prob = self._prob_model(self._prob, history)

    def add_and_drop(self, card):
        '''
        winrate: (batch_size, *repr) -> (batch_size, 14, *repr)
        discard = tf.argmin(winrate, axis=1)
        self._hand = apply(self._hand, discard)
        '''
