from typing import Dict, Text

import tensorflow as tf
import tensorflow_recommenders as tfrs


class Model(tfrs.Model):

    def __init__(self, dataset):
        super().__init__()

        embedding_dimension = 32

        self.user_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=dataset.unique_medicine_ids,
                mask_token=None),
            tf.keras.layers.Embedding(
                len(dataset.unique_medicine_ids) + 1, embedding_dimension),
            tf.keras.layers.GRU(embedding_dimension)])

        self.medicine_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=dataset.unique_medicine_ids,
                mask_token=None),
            tf.keras.layers.Embedding(
                len(dataset.unique_medicine_ids) + 1, embedding_dimension)])

        metrics = tfrs.metrics.FactorizedTopK(
            candidates=dataset.medicine_dataset.batch(128).map(
                self.medicine_model))

        self.task = tfrs.tasks.Retrieval(
            metrics=metrics)

    def compute_loss(self, features: Dict[Text,
                                          tf.Tensor],
                     training=False) -> tf.Tensor:

        medicine_history = features["past_medicine"]
        current_medicine = features["past_medicine"]

        user_embeddings = self.user_model(medicine_history)
        positive_med_embeddings = self.medicine_model(current_medicine)

        return self.task(user_embeddings, positive_med_embeddings,
                         compute_metrics=not training)
