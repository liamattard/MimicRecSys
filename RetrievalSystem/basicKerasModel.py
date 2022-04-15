import tensorflow as tf
import tensorflow_recommenders as tfrs

from typing import Dict, Text


class BasicMimicModel(tfrs.Model):

    def __init__(self, user_model, medicine_model, task):
        super().__init__()
        self.medicine_model: tf.keras.Model = medicine_model  # type: ignore
        self.user_model: tf.keras.Model = user_model  # type: ignore
        self.task: tf.keras.layers.Layer = task  # type: ignore

    def compute_loss(self, features: Dict[Text, tf.Tensor],
                     training=False) -> tf.Tensor:

        user_embeddings = self.user_model(features["user_id"])
        positive_medicine_embeddings = self.medicine_model(
                     features["medicine_name"])
        return self.task(user_embeddings, positive_medicine_embeddings)
