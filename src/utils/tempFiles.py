import dill
import pickle

subject_ids = dill.load(open('Data/test_subject_ids.pkl', 'rb'))

my_data_set = pickle.load(open('Data/SOTA/dataset.pickle', 'rb'))

dataset_subject_ids = set(my_data_set['subject_id'].unique())

for i in subject_ids:
    if(i not in dataset_subject_ids):
        print(i)
    else:
        print('ok for ' + str(i))

print(len((subject_ids)))
