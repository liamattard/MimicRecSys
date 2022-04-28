import Data_Processing.create_tensors as preprocessing
import RetrievalSystem.retrieval as retrieval


def main():

    user_medicine_dataset, medicine_dataset = preprocessing.start(
                                               file='Data/SOTA/dataset.pickle')
    retrieval.start_train(user_medicine_dataset, medicine_dataset)

    # retrieval.import_model('Data/model')


if __name__ == "__main__":
    main()
