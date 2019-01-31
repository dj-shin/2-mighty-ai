import tensorflow as tf


def encode_card(card):
    # 13 numbers : one-hot
    # 4 shapes : one-hot (Heart, Spade, Clover, Diamond)
    # 5 (potentially) special cards (Spade A, Dia A, Clover 3, Heart 3, Jocker)
    is_jocker = tf.equal(card, 53)
    shape = tf.cond(
        is_jocker,
        lambda: tf.zeros(4),
        lambda: tf.one_hot(tf.dtype.cast(tf.divide(card, 13), tf.int64), 4, dtype=tf.int64))
    number = tf.cond(
        is_jocker,
        lambda: tf.zeros(13),
        lambda: tf.one_hot(card - tf.math.argmax(shape) * 13, 13, dtype=tf.int64))

    is_spade_a = tf.cast(tf.equal(card, 13 * 1 + 0), tf.int64)
    is_diamond_a = tf.cast(tf.equal(card, 13 * 3 + 0), tf.int64)
    is_clover_3 = tf.cast(tf.equal(card, 13 * 2 + 2), tf.int64)
    is_heart_3 = tf.cast(tf.equal(card, 13 * 0 + 2), tf.int64)
    is_jocker = tf.cast(is_jocker, tf.int64)

    return tf.concat([number, shape, is_jocker, is_spade_a, is_diamond_a, is_clover_3, is_heart_3])
