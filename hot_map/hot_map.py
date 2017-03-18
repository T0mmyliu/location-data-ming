# -*- coding: utf-8 -*-
import os

class GpsInfo:
    def __init__(self, lng, lat):
        self.lng = float(lng)
        self.lat = float(lat)

class HotMap:
    def __init__(self):
        self.raw_data_dir = '../data/raw'
        self.raw_data_files = {}
        self.user_hot_map_data = {}
        self.__setup__()

    def gen_hot_map_data(self, user_id):
        files = self.__get_raw_data_files_by_id(user_id)
        dps_datas = []
        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    datas = line.split(",")
                    if len(datas) == 7:
                        gps_info = {}
                        gps_info["lng"], gps_info["lat"], gps_info["count"] = datas[1], datas[0], 1
                        dps_datas.append(gps_info)
        self.user_hot_map_data[user_id] = dps_datas

    def dump_hot_map_data(self, user_id):
        pass

    def __get_raw_data_files_by_id(self, user_id):
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
    hot_map.gen_hot_map_data(1)
    print hot_map.user_hot_map_data[1]
