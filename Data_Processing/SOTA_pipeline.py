import Data_Processing.database_tools as db
import tensorflow as tf
import logging
import pickle
import pandas as pd
import dill
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tensorflow_pipeline")


def start(file=None, number_of_users=None, from_sota=False):
    log.info("DATA PREPROCESSING: Started Building Tensorflow Pipleline")

    if file is None:
        log.debug("Building Dataset From Database")
        db.connect()
        user_medicine_list = create_array_from_database(db, number_of_users)
        user_medicine_list = pd.DataFrame(
                                user_medicine_list,
                                columns=['NDC', 'drug', 'subject_id'])
        if from_sota:
            log.info("Building Dataset From SOTA")
            user_medicine_list = load_sota_values(user_medicine_list)
        dump_array_to_pickle(user_medicine_list, number_of_users, from_sota)

    else:
        log.debug("Fetching Dataset From File" + file)
        user_medicine_list = load_array_from_pickle(file)

    return create_tensorflow_pipeline(user_medicine_list)
    log.info("DATA PREPROCESSING: Finished Building Tensorflow Pipleline")


def convert_to_atc(med_pd, rxnorm2RXCUI_file, RXCUI2atc4_file):
    with open(rxnorm2RXCUI_file, 'r') as f:
        rxnorm2RXCUI = eval(f.read())
    med_pd['RXCUI'] = med_pd['NDC'].map(rxnorm2RXCUI)
    med_pd.dropna(inplace=True)

    rxnorm2atc4 = pd.read_csv(RXCUI2atc4_file)
    rxnorm2atc4 = rxnorm2atc4.drop(columns=['YEAR', 'MONTH', 'NDC'])
    rxnorm2atc4.drop_duplicates(subset=['RXCUI'], inplace=True)
    # Dahal ATC4

    med_pd.drop(index=med_pd[med_pd['RXCUI'].isin([''])].index, axis=0, inplace=True)
    med_pd['RXCUI'] = med_pd['RXCUI'].astype('int64')
    med_pd = med_pd.reset_index(drop=True)
    med_pd = med_pd.merge(rxnorm2atc4, on=['RXCUI'])
    med_pd.drop(columns=['NDC', 'RXCUI'], inplace=True)
    med_pd['ATC4'] = med_pd['ATC4'].map(lambda x: x[:4])
    med_pd = med_pd.rename(columns={'ATC4': 'ATC3'})
    med_pd = med_pd.drop_duplicates()
    med_pd = med_pd.reset_index(drop=True)
    return med_pd


def load_sota_values(user_medicine_list):
    user_medicine_list = convert_to_atc(
                            user_medicine_list,
                            'Data/rxnorm2RXCUI.txt',
                            'Data/RXCUI2atc4.csv')

    voc_final = dill.load(open('Data/voc_final.pkl', 'rb'))
    medicine_list = voc_final['med_voc'].word2idx.keys()
    user_medicine_list = user_medicine_list[
                            ~user_medicine_list['ATC3'].isin(
                                medicine_list)]
    return user_medicine_list


def create_array_from_database(db, number_of_users=None):
    log.info("DATA PREPROCESSING: Starting querying data from database")
    user_medicine_list = db.query(
        "SELECT "
        + "ndc,"
        + "drug,"
        + "subject_id "
        + "FROM prescriptions"
    )

    user_medicine_list = user_medicine_list[0:number_of_users]
    # medicine_list = [i[0] for i in user_medicine_list]
    # user_list = [i[1] for i in user_medicine_list]
    log.info("DATA PREPROCESSING: Finished querying data from database")

    return user_medicine_list


def dump_array_to_pickle(user_medicine_list, number_of_users, from_sota):
    log.info("Starting dumping array to pickle")
    folder_name = "Data/"
    if from_sota:
        folder_name = folder_name + "SOTA"
    else:
        folder_name = folder_name + "Database"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if number_of_users is not None:
        folder_name = folder_name + str(number_of_users)

    with open(folder_name + '/dataset.pickle', 'wb') as handle:
        pickle.dump(user_medicine_list, handle)

    log.info("Finished dumping array to pickle, DirectoryName: " + folder_name)


def load_array_from_pickle(fileName):
    log.info("Starting loading array from pickle")
    user_medicine_pickle = open(fileName, 'rb')

    user_medicine_list = pickle.load(user_medicine_pickle)
    log.info("Finished loading array from pickle")
    return user_medicine_list


def create_tensorflow_pipeline(user_medicine_list):
    # TODO: FIX THIS
    # TODO: CHeck if safedrug has less rows than my dataset

    log.info("Starting generating tensors from arrays")
    medicine_set = set(medicine_list)

    user_medicine_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name': medicine_list,
                                            'user_id': [str(i) for i in
                                                        user_list]})
    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(medicine_set))
    log.info("Finished generating tensors from arrays")

    return user_medicine_dataset, medicine_dataset
