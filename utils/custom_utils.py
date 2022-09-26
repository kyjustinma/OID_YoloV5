import os
import logging
import sys
import glob
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s",
    level=int(config["VERBOSE"]),
    stream=sys.stdout,
)


def get_folder_files(path=r"data/images", extension="*.jpg", reverse=True):
    path = path + "/" + extension
    list_of_files = glob.glob(path)  # * means all if need specific format then *.csv
    list_of_files.sort(key=os.path.getmtime, reverse=reverse)

    return list_of_files


if __name__ == "__main__":
    get_folder_files()
