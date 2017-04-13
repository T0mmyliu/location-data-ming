# -*- coding: utf-8 -*-
import csv
import os
import numpy as np
import json
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import sys
sys.path.append("..")
from base import gps_record
from tool import gps_transfer

class Cluster:
    def __init__(self):
        self.raw_data_dir = '../data/stay_point'
        self.raw_data_files = {}
        self.__setup__()

    def single_cluster(self, user_id, eps):
        staypoints = self.__load_staypoints_v2(user_id)
        print len(staypoints)
        min_samples = len(staypoints)/15
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(staypoints)
        clusters, ignore_nodes = self.__parse_dbscan_result(db, staypoints)
        return clusters, ignore_nodes

    def cal_mean(self, clusters):
        cluster_center_points = []
        for cluster in clusters:
            la = 0
            lo = 0
            for point in cluster:
                la += point[1]
                lo += point[0]
            mean_la = la/len(cluster)
            mean_lo = lo/len(cluster)

            cluster_center_points.append([mean_lo, mean_la])
        return cluster_center_points


    def plot(self, clusters, ignore_nodes, mode=1):
        colors = plt.cm.Spectral(np.linspace(0, 1, len(clusters)))

        fig = plt.figure(2)
        plt.title('DBSCAN :Estimated number of clusters: %d' % len(clusters))

        for i in range(len(clusters)):
            plt.plot(clusters[i][:, 0], clusters[i][:, 1], 'o',
                     markerfacecolor=colors[i],
                     markeredgecolor='k', markersize=10)

        if mode == 1 :
            if len(ignore_nodes):
                plt.plot(ignore_nodes[:, 0], ignore_nodes[:, 1], 'o',
                         markeredgecolor='k', markersize=3)

        plt.show()

    def __parse_dbscan_result(self, db, staypoints):
        labels = db.labels_
        unique_labels = set(labels)

        clusters = []
        ignore_nodes = []

        for k in unique_labels:
            class_member_mask = (labels == k)
            xy = staypoints[class_member_mask]
            if k == -1:
                ignore_nodes = xy
            else:
                clusters.append(xy)

        return clusters, ignore_nodes

    def __load_staypoints(self, user_id):
        staypoints = []
        csv_name = "staypoints_%s.csv" % user_id
        path = os.path.join("../data/stay_point", csv_name)
        with open(path, "rb") as csvfp:
            reader = csv.reader(csvfp)
            for line in reader:
                staypoints.append(line)
        staypoints = np.array(staypoints, np.float)
        return staypoints

    def __load_staypoints_v2(self, user_id):
        staypoints = []
        files = self.__get_raw_data_files_by_id(user_id)
        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    datas = line.split(" ")
                    if len(datas) == 4:
                        staypoint = []
                        staypoint.append(float(datas[0]))
                        staypoint.append(float(datas[1]))
                        staypoints.append(staypoint)
        staypoints = np.array(staypoints, np.float)
        return staypoints

    def __setup__(self):
        self.__get_all_user_files()

    def __get_all_user_files(self):
        for dirname, dirnames, filenames in os.walk(self.raw_data_dir):
            if dirname.endswith("Trajectory"):
                names = dirname.split("/")
                self.raw_data_files[int(names[3])] = \
                    list([os.path.join(dirname, filename) for filename in filenames])

    def __get_raw_data_files_by_id(self, user_id):
        if user_id in self.raw_data_files:
            return self.raw_data_files[user_id]

    def dump_to_data(self, cluster_points, user_id):
        coords = []

        for point in cluster_points:
            coord = gps_record.gps_record()
            coord.gps_latitude = point[0]
            coord.gps_longitude = point[1]
            coords.append(coord)
        coords = gps_transfer.convert_coordinate_batch(coords)

        gps_datas = []
        for coord in coords:
            gps_info = {}
            gps_info["lat"], gps_info["lng"], gps_info["count"] = round(coord.gps_latitude, 6), \
                                                                  round(coord.gps_longitude, 6), 1
            gps_datas.append(gps_info)
        json_path = str(user_id) + ".json"
        with open(os.path.join("../data/cluster_point_baidu", json_path), 'w') as outfile:
            json_file = {}
            json_file["gps"] = gps_datas
            json.dump(json_file, outfile)


if __name__ == '__main__':
    c = Cluster()
    cluster, ignore_nodes = c.single_cluster(2, 0.003)
    points = c.cal_mean(cluster)
    c.dump_to_data(points, 2)
    c.plot(clusters=cluster, ignore_nodes=ignore_nodes)
