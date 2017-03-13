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


        labels = db.labels_

        num_cluster = len(set(labels)) - (1 if -1 in labels else 0)

        print num_cluster

        unique_labels = set(labels)

        print unique_labels


        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

        fig = plt.figure(2)
        centerPoint = []

        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True

        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = 'k'

            class_member_mask = (labels == k)

            xy = staypoints[class_member_mask & core_samples_mask]

            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                     markeredgecolor='k', markersize=14)

        plt.title('DBSCAN :Estimated number of clusters: %d' % num_cluster)

        plt.show()

    def __load_staypoints(self, user_id):
        staypoints = []
        csv_name = "staypoints_%s.csv" % user_id
        path = os.path.join("../stay_point", csv_name)
        with open(path, "rb") as csvfp:
            reader = csv.reader(csvfp)
            for line in reader:
                staypoints.append(line)
        staypoints = np.array(staypoints, np.float)
        return staypoints

if __name__ == '__main__':

    c = Cluster()
    c.single_cluster(1, 0.01, 10)

