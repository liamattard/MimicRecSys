from src.utils.model_types import Model_Type
from wandb.keras import WandbCallback

import src.models.colabFiltering as pure_collaborative

import tensorflow_recommenders as tfrs
import tensorflow as tf
import wandb


def train(dataset, model_type):
    wandb.init(project="mimicRecSys", entity="liam_dratta")

    if(model_type == Model_Type.pure_collaborative):
        wandb.config = {
          "learning_rate": 0.1,
          "epochs": 10,
          "batch_size": 8192
        }
        model = pure_collaborative.Model(dataset)
        model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))

        cached_train = dataset.train.shuffle(100_000).batch(8192).cache()
        cached_test = dataset.test.batch(4096).cache()
        model.fit(cached_train, epochs=10, callbacks=[WandbCallback()])
        model.evaluate(cached_test, return_dict=True)

        index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)

        tf.saved_model.save(index, "saved_models/pure_collaborative")

