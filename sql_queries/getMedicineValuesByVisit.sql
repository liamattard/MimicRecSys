SELECT hadm_id, drug
    FROM mimiciii.prescriptions
    WHERE drug NOT LIKE ' '
