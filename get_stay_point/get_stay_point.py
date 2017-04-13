# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from sql_base import dbutils
from base import base_op
from base.stay_point import StayPoint
import logging.config
import csv
import pickle
import json
from convert_coordinate import convert_coordinate
import os
from math import radians, cos, sin, asin, sqrt
import time

logger = None

column_name = ("gps_userid", "gps_latitude", "gps_longitude", "gps_code",\
       "gps_altitude", "gps_UTC_timestamp", "gps_UTC_unix_timestamp")

def log_init():
    global logger
    if(logger == None):
        logging.config.fileConfig("logger.conf")
        logger = logging.getLogger("root")
    return logger

def calc_mean_pos(s_point,tmp_points):
    i = 0;
    latitude_sum = 0
    longitude_sum = 0
    altitude_sum = 0
    
    for p in tmp_points:
        latitude_sum = p.gps_latitude + latitude_sum
        longitude_sum = p.gps_longitude + longitude_sum
        altitude_sum = p.gps_altitude + altitude_sum
        i = i + 1
    s_point.mean_coordinate_latitude = latitude_sum/i
    s_point.mean_coordinate_longtitude = longitude_sum/i
    s_point.mean_coordinate_altitude = altitude_sum/i
    s_point.arrival_timestamp = tmp_points[0].gps_UTC_unix_timestamp
    s_point.leaving_timestamp = tmp_points[i-1].gps_UTC_unix_timestamp
    s_point.arrival_point = tmp_points[0].id
    s_point.leaving_point = tmp_points[i-1].id
    return s_point

def get_stay_points(user_id, max_distence=200, max_time=20*60):
    gps_obj_list = dbutils.get_gps_record_time_order(user_id, 0, -1)
    stay_point_list = []
    gps_size = len(gps_obj_list)
    i = 0
    while i < gps_size:
        j = i + 1
        point_i = gps_obj_list[i]
        while (j < gps_size) :
            point_j = gps_obj_list[j]
            dist = get_distance(point_i.gps_longitude, point_i.gps_latitude,
                                point_j.gps_longitude, point_j.gps_latitude)
            if dist > max_distence:
                delta_time = point_j.gps_UTC_unix_timestamp - point_i.gps_UTC_unix_timestamp
                if delta_time > max_time:
                    stay_point = StayPoint()
                    stay_point.user_id = user_id
                    lo, la = compute_mean_coord(gps_obj_list[i:j+1])
                    stay_point.mean_coordinate_latitude = la
                    stay_point.mean_coordinate_longtitude = lo
                    stay_point.arrival_timestamp = point_i.gps_UTC_unix_timestamp
                    stay_point.leaving_timestamp = point_j.gps_UTC_unix_timestamp
                    stay_point_list.append(stay_point)

                    time_format = '%Y-%m-%d,%H:%M:%S'
                    print  stay_point.mean_coordinate_latitude, stay_point.mean_coordinate_longtitude,\
                        time.strftime(time_format, time.localtime(
                            stay_point.arrival_timestamp)), \
                        time.strftime(time_format, time.localtime(stay_point.leaving_timestamp))

                    i = j
                    break
            j += 1
        i += 1
    return stay_point_list

def get_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    m = 6371000 * c
    return m

def compute_mean_coord(gps_points):
    lon = 0.0
    lat = 0.0
    for point in gps_points:
        lon += point.gps_latitude
        lat += point.gps_longitude
    return (lon/len(gps_points), lat/len(gps_points))

def get_stay_points_list(user_id, mode=0, buffer_file_name="buffer"):
    if mode == 1:
        print "read from local file "
        mydb = open(buffer_file_name, 'r')
        stay_points_list = pickle.load(mydb)
    else:
        print "read from mysql"
        stay_points_list = get_stay_points(user_id)
        mydb = open(buffer_file_name, 'w')
        pickle.dump(stay_points_list, mydb) 
    return stay_points_list

    
def convert_staypoint_baidu_corrd(stay_points_list):
    orinArry = []
    for s in stay_points_list:
        p = []
        p.append(s.mean_coordinate_longtitude)
        p.append(s.mean_coordinate_latitude)
        orinArry.append(p)
    return convert_coordinate.convert_coordinate_batch_array(orinArry)
    
    
def saveStayPointsToJson(distPointList, filepath='', fileId = 0 ):
    if not distPointList:
        print "Null Value"
        return
    datalist = []
    for p in distPointList:
        data = []
        data.append(p.gps_longitude);
        data.append(p.gps_latitude);
        data.append(1);
        datalist.append(data);
    strTmp = "var data%d =" %fileId
    saveDate = {'data':datalist,'total':len(datalist),"rt_loc_cnt":47764510,"errorno":0,"NearestTime":"2014-08-29 15:20:00","userTime":"2014-08-29 15:32:11"}
    strTmp += json.dumps(saveDate,sort_keys=False)
    with open(filepath, "w") as fp:
        fp.write(strTmp)
    fp.close()

def saveStayPointsBaiduCoordToJson(stay_points_list,dirName,userid):
    stay_points_list_baidu = []
    stay_points_list_baidu = convert_staypoint_baidu_corrd(stay_points_list)
    filetype = ""
    filepath = "%s/points_staypoints_baidu_%d%s.js" %(dirName, userid,filetype)
    saveStayPointsToJson(stay_points_list_baidu, filepath)
    
def saveStayPointsToCsv(csv_name, stay_points_list):
    with open(csv_name,"wb") as csvfp:
        writer = csv.writer(csvfp)
        for p in stay_points_list:
             writer.writerow([p.mean_coordinate_latitude]+[p.mean_coordinate_longtitude]);
        print len(stay_points_list)
    csvfp.close()

def main():
    userid = 11
    dirName = "stay_points_dir"
    stayPointNumFile = dirName+"/%d_staypoints_num.txt" %userid
    stayPointListFile = dirName+"/%d_staypoints_list.txt" %userid
    csv_name = dirName+ "/staypoints_%s.csv" %userid

    if not os.path.exists(dirName):
        os.mkdir(dirName)  
    stay_points_list = get_stay_points_list(stayPointListFile, userid)
    print len(stay_points_list)

    saveStayPointsToCsv(csv_name,stay_points_list)

    mydb = open(stayPointNumFile, 'w')
    pickle.dump(len(stay_points_list), mydb)
    saveStayPointsBaiduCoordToJson(stay_points_list, dirName, userid)
    print "successfully!"

def get_stay_point(user_id):
    dir_name = "../data/stay_point_v1"
    csv_name = dir_name+ "/staypoints_%s.csv" %user_id
    stay_points_list = get_stay_points_list(user_id)
    saveStayPointsToCsv(csv_name, stay_points_list)

get_stay_point(1)

