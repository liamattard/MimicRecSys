import src.data_handler.load_data as load_data


def main():

    load_data.start()

    # user_medicine_dataset, medicine_dataset = preprocessing.start(
                                               # file='Data/SOTA/dataset.pickle')
    # breakpoint()

    # retrieval.start_train(user_medicine_dataset, medicine_dataset)

    # model = retrieval.import_model('Data/model')
    # print(retrieval.get_user_recommendations("100", model))


if __name__ == "__main__":
    main()
