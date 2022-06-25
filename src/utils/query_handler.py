import numpy as np
queries_base_path = "sql_queries/"


def load_user_age_map(db):

    age_query = open(queries_base_path + "getAge.sql").read()
    user_age_list = db.query(age_query)
    user_age_map = dict(user_age_list)

    return user_age_map


def load_user_gender_map(db):

    gender_query = open(queries_base_path + "getGender.sql").read()
    user_gender_list = db.query(gender_query)
    user_gender_map = dict(user_gender_list)

    return user_gender_map


def load_ordered_visits(db):

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


def load_medicine_values_by_visit(db):

    medicine_query = open(queries_base_path +
                          "getMedicineValuesByVisit.sql").read()
    visit_medicine_list = db.query(medicine_query)
    visit_medicine_map = dict(visit_medicine_list)

    return visit_medicine_map


def load_medicine_values_by_user(db):

    medicine_query = open(queries_base_path + "getUniqueMedicine.sql").read()
    medicine_list = db.query(medicine_query)
    medicine_list = list(map(lambda x: x[0], medicine_list))

    medicine_query = open(queries_base_path +
                          "getMedicineValuesByUser.sql").read()
    user_medicine_list = db.query(medicine_query)

    return user_medicine_list, medicine_list
