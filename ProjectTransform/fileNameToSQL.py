# coding=utf-8
import MySQLdb
import sys
import xml.etree.ElementTree as ET
import time
import numpy
import re

def parseXML(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    for projrange in root.iter('ProjRange'):
        maxlon = projrange.find('MaxLon').text
        minlon = projrange.find('MinLon').text
        maxlat = projrange.find('MaxLat').text
        minlat = projrange.find('MinLat').text

    return minlon, maxlat, maxlon, minlat


def fileNameToSQL(JPGfile, HDFfile, xlmFile, dnflag):
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='gds',
        passwd='gds',
        db='GDS',
    )
    cur = conn.cursor()

    # �������ݱ�
    # cur.execute("create table SST_Product(HDFfile varchar(300),JPGfile varchar(300))")

    checkSQL = "SELECT * FROM SST_Product"  # WHERE JPGfile "#> '%s'" % (1000)
    cur.execute(checkSQL)
    results = cur.fetchall()
    if len(results) == 0:
        ID = 0
    else:
        ID = results[-1][0] + 1
        
    temp = re.search("FY3",HDFfile)
    SatID = HDFfile[temp.start():temp.start()+4]
    print "]]]]]]]]]]]]"
    print SatID
    
    Date = JPGfile[-26:-18]
    print JPGfile, Date, dnflag

    curr_time = time.localtime(time.time())

    dataCreatTime = str(curr_time[0]).zfill(4) + '-' + str(curr_time[1]).zfill(2) + '-' + str(curr_time[2]).zfill(
        2) + ' ' + str(curr_time[3]).zfill(2) + ':' + str(curr_time[4]).zfill(
        2) + ':' + str(curr_time[5]).zfill(2)
    minlon, maxlat, maxlon, minlat = parseXML(xlmFile)  # �Ľǵ㾭γ��
    PD_PT_PM_PY = HDFfile[-6:-4]
    # ����һ������
    # cur.execute("insert into SST_Product values('%d','%s','%s','%s','%s')"%(ID,Date,JPGfile,HDFfile,"PD"))
    #sql = "insert into SST_Product values('%d','%s','%s','%s','%s','%s','%s','%f','%f','%f','%f')" % (
    #ID, dataCreatTime, Date, JPGfile, HDFfile, PD_PT_PM_PY, dnflag, float(maxlat), float(minlon), float(minlat),
    #float(maxlon))
    print "------------------------"
    print dataCreatTime, Date
    sql = "insert into SST_Product values('%d','%s','%s','%s','%s','%s','%s','%s','%f','%f','%f','%f')" % (
    ID,SatID, dataCreatTime, Date, JPGfile, HDFfile, PD_PT_PM_PY, dnflag, float(maxlat), float(minlon), float(minlat),
    float(maxlon))
    print sql
    cur.execute(sql)

    # �޸Ĳ�ѯ����������
    # cur.execute("update student set class='3 year 1 class' where name = 'Tom'")
    # ɾ����ѯ����������
    # cur.execute("delete from student where JPGfile='/gds/DATA/MOSAIC/FY3C_VIRR_MOSAIC_20171120_PD.HDF'")

    # checkSQL = "SELECT * FROM SST_Product" # WHERE JPGfile "#> '%s'" % (1000)
    # cur.execute(checkSQL)
    # results = cur.fetchall()
    # print results
    # cur.execute("DROP TABLE IF EXISTS SST_Product")
    cur.close()
    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    JPGfile = sys.argv[1]
    HDFfile = sys.argv[2]
    dnflag = sys.argv[3]
    xlmFile = "/GDS/SSTWORK/ProjectTransform_FY3D_SST/FY3D_MERSI_5000m_Proj.xml"

    print sys.argv
    # print Date
    fileNameToSQL(JPGfile, HDFfile, xlmFile, dnflag)
    print HDFfile, JPGfile
