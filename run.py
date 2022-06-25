from src.train import train
from src.utils.model_types import Model_Type

import src.data_handler.start as load_data


def main():

    # Load Data
    dataset = load_data.start(Model_Type.pure_collaborative)

    # Train Model
    train(dataset, Model_Type.pure_collaborative)


if __name__ == "__main__":
    main()
