# -*- coding: utf-8 -*-
import csv
import os
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


class Cluster:
    def single_cluster(self, user_id, eps, min_stamples):
        staypoints = self.__load_staypoints(user_id)
        db = DBSCAN(eps=eps, min_samples=min_stamples).fit(staypoints)
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

            cluster_center_points.append([mean_la, mean_lo])
        return cluster_center_points


    def plot(self, clusters, ignore_nodes, mode=0):
        colors = plt.cm.Spectral(np.linspace(0, 1, len(clusters)))

        fig = plt.figure(2)
        plt.title('DBSCAN :Estimated number of clusters: %d' % len(clusters))

        for i in range(len(clusters)):
            plt.plot(clusters[i][:, 0], clusters[i][:, 1], 'o',
                     markerfacecolor=colors[i],
                     markeredgecolor='k', markersize=10)

        if mode ==1 :
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

if __name__ == '__main__':
    c = Cluster()
    cluster, ignore_nodes = c.single_cluster(1, 0.001, 10)
    points = c.cal_mean(cluster)
    print points
    c.plot(clusters=cluster, ignore_nodes=ignore_nodes)
