from src.train import train
from src.utils.model_types import Model_Type

import src.data_handler.start as load_data
import tensorflow as tf


def main():

    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

    model_type = Model_Type.pure_collaborative

    # Load Data
    dataset = load_data.start(model_type)

    # Train Model
    train(dataset, model_type)


if __name__ == "__main__":
    main()
