__author__ = "Miroslav Burýšek"

from parseJSON import *
from saveToDatabase import *


def main():
    filename = "sample-data.json"
    data = load_json(filename)
    # print_info_data(data)
    # print(create_containers_from_json(data))
    
    db = initialize_MySQL()
    save_to_database(db, create_containers_from_json(data))

if __name__ == "__main__":
    main()