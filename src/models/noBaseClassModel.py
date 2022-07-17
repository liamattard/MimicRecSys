from typing import Dict, Text

import tensorflow as tf
import tensorflow_recommenders as tfrs


class Model(tf.keras.Model):

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

    def train_step(self, features: Dict[Text, tf.Tensor]):

        # Set up a gradient tape to record gradients.
        with tf.GradientTape() as tape:

            # Loss computation.
            user_embeddings = self.user_model(features["user_id"])
            positive_med_embeddings = self.medicine_model(
                features["medicine_name"])
            loss = self.task(user_embeddings, positive_med_embeddings)

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

        return metrics

    def test_step(self, features: Dict[Text, tf.Tensor]):

        # Loss computation.
        user_embeddings = self.user_model(features["user_id"])
        positive_med_embeddings = self.medicine_model(
                                    features["medicine_name"])
        loss = self.task(user_embeddings, positive_med_embeddings)

        # Handle regularization losses as well.
        regularization_loss = sum(self.losses)

        total_loss = loss + regularization_loss

        metrics = {metric.name: metric.result() for metric in self.metrics}
        metrics["loss"] = loss
        metrics["regularization_loss"] = regularization_loss
        metrics["total_loss"] = total_loss

        return metrics
