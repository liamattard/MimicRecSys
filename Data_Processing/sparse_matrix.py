import pickle
import numpy as np
import tensorflow.compat.v1 as tf  # type: ignore
import pandas as pd
from Data_Processing.CFModel import CFModel


def build_sparse_matrix(dataset, users, medicine):
    return tf.sparse.SparseTensor(
        indices=dataset.values,
        values=np.ones(len(dataset.values)),
        dense_shape=[users.shape[0], medicine.shape[0]])


def split_dataframe(df, holdout_fraction=0.1):
    test = df.sample(frac=holdout_fraction, replace=False)
    train = df[~df.index.isin(test.index)]
    return train, test


def sparse_mean_square_error(sparse_matrix, user_embeddings,
                             medicine_embeddings):

    predictions = tf.reduce_sum(
      tf.gather(user_embeddings, sparse_matrix.indices[:, 0]) *
      tf.gather(medicine_embeddings, sparse_matrix.indices[:, 1]),
      axis=1)
    loss = tf.losses.mean_squared_error(sparse_matrix.values, predictions)
    return loss


def build_model(dataset, users, medicine, embedding_dim=3,
                init_stdev=0.5):
    train, test = split_dataframe(dataset)
    A_train = build_sparse_matrix(train, users, medicine)
    A_test = build_sparse_matrix(test, users, medicine)

    # Initialize the embeddings using a normal distribution.
    U = tf.Variable(tf.random_normal(
      [A_train.dense_shape[0], embedding_dim], stddev=init_stdev))
    V = tf.Variable(tf.random_normal(
      [A_train.dense_shape[1], embedding_dim], stddev=init_stdev))
    train_loss = sparse_mean_square_error(A_train, U, V)
    test_loss = sparse_mean_square_error(A_test, U, V)
    metrics = {
      'train_error': train_loss,
      'test_error': test_loss
    }
    embeddings = {
      "user_id": U,
      "medicine_id": V
    }
    return CFModel(embeddings, train_loss, [metrics])


def start():
    dataset_file = open('Data/dataset.pickle', 'rb')
    users_file = open('Data/users.pickle', 'rb')
    medicine_file = open('Data/medicine.pickle', 'rb')

    dataset = pickle.load(dataset_file)
    users = pickle.load(users_file)
    medicine = pickle.load(medicine_file)

    dataset = pd.DataFrame(dataset, columns=['User', 'Medicine'])
    users = pd.DataFrame(users, columns=['user_key', 'user_value'])
    medicine = pd.DataFrame(medicine, columns=['medicine_key',
                                               'medicine_value'])

    model = build_model(dataset, users, medicine, embedding_dim=30,
                        init_stdev=0.5)

    model.train(num_iterations=100, learning_rate=10)


