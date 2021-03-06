

import errno
import json
def close_file(fp):
    try:
        fp. close()
    except IOError as e:
        if e.errno == errno.EACCES:
            return "some default data"
        # Not a permission error.
        raise

def open_file(filename):
    try:
        fp = open(filename)
    except IOError as e:
        if e.errno == errno.EACCES:
            return "some default data"
        # Not a permission error.
        raise IOError
    else:
#      with fp:
            return fp

def open_file_write(filename):
    try:
        fp = open(filename, 'w')
    except IOError as e:
        if e.errno == errno.EACCES:
            return "some default data"
        # Not a permission error.
        raise
    else:
#      with fp:
            return fp

def store_list(filename, listName, listContext):
    fileStr = ""
    existFlag = 0
    listStr = ""
    fp = None
    # if(len(listContext) == 0) :
    #    return ;

    for nodeStr in listContext:
        if (isinstance(nodeStr, basestring)):
#        if type(nodeStr) is types.StringType:
            listStr = listStr + nodeStr + ","
    listStr = listStr.strip(',')
    try:
        fp = open_file(filename)
        while True:
            line = fp.readline()
            ret = line.find("listName:"+ listName)
            if(ret == -1):
                fileStr = line +fileStr+fp.readline();
            else:
                existFlag = 1;
                fileStr = line +fileStr+listStr;
                fp.readline();
            if(line == ""):
                break
            print line
    except :
        print "No list exist";
    finally:
        if (fp):
            close_file(fp);
    if not (existFlag):
        fileStr = fileStr + "listName:" + listName + "\n"
        fileStr = fileStr + listStr + "\n"
    fp = open_file_write(filename)
    fp.write(fileStr);
    close_file(fp);


def get_store_list(filename, listName):
    listContext = None
    fp = None
    try:
        fp = open_file(filename)
        while True:
            line = fp.readline()
            ret = line.find("listName:"+ listName)
            if(ret == -1):
                fp.readline();
            else:
                #existFlag = 1;
                listContext = fp.readline();
            if(line == ""):
                break
            print line
    except :
        print "not exist";
        raise IOError;
    finally:
        if (fp):
            close_file(fp);
    return listContext

def savePointsToJson(distPointList, userid, filetype='', fileId = 0 ):
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
    fileGpoints = "%d_points_dir/points_gps_%s%d.js" %(userid,filetype,fileId)
    strTmp = "var data%d =" %fileId
    saveDate = {'data':datalist,'total':len(datalist),"rt_loc_cnt":47764510,"errorno":0,"NearestTime":"2014-08-29 15:20:00","userTime":"2014-08-29 15:32:11"}
    strTmp += json.dumps(saveDate,sort_keys=False)
    with open(fileGpoints,"w") as fp:
        fp.write(strTmp)
    fp.close()

