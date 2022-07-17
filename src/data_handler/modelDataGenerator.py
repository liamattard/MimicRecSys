from src.utils.classes.Dataset import Dataset
from sklearn.model_selection import train_test_split

import tensorflow as tf
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("Data loader")


def generate_pure_coll(user_med_pd, med_set):
    user_med_pd = user_med_pd.astype('string')
    user_med_pd = user_med_pd.drop_duplicates()
    user_med_pd = user_med_pd.drop(
                    ['drug_id', 'has_past_medicine'], axis=1)
    user_med_pd = user_med_pd.sample(frac=1, random_state=1).reset_index()

    train_pd, test_pd = train_test_split(
        user_med_pd, test_size=0.2, shuffle=False)

    user_med_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            user_med_pd['drug'],
                                         'user_id':
                                            user_med_pd['subject_id']})

    train = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            train_pd['drug'],
                                         'user_id':
                                            train_pd['subject_id']})

    test = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            test_pd['drug'],
                                         'user_id':
                                            test_pd['subject_id']})

    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(med_set))

    tf.random.set_seed(42)

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


def generate_pure_seq(user_med_pd, med_set, past_medicine_array):

    user_med_pd.drug_id = user_med_pd.drug_id.astype('string')

    user_med_pd = user_med_pd[user_med_pd.has_past_medicine]

    # TODO: Remove these
    past_medicine_array = past_medicine_array[0:100]
    user_med_pd = user_med_pd.head(100)

    user_med_dataset = tf.data.Dataset.from_tensor_slices(
                                        {'medicine_name':
                                            user_med_pd['drug_id'],
                                         'past_medicine':
                                            past_medicine_array})

    medicine_dataset = tf.data.Dataset.from_tensor_slices(list(med_set))

    unique_med_ids = np.unique(med_set)

    tf.random.set_seed(42)
    shuffled = user_med_dataset.shuffle(100_000, seed=42,
                                        reshuffle_each_iteration=False)

    train = shuffled.take(80_000)

    dataset = Dataset(unique_medicine_ids=unique_med_ids,
                      medicine_dataset=medicine_dataset,
                      train=train)

    return dataset
