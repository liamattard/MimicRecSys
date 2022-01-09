import Data_Processing.database_tools as db

def start():

    # TODO: make all values contain 3 

    print("Setting up database connection")
    db.connect()

    diagnosis = db.query("select hadm_id,seq_num,icd9_code from mimiciii.diagnoses_icd")
    visit_map = create_visit_diagnosis_map(diagnosis)

    procedures = db.query("select hadm_id,seq_num,icd9_code from mimiciii.procedures_icd")
    visit_map = create_visit_procedures_map(visit_map, procedures)

    prescriptions = db.query("select hadm_id,ndc from mimiciii.prescriptions")
    visit_map = create_visit_prescriptions_map(visit_map, prescriptions)

    admissions = db.query("select subject_id,hadm_id from mimiciii.admissions")
    user_visit_map = create_user_visit_map(admissions, visit_map)

    print(len(user_visit_map[68]))
        

def create_visit_diagnosis_map(diagnosis):

    visit_map = {}

    for diagnose in diagnosis:
        hadm_id = int(diagnose[0])

        seq_num = diagnose[1]

        icd9_code = diagnose[2]

        diagnose_value =  [seq_num,icd9_code]

        if not hadm_id in visit_map:
            visit_map[hadm_id] = [[diagnose_value]]
        else:
            visit_map[hadm_id][0].append(diagnose_value)

    return visit_map 

def create_visit_procedures_map(visit_map, procedures):

    for procedure in procedures:
        hadm_id = int(procedure[0])

        seq_num = int(procedure[1])
        icd9_code = int(procedure[2])

        procedure_value =  [seq_num, icd9_code]

        if not hadm_id in visit_map:
            visit_map[hadm_id] = [[],[procedure_value]]
        else:
            if len(visit_map[hadm_id]) < 2:

                visit_map[hadm_id] = [visit_map[hadm_id][0],[procedure_value]]

            else:
                visit_map[hadm_id][1].append(procedure_value)

    return visit_map 

def create_visit_prescriptions_map(visit_map, prescriptions):

    for prescription in prescriptions:
        hadm_id = prescription[0]

        drug_code = prescription[1]

        if not hadm_id in visit_map:
            visit_map[hadm_id] = [[],[],[drug_code]]
        else:
            if len(visit_map[hadm_id]) == 1:
                visit_map[hadm_id] = [visit_map[hadm_id][0],[],[drug_code]]
            if len(visit_map[hadm_id]) == 2 :
                visit_map[hadm_id] = [visit_map[hadm_id][0],visit_map[hadm_id][1],[drug_code]]
            else:

                visit_map[hadm_id][2].append(drug_code)

    return visit_map 

def create_user_visit_map(admissions, visit_map):

    user_visit_map = {}

    for admission in admissions:

        user_id = int(admission[0])
        visit_id = int(admission[1])

        if not user_id in user_visit_map:
            user_visit_map[user_id] = [visit_map[visit_id]]
        else:
            user_visit_map[user_id].append(visit_map[visit_id])

    return user_visit_map