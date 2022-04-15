import Data_Processing.database_tools as db
import pickle
import csv


def create_dataset(db):

    user_medicine_list = db.query(
        "SELECT "
        + "ndc, subject_id "
        + "FROM prescriptions"
    )

    medicine_set = set([i[0] for i in user_medicine_list])
    medicine_set.remove('0')

    user_set = set([i[1] for i in user_medicine_list])

    medicine_map = dict((i[1], i[0]) for i in enumerate(medicine_set))
    user_map = dict((i[1], i[0]) for i in enumerate(user_set))

    dataset = []

    for row in user_medicine_list:
        user_id = user_map[row[1]]

        if row[0] != '0':
            medicine_id = medicine_map[row[0]]
            dataset.append([user_id, medicine_id])

    # -----------------------------------------
    # Write the Dataset CSV File + pickle
    file = open('Data/dataset.csv', 'w+', newline='')

    with file:
        write = csv.writer(file)
        write.writerow(["user_id", "medicine_id"])
        write.writerows(dataset)

    with open('Data/dataset.pickle', "wb") as f:
        pickle.dump(dataset, f)

    # -----------------------------------------
    # Write the User Key CSV File + pickle
    file = open('Data/users.csv', 'w+', newline='')

    with file:
        write = csv.writer(file)
        write.writerow(["key", "value"])
        for user in user_map:
            write.writerow([user_map[user], user])

    with open('Data/users.pickle', "wb") as f:
        pickle.dump(list(map(list, user_map.items())), f)

    # -----------------------------------------
    # Write the Medicine Key CSV File + pickle
    file = open('Data/medicine.csv', 'w+', newline='')

    with file:
        write = csv.writer(file)
        write.writerow(["key", "value"])
        for medicine in medicine_map:
            write.writerow([medicine_map[medicine], medicine])

    with open('Data/medicine.pickle', "wb") as f:
        pickle.dump(list(map(list, medicine_map.items())), f)

    breakpoint()


print("Setting up database connection")
db.connect()
create_dataset(db)
