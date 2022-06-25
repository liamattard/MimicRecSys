from typing import Dict, Text

import tensorflow as tf
import tensorflow_recommenders as tfrs


class Model(tfrs.Model):

    def __init__(self, dataset):
        super().__init__()

        embedding_dimension = 32

        self.user_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=dataset.unique_user_ids,
                mask_token=None),
            tf.keras.layers.Embedding(
                len(dataset.unique_user_ids) + 1, embedding_dimension)])

        self.medicine_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=dataset.unique_medicine_names,
                mask_token=None),
            tf.keras.layers.Embedding(
                len(dataset.unique_medicine_names) + 1, embedding_dimension)])

        metrics = tfrs.metrics.FactorizedTopK(
            candidates=dataset.medicine_dataset.batch(128).map(
                self.medicine_model))

        self.task = tfrs.tasks.Retrieval(
            metrics=metrics)

    def compute_loss(self, features: Dict[Text,
                                          tf.Tensor],
                     training=False) -> tf.Tensor:

        user_embeddings = self.user_model(features["user_id"])
        positive_med_embeddings = self.medicine_model(
                                            features["medicine_name"])

        return self.task(user_embeddings, positive_med_embeddings)
