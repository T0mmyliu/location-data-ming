# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
sys.path.append("..")
from base import gps_record
import json
import time
import json
import os
import gps_transfer


class GpsInfo:
    def __init__(self, lng, lat):
        self.lng = float(lng)
        self.lat = float(lat)

class DataTransferTool:
    def __init__(self):
        self.raw_data_dir = '../data/raw'
        self.raw_data_files = {}
        self.__setup__()

    def gen_baidu_data(self, user_id):
        files = self.__get_raw_data_files_by_id(user_id)
        raw_gps_datas = []
        baidu_gps_data = None
        for file in files:
            print file
            with open(file, 'r') as f:
                for line in f:
                    datas = line.split(",")
                    if len(datas) == 7:
                        point = gps_record.gps_record()
                        point.gps_longitude = round(float(datas[1]), 6)
                        point.gps_latitude = round(float(datas[0]), 6)
                        raw_gps_datas.append(point)

        print len(raw_gps_datas)
        baidu_gps_data = gps_transfer.convert_coordinate_batch(raw_gps_datas)

        json_dps_datas = []
        for point in baidu_gps_data:
            gps_info = {}
            gps_info["lng"], gps_info["lat"], gps_info["count"] = str(point.gps_longitude), str(point.gps_latitude), 1
            json_dps_datas.append(gps_info)

        json_path = str(user_id) + ".json"
        print len(json_dps_datas)
        with open(os.path.join("../data/baidu_gps", json_path), 'w') as outfile:
            json_file = {}
            json_file["gps"] = json_dps_datas
            json.dump(json_file, outfile)

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
    data_transfer_tool = DataTransferTool()
    data_transfer_tool.gen_baidu_data(2)



