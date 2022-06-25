from src.train import train
from src.utils.model_types import Model_Type

import src.data_handler.start as load_data


def main():

    model_type = Model_Type.pure_sequential

    # Load Data
    dataset = load_data.start(model_type)

    # Train Model
    train(dataset, model_type)


if __name__ == "__main__":
    main()
