from src.utils.model_types import Model_Type

import src.data_handler.modelDataGenerator as data_generator
import src.utils.database_utils as db
import src.utils.query_handler as query_handler

import pandas as pd
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
    user_med_pd, med_set, past_med_arr = load()
    return generate(model_type, user_med_pd, med_set, past_med_arr)


def save(db):

    user_med_list, med_set, past_medicine_array = query_handler.load(db)
    user_medicine_pd = pd.DataFrame(
                            user_med_list,
                            columns=['subject_id', 'drug', 'drug_id',
                                     'has_past_medicine'])

    with open(config["DATASET"]["medicine_set"], 'wb') as handle:
        pickle.dump(med_set, handle)

    with open(config["DATASET"]["user_med_pd"], 'wb') as handle:
        pickle.dump(user_medicine_pd, handle)

    with open(config["DATASET"]["past_med_arr"], 'wb') as handle:
        pickle.dump(past_medicine_array, handle)


def load():
    log.info("Starting loading dataset from directory")

    med_set = pickle.load(open(config["DATASET"]["medicine_set"], 'rb'))
    user_med_pd = pickle.load(open(config["DATASET"]["user_med_pd"], 'rb'))
    past_med_arr = pickle.load(open(config["DATASET"]["past_med_arr"], 'rb'))

    return user_med_pd, med_set, past_med_arr


def generate(model_type, user_med_pd, med_set, past_med_arr):

    log.info("Starting generating dataset for model type: " + str(model_type))

    if(model_type == Model_Type.pure_collaborative):
        return data_generator.generate_pure_coll(user_med_pd, med_set)

    if(model_type == Model_Type.pure_sequential):
        return data_generator.generate_pure_seq(user_med_pd, med_set,
                                                past_med_arr)
