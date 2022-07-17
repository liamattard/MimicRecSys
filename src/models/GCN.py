import tensorflow as tf
import numpy as np


class GCN(tf.keras.Model):

    def __init__(self, voc_size, emb_dim, ehr_adj):
        self.voc_size = voc_size
        self.emb_dim = emb_dim
        adj = self.normalize(adj + np.eye(adj.shape[0]))
        
        self.adj = tf.constant(adj)
        self.x = tf.eye(voc_size)

    def normalize(self, mx):
        rowsum = np.array(mx.sum(1))
        r_inv = np.power(rowsum, -1).flatten()
        r_inv[np.isinf(r_inv)] = 0.
        r_mat_inv = np.diagflat(r_inv)
        mx = r_mat_inv.dot(mx)
        return mx

