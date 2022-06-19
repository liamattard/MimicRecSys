import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("Data processor")

queries_base_path = "src/utils/sql_queries/"


def build(db):
    user_age_map = __load_user_age_map(db)
    user_gender_map = __load_user_gender_map(db)
    user_visit_map,visit_number_map = __load_ordered_visits(db)
    breakpoint()


def __load_user_age_map(db):

    age_query = open(queries_base_path + "getAge.sql").read()
    user_age_list = db.query(age_query)
    user_age_map = dict(user_age_list)

    return user_age_map


def __load_user_gender_map(db):

    gender_query = open(queries_base_path + "getGender.sql").read()
    user_gender_list = db.query(gender_query)
    user_gender_map = dict(user_gender_list)

    return user_gender_map


def __load_ordered_visits(db):

    patient_query = open(queries_base_path + "getPatients.sql").read()
    patient_list = db.query(patient_query)
    patient_list = list(map(lambda x: x[0], patient_list))
    patient_visits_count = np.zeros(len(patient_list))
    patient_count_map = dict(zip(patient_list, patient_visits_count))

    visit_query = open(queries_base_path + "getOrderedVisits.sql").read()
    user_visit_list = db.query(visit_query)
    visit_count_map = {}

    for visit in user_visit_list:

        visit_count_map[visit[1]] = patient_count_map[visit[0]]
        patient_count_map[visit[0]] = patient_count_map[visit[0]] + 1

    user_visit_map = dict(map(lambda x: (x[1], x[0]), user_visit_list))

    return user_visit_map, visit_count_map

