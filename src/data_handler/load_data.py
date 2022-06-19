import src.utils.database_utils as db
import src.data_handler.preprocess as preprocessing
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("Data loader")


def start(file=None, number_of_users=None, from_sota=False):
    build_dataset = file is None

    log.info("Started fetching data, preprocessing: " + str(build_dataset))

    if build_dataset:
        log.debug("Started building bataset from PostgreSQL database")

        db.connect()
        preprocessing.build(db)
