# -*- coding: utf-8 -*-
import os

class HotMap:
    def __init__(self):
        self.raw_data_dir = '../data/raw'
        self.raw_data_files = {}
        self.__setup__()

    def get_hot_map_data_from_raw(self, user_id):
        pass

    def get_raw_data_files_by_id(self, user_id):
        if user_id in self.raw_data_files:
            return self.raw_data_files[user_id]

    def __setup__(self):
        self.__get_all_user_files()

    def __get_all_user_files(self):
        for dirname, dirnames, filenames in os.walk(self.raw_data_dir):
            if dirname.endswith("Trajectory"):
                names = dirname.split("/")
                self.raw_data_files[int(names[3])] = \
                    list([os.path.join(dirname, filename) for filename in filenames])






if __name__ == "__main__":
    hot_map = HotMap()
    files = hot_map.get_raw_data_files_by_id(0)


