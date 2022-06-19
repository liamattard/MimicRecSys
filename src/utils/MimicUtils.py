def number_of_unique_medicine(medicine_dataset):
    unique_medicine_titles = set(medicine_dataset.as_numpy_iterator())
    print("number of unique medicine: ", len(unique_medicine_titles))
