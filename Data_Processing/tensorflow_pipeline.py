import Data_Processing.database_tools as db
import tensorflow as tf
import logging
import pickle

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tensorflow_pipeline")


def start(should_create=False):
    log.info("DATA PREPROCESSING: Started Building Tensorflow Pipleline")

    if(should_create):
        log.debug("Creating Dataset Using Database")

        db.connect()
        user_list, medicine_list = create_array_from_database(db)

        dump_array_to_pickle(user_list, medicine_list)

    user_list, medicine_list = load_array_from_pickle()

    log.info("DATA PREPROCESSING: Finished Building Tensorflow Pipleline")
    return create_tensorflow_pipeline(user_list, medicine_list)


def create_array_from_database(db):
    log.info("DATA PREPROCESSING: Starting querying data from database")
    user_medicine_list = db.query(
        "SELECT "
        + "drug,"
        + "subject_id "
        + "FROM prescriptions"
    )

    user_medicine_list = user_medicine_list[0:1000000]
    medicine_list = [i[0] for i in user_medicine_list]
    user_list = [i[1] for i in user_medicine_list]
    log.info("DATA PREPROCESSING: Finished querying data from database")

    return user_list, medicine_list


def dump_array_to_pickle(user_list, medicine_list):
    log.info("Starting dumping array to pickle")
    with open('Data/medicine_list.pickle', 'wb') as handle:
        pickle.dump(medicine_list, handle)

    with open('Data/user_list.pickle', 'wb') as handle:
        pickle.dump(user_list, handle)

    log.info("Finished dumping array to pickle")


def load_array_from_pickle():
    log.info("Starting loading array from pickle")
    user_pickle = open('Data/user_list.pickle', 'rb')
    medicine_pickle = open('Data/medicine_list.pickle', 'rb')

    user_list = pickle.load(user_pickle)
    medicine_list = pickle.load(medicine_pickle)
    log.info("Finished loading array from pickle")
    return user_list, medicine_list


def create_tensorflow_pipeline(user_list, medicine_list):
    log.info("Starting generating tensors from arrays")
    medicine_set = set(medicine_list)

    user_medicine_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name': medicine_list,
                                            'user_id': [str(i) for i in
                                                        user_list]})
    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(medicine_set))
    log.info("Finished generating tensors from arrays")

    return user_medicine_dataset, medicine_dataset
