import os
import logging
import sys
import glob




def get_folder_files(path=r"data/images", extension="*.jpg", reverse=True):
    path = path + "/" + extension
    list_of_files = glob.glob(path)  # * means all if need specific format then *.csv
    list_of_files.sort(key=os.path.getmtime, reverse=reverse)
    return list_of_files

"""
Checks if the folder exits and creates it if it does not
"""
def create_folder(directory_path: str) -> bool:
  if (not os.path.exists(directory_path)):
      os.makedirs(directory_path)
  return os.path.normpath(directory_path)


if __name__ == "__main__":
    get_folder_files()
