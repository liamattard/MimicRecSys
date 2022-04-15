import Data_Processing.tensorflow_pipeline as tp
import RetrievalSystem.retrieval as retrieval


def main():
    # Currently only using 1000000 values

    user_medicine_dataset, medicine_dataset = tp.start(should_create=False)
    # retrieval.start_train(user_medicine_dataset, medicine_dataset)
    retrieval.import_model('Data/model')


if __name__ == "__main__":
    main()
