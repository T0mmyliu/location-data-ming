# -*- coding: utf-8 -*-

import math

'''
 * 百度坐标（BD09）、国测局坐标（火星坐标，GCJ02）、和WGS84坐标系之间的转换的工具
 *
 * 参考 https://github.com/wandergis/coordtransform 实现的python版本
 * @author wpliu
'''


class CoordinateTransformTool:
    def __init__(self):
        self.x_pi = 14159265358979324 * 3000.0 / 180.0
        # π
        self.pi = 3.1415926535897932384626
        # 长半轴
        self.a = 6378245.0
        # 扁率
        self.ee = 0.00669342162296594323

    '''
    * WGS坐标转百度坐标系(BD-09)
    *
    * @param lng WGS84坐标系的经度
    * @param lat WGS84坐标系的纬度
    * @return 百度坐标数组
    '''
    def wgs84_to_bd09(self, lng, lat):
        gcj = self.wgs84_to_gcj02(lng, lat)
        bd09 = self.gcj02_to_bd09(gcj[0], gcj[1])
        return bd09

    '''
     * 火星坐标系(GCJ-02)转百度坐标系(BD-09)
     *
     * 谷歌、高德——>百度
     * @param lng 火星坐标经度
     * @param lat 火星坐标纬度
     * @return 百度坐标数组
     *
    '''
    def gcj02_to_bd09(self, lng, lat):
        z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * self.x_pi)
        theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * self.x_pi)
        bd_lng = z * math.cos(theta) + 0.0065
        bd_lat = z * math.sin(theta) + 0.006
        return bd_lng, bd_lat

    '''
     * WGS84转GCJ02(火星坐标系)
     *
     * @param lng WGS84坐标系的经度
     * @param lat WGS84坐标系的纬度
     * @return 火星坐标数组
     *
    '''

    def wgs84_to_gcj02(self, lng, lat):
        if self.out_of_china(lng, lat):
            return lng, lat
        dlat = self.transform_lat(lng - 105.0, lat - 35.0)
        dlng = self.transform_lng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * self.pi
        magic = math.sin(radlat)
        magic = 1 - self.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((self.a * (1 - self.ee)) / (magic * sqrtmagic) * self.pi)
        dlng = (dlng * 180.0) / (self.a / sqrtmagic * math.cos(radlat) * self.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return mglng, mglat

    '''
     * 纬度转换
     *
     * @param lng
     * @param lat
     * @return
     */
     '''

    def transform_lat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 * math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 * math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 * math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    '''
     * 经度转换
     *
     * @param lng
     * @param lat
     * @return
    '''

    def transform_lng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 * math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 * math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 * math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    '''
    * 判断是否在国内，不在国内不做偏移
    *
    * @param lng
    * @param lat
    * @return
    '''

    @staticmethod
    def out_of_china(lng, lat):
        if lng < 72.004 or lng > 137.8347:
            return True
        elif lat < 0.8293 or lat > 55.8271:
            return True
        return False

def test():
    coor_trans_tool = CoordinateTransformTool()
    lon, lat = coor_trans_tool.wgs84_to_bd09(116.326624, 39.977897)
    print lon, lat

test()