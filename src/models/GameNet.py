import tensorflow as tf


class Model(tf.keras.Model):

    def __init__(self, voc_size, emb_dim, ehr_adj, ddi_adj):

        super().__init__()
        self.K = len(voc_size)
        self.vocab_size = voc_size
        self.tensor_ddi_adj = tf.constant(ddi_adj, dtype=tf.float32)
        self.embeddings = [tf.keras.layers.Embedding(
                                voc_size[i], 64) for i in range(self.K-1)]
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.encoders = [tf.keras.layers.GRU(
                            emb_dim * 2,
                            time_major=True) for _ in range(self.K-1)]

        self.query = tf.keras.layers.Sequential([
                        tf.keras.layers.ReLU(),
                        tf.keras.layers.Linear(emb_dim * 4, emb_dim)])

