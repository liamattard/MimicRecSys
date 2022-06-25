from src.utils.classes.Dataset import Dataset
from src.utils.model_types import Model_Type

import src.utils.database_utils as db
import src.utils.query_handler as query_handler

import tensorflow as tf
import pandas as pd
import numpy as np
import configparser
import logging
import pickle
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("Data loader")

config = configparser.ConfigParser()
config.sections()
config.read("properties.ini")


def start(model_type, from_sota=False):

    if not from_sota:
        dataset_exits = (os.path.exists(config["DATASET"]["medicine_set"]) and
                         os.path.exists(config["DATASET"]["user_med_pd"]))

        if not dataset_exits:
            log.info("Started generating the dataset using PostgreSQL server")

            db.connect()
            save(db)

    log.info("Started loading the dataset")
    user_med_pd, med_set = load()
    return fetch(model_type, user_med_pd, med_set)


def save(db):

    user_med_list, med_set = query_handler.load(db)
    user_medicine_pd = pd.DataFrame(
                            user_med_list,
                            columns=['subject_id', 'drug', 'past_medicine'])

    with open(config["DATASET"]["medicine_set"], 'wb') as handle:
        pickle.dump(med_set, handle)

    with open(config["DATASET"]["user_med_pd"], 'wb') as handle:
        pickle.dump(user_medicine_pd, handle)


def load():
    log.info("Starting loading dataset from directory")

    med_set = pickle.load(open(config["DATASET"]["medicine_set"], 'rb'))
    user_med_pd = pickle.load(open(config["DATASET"]["user_med_pd"], 'rb'))

    return user_med_pd, med_set


def fetch(model_type, user_med_pd, med_set):

    log.info("Starting generating dataset for model type: " + str(model_type))

    if(model_type == Model_Type.pure_collaborative):
        return generate_pure_coll(user_med_pd, med_set)

    if(model_type == Model_Type.pure_sequential):
        return generate_pure_seq(user_med_pd, med_set)


def generate_pure_coll(user_med_pd, med_set):
    user_med_pd = user_med_pd.astype('string')
    user_med_pd = user_med_pd.drop_duplicates()

    user_med_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            user_med_pd['drug'],
                                         'user_id':
                                            user_med_pd['subject_id']})

    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(med_set))

    tf.random.set_seed(42)
    shuffled = user_med_dataset.shuffle(100_000, seed=42,
                                        reshuffle_each_iteration=False)

    train = shuffled.take(80_000)
    test = shuffled.skip(80_000).take(20_000)

    med_titles = medicine_dataset.batch(1_000)
    user_ids = user_med_dataset.batch(1_000).map(lambda x: x['user_id'])

    unique_user_ids = np.unique(user_med_pd['subject_id'])
    unique_med_names = np.array(med_set)

    log.info("Finished loading dataset from directory")
    dataset = Dataset(unique_user_ids=unique_user_ids,
                      unique_medicine_names=unique_med_names,
                      user_medicine_dataset=user_med_dataset,
                      medicine_dataset=medicine_dataset,
                      medicine_titles=med_titles,
                      user_ids=user_ids,
                      train=train,
                      test=test)

    log.info("Finished generating dataset for model type: Pure Coll Model ")
    return dataset


def generate_pure_seq(user_med_pd, med_set):

    user_med_pd.subject_id = user_med_pd.subject_id.astype('string')
    user_med_pd = user_med_pd[user_med_pd.past_medicine.astype(bool)]

    user_med_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            user_med_pd['drug'],
                                         'past_medicine':
                                            user_med_pd['past_medicine']})

    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(med_set))
    breakpoint()

    return "x"
