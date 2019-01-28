# coding=utf-8
import MySQLdb
import sys
import xml.etree.ElementTree as ET
import time
import numpy


class InsertDB:

    def __init__(self):
        self.conn = MySQLdb.connect(
            host='10.24.4.135',
            port=3306,
            user='gds',
            passwd='gds',
            db='GDS',
        )
        self.cur = self.conn.cursor()

    def Storage(self,strDate,Avgdata,maxdata,mindata,datatype,DSL,areaid = 0,DorN = "D",SatID = "VIRR"):

        SQLcheck = "SELECT * FROM SST_AVG WHERE DataType = '%s' AND DSL = %d AND SATID = '%s' AND AREAID = %d AND DorN = '%s' "  %(datatype, DSL, SatID, areaid,DorN)
        print SQLcheck
        self.cur.execute(SQLcheck)
        results = self.cur.fetchall()
        print results

        if len(results) == 0:
            sqlcomm = "SELECT * FROM SST_AVG "
            # print sqlcomm
            self.cur.execute(sqlcomm)
            res = self.cur.fetchall()
            if len(res) == 0:
                ID = 0
            else:
                ID = res[-1][0] + 1
            self.insert(ID,strDate,Avgdata,maxdata,mindata,datatype,DSL,SatID,areaid,DorN)
        else:
            ID = results[-1][0]
            self.updata(ID,strDate,Avgdata,maxdata,mindata,datatype,DSL,SatID,areaid,DorN)

        return

    def delete(self,datatype,DSL,SatID):
        sqlcomm = "DELETE FROM SST_AVG WHERE DataType = '%s' AND DSL = %d AND SATID = '%s'" %(datatype,DSL,SatID)
        try:
            self.cur.execute(sqlcomm)
        except:
            print "DELETE ERROR"
            return -1

        return 0

    def insert(self,ID,strDate,Avgdata,maxdata,mindata,datatype,DSL,SatID,areaid,DorN):

        sqlcomm = "insert into SST_AVG values(%d,'%s',%f,%f, %f,'%s',%d,'%s',%d,'%s')" %(ID,strDate,Avgdata,maxdata,mindata,datatype,DSL,SatID,areaid,DorN)
        print sqlcomm
        try:
            result = self.cur.execute(sqlcomm)
            print "Insert SUCCESS"
        except:
            print "Insert ERROR"
            return -1

        return 0

    def updata(self,ID,strDate,Avgdata,maxdata,mindata,datatype,DSL0,SatID,areaid,DorN):
        sqlcomm = "UPDATE SST_AVG SET DateTime = '%s',AVG_Degree = %f,Max_Degree = %f,Min_Degree = %f WHERE DataType = '%s' AND DSL = %d AND SATID = '%s' AND  AREAID = %d AND DorN = '%s'" \
                  %(strDate, Avgdata, maxdata, mindata, datatype, DSL0, SatID, areaid, DorN)
        print sqlcomm
        try:
            result = self.cur.execute(sqlcomm)
            print "UPDATE SUCCESS"
        except:
            print "UPDATE ERROR"
            return -1

        return 0

    def closeall(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def getValue(self,strType,areaid = 0,DorN = 'D',SatID = "VIRR"):
        #self.cur = self.conn.cursor()
        sqlcomm = "SELECT * FROM SST_AVG WHERE DataType = '%s' AND SATID = '%s' AND AREAID = %d AND DorN = '%s' ORDER BY DSL"  %(strType, SatID, areaid, DorN)
        self.cur.execute(sqlcomm)
        results = self.cur.fetchall()
        #print "getvalue results",results,len(results)
        if len(results) == 0:
            print "Do not Find Match Data"
        elif len(results) == 1:
            Avgdata = results[0][2]
            DSL = results[0][6]
        else:
            # Avgdata = results[:,2]
            # DSL = results[:,6]

            #v = [x[0] for x in arr]
            Avgdata = [res[2] for res in results]
            DSL = [res[6] for res in results]
        #self.closeall()

        return (DSL, Avgdata)

    def get_Lat_Lon_Extend(self,areaid = 0):
        #self.cur = self.conn.cursor()
        sqlcomm = "SELECT * FROM SST_Area_Config WHERE SSTAREA_ID = %d" % (areaid)
        # print sqlcomm
        self.cur.execute(sqlcomm)
        results = self.cur.fetchall()
        #print "getvalue results",results,len(results)
        if len(results) == 0:
            print "Do not Find Match Data"
        elif len(results) == 1:
            sLat = results[0][2]
            sLon = results[0][3]
            eLat = results[0][4]
            eLon = results[0][5]
        else:
            print "Do not Find Match Data"
            # Avgdata = [res[2] for res in results]
            # DSL = [res[6] for res in results]

        return sLat,sLon,eLat,eLon

# if __name__ == "__main__":
#     DB = InsertDB()
#     DB.Handle("20180101",24.5,25.1,22.2,"PD")