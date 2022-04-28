import tensorflow as tf
import numpy as np
import wandb
import tensorflow_recommenders as tfrs

from wandb.keras import WandbCallback
from RetrievalSystem.model import build_model


def start_train(user_medicine_tensor, medicine_tensor):
    tf.random.set_seed(42)
    wandb.init(project="KerasRecSys", entity="liam_dratta")

    # Get our data and split it into a training and test set.

    shuffled = user_medicine_tensor.shuffle(
            100_000, seed=42, reshuffle_each_iteration=False)

    train = shuffled.take(80_000)
    test = shuffled.skip(80_000).take(20_000)

    medicine_titles = medicine_tensor.batch(1_000)
    user_ids = user_medicine_tensor.batch(1_000_000).map(lambda x:
                                                         x["user_id"])

    unique_medicine_list = np.unique(np.concatenate(list(medicine_titles)))
    unique_user_ids = np.unique(np.concatenate(list(user_ids)))

    # Implement a retrieval model.
    wandb.config = {
      "learning_rate": 0.1,
      "epochs": 20,
      "batch_size": 1_000
    }

    model = build_model(unique_user_ids, unique_medicine_list, medicine_tensor)

    # Fit and evaluate it.

    model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.1))
    cached_train = train.shuffle(100_000).batch(8192).cache()
    cached_test = test.batch(4096).cache()

    model.fit(cached_train, epochs=20, callbacks=[WandbCallback()])
    model.evaluate(cached_test, return_dict=True, callbacks=[WandbCallback()])

    # Export it for efficient serving by building an approximate nearest
    # neighbours (ANN) index.

    # Create a model that takes in raw query features, and
    # recommends medicine out of the entire medicine dataset.

    # Create a model that takes in raw query features, and
    index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
# recommends movies out of the entire movies dataset.
    index.index_from_dataset(
        tf.data.Dataset.zip((medicine_tensor.batch(100),
                             medicine_tensor.batch(100).map(
                                 model.medicine_model)))
    )

    # Get recommendations.
    _, titles = index(tf.constant(["42"]))
    print(f"Recommendations for user 42: {titles[0, :3]}")

    export_model(index)


def export_model(index):

    tf.saved_model.save(
        index,
        'Data/model',
    )


def import_model(path):
    loaded = tf.saved_model.load(path)

    _, results = loaded(tf.constant(["42"]))  # type: ignore

    print(f"Recommendations: {results[0][:3]}")
