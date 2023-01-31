__author__ = "Miroslav Burýšek"

import logging

from parseJSON import *
from saveToDatabase import *

# Uncomment the lines for creating a log file
logging.basicConfig(
    level=logging.INFO,
    #filename="app.log",
    #filemode="w+",
    format="%(process)d- %(name)s - %(levelname)s - %(message)s",
)


def main():
    logging.info("Process started")
    filename = "sample-data.json"
    data = load_json(filename)

    db = initialize_MySQL()
    save_to_database(db, create_containers_from_json(data))

    logging.info("Success")


if __name__ == "__main__":
    main()
