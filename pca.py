from sklearn.metrics import jaccard_score

import _pickle
import Data_Processing.database_tools as db
import numpy as np
import pandas as pd


def main():
    db.connect()

    diagnosis = db.query(
        "SELECT "
        + "diagnoses_icd.hadm_id, "
        + "d_icd_diagnoses.row_id "
        + "FROM diagnoses_icd, d_icd_diagnoses "
        + "WHERE diagnoses_icd.icd9_code = d_icd_diagnoses.icd9_code"
    )

    # TODO: Get a list of hadm_ids where no medicine is set

    visit_map = {}

    for diagnose in diagnosis:
        diagnose_array = np.zeros([1, 14566])
        hadm_id = int(diagnose[0])
        icd9_code = diagnose[1]

        if hadm_id not in visit_map:
            visit_map[hadm_id] = [diagnose_array]
            visit_map[hadm_id][0][0, (int(icd9_code) - 1)] = 1
        else:
            visit_map[hadm_id][0][0, (int(icd9_code) - 1)] = 1


    df = pd.DataFrame(visit_map).T

    df.to_pickle("./diagnosis.pkl")

    # with open("diagnosis.pickle", "wb") as f:
    #     pickle.dump(df.T, f)

def calculate_jaccard():

    with open("diagnosis.pickle", "rb") as f:
        my_df= pickle.load(f)

        print(jaccard_score(my_df[22], my_df[22]))
    # admissions = db.query("select subject_id,hadm_id from admissions Order by hadm_id")

    # user_diagnosis_map = {}

    # for admission in admissions:
    #     user_id = int(admission[0])
    #     visit_id = int(admission[1])
    #     if user_id not in user_diagnosis_map():


if __name__ == "__main__":
    main()
