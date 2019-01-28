# coding=utf-8
import MySQLdb
import sys
import xml.etree.ElementTree as ET
import time
import numpy


def fileNameToSQL(inputString):
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

    checkSQL = "SELECT * FROM SST_Product_Analyse"  # WHERE JPGfile "#> '%s'" % (1000)
    cur.execute(checkSQL)
    results = cur.fetchall()
    if len(results) == 0:
        ID = 0
    else:
        ID = results[-1][0] + 1
    inputString = inputString.split(",")
    print inputString
    # ����һ������
    # cur.execute("insert into SST_Product values('%d','%s','%s','%s','%s')"%(ID,Date,JPGfile,HDFfile,"PD"))
    cur.execute(
        "insert into SST_Product_Analyse values('%d','%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%f','%f','%f','%f')" % (
            ID, int(inputString[0]),
            inputString[1], inputString[2], inputString[3], inputString[4], inputString[5], inputString[6],
            inputString[7],
            inputString[8], inputString[9], inputString[10], inputString[11], inputString[12],
            inputString[13], inputString[14], float(inputString[15]), float(inputString[16]), float(inputString[17]),float(inputString[18])))

    cur.close()
    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    inputString = sys.argv[1]
    fileNameToSQL(inputString)
