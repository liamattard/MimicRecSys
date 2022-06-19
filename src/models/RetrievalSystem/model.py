import tensorflow as tf
import tensorflow_recommenders as tfrs

from typing import Dict, Text


class BasicMimicModel(tf.keras.Model):  # type: ignore

    def __init__(self, user_model, medicine_model, task):
        super().__init__()
        self.medicine_model: tf.keras.Model = medicine_model  # type: ignore
        self.user_model: tf.keras.Model = user_model  # type: ignore
        self.task: tf.keras.layers.Layer = task  # type: ignore

    def train_step(self,
                   features: Dict[Text,
                                  tf.Tensor]) -> tf.Tensor:  # type: ignore

        # Set up a gradient tape to record gradients.
        with tf.GradientTape() as tape:

            # Loss computation.
            user_embeddings = self.user_model(features["user_id"])
            tf.print(user_embeddings)
            positive_medicine_embeddings = self.medicine_model(
                features["medicine_name"])
            loss = self.task(user_embeddings, positive_medicine_embeddings)

            # Handle regularization losses as well.
            regularization_loss = sum(self.losses)

            total_loss = loss + regularization_loss

        gradients = tape.gradient(total_loss, self.trainable_variables)
        self.optimizer.apply_gradients(
            zip(gradients, self.trainable_variables))

        metrics = {metric.name: metric.result() for metric in self.metrics}
        metrics["loss"] = loss
        metrics["regularization_loss"] = regularization_loss
        metrics["total_loss"] = total_loss

        return metrics  # type: ignore

    def test_step(self, features: Dict[Text, tf.Tensor]) -> tf.Tensor:

        # Loss computation.
        user_embeddings = self.user_model(features["user_id"])
        positive_medicine_embeddings = self.medicine_model(
            features["medicine_name"])
        loss = self.task(user_embeddings, positive_medicine_embeddings)

        # Handle regularization losses as well.
        regularization_loss = sum(self.losses)

        total_loss = loss + regularization_loss

        metrics = {metric.name: metric.result() for metric in self.metrics}
        metrics["loss"] = loss
        metrics["regularization_loss"] = regularization_loss
        metrics["total_loss"] = total_loss

        return metrics  # type: ignore


def build_model(unique_user_ids, unique_medicine_names, medicine_tensor):

    embedding_dimension = 32

    user_model = tf.keras.Sequential([
        tf.keras.layers.StringLookup(
            vocabulary=unique_user_ids, mask_token=None),
        tf.keras.layers.Embedding(
            len(unique_user_ids) + 1, embedding_dimension)
    ])

    medicine_model = tf.keras.Sequential([
        tf.keras.layers.StringLookup(
            vocabulary=unique_medicine_names, mask_token=None),
        tf.keras.layers.Embedding(
            len(unique_medicine_names) + 1, embedding_dimension)
    ])

    metrics = tfrs.metrics.FactorizedTopK(
      candidates=medicine_tensor.batch(128).map(medicine_model)
    )

    task = tfrs.tasks.Retrieval(
      metrics=metrics
    )

    model = BasicMimicModel(user_model, medicine_model, task)

    return model
