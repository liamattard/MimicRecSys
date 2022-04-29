import Data_Processing.database_tools as db
import Utils.medicineUtils as medUtils
import tensorflow as tf
import logging
import pickle
import pandas as pd
import dill
import os

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tensorflow_pipeline")


def start(file=None, number_of_users=None, from_sota=False):
    log.info("DATA PREPROCESSING: Started Creating/Fetching Data")

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

    log.info("DATA PREPROCESSING: Finished Creating/Fetching Data")
    return create_tensorflow_pipeline(user_medicine_list)


def load_sota_values(user_medicine_list):
    user_medicine_list = medUtils.convert_to_atc_using_safedrug(
                           user_medicine_list,
                           'Data/rxnorm2RXCUI.txt',
                           'Data/RXCUI2atc4.csv')

    voc_final = dill.load(open('Data/voc_final.pkl', 'rb'))
    medicine_list = [*voc_final['med_voc'].word2idx]
    user_medicine_list = user_medicine_list[
                            user_medicine_list['ATC3'].isin(
                                medicine_list)]

    # remove all users that only took one medicine
    user_medicine_list = user_medicine_list[
                            user_medicine_list.subject_id.duplicated(
                                keep=False)]

    # remove all users that are in the SOTA testing set
    sota_testing_set = dill.load(open('Data/test_subject_ids.pkl', 'rb'))

    user_medicine_list = user_medicine_list[
                            ~user_medicine_list.subject_id.isin(
                                sota_testing_set)]

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
    log.info("Starting generating tensors from arrays")

    user_medicine_list = user_medicine_list.astype('string')
    user_medicine_list = user_medicine_list.drop_duplicates()
    user_medicine_list.drop(columns=['ATC3'], inplace=True)

    medicine_set = set(user_medicine_list['drug'])

    user_medicine_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            user_medicine_list['drug'],
                                         'user_id':
                                            user_medicine_list['subject_id']})

    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(medicine_set))
    log.info("Finished generating tensors from arrays")

    return user_medicine_dataset, medicine_dataset
