import Data_Processing.SOTA_pipeline as sotap


def main():
    # Currently only using 1000000 values

    # user_medicine_dataset, medicine_dataset = tp.start(should_create=False)
    # retrieval.start_train(user_medicine_dataset, medicine_dataset)
    sotap.start(from_sota=True)
    # retrieval.import_model('Data/model')


if __name__ == "__main__":
    main()
