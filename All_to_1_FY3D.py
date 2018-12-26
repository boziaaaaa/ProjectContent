 #-*-coding:utf-8-*-
import os
import numpy
import datetime
import re

inpath = r'D:\\temp_10.24.34.219\\result_20180702\\FY3D_mersi\\'
outpath = r'D:\\temp_10.24.34.219\\result_20180702\\FY3D_mersi\\'

sdt = datetime.datetime.strptime('20171126', '%Y%m%d')
edt = datetime.datetime.strptime('20180701','%Y%m%d')
dt = sdt

while dt <=edt:
    date = dt.strftime("%Y%m%d")
    dt += datetime.timedelta(days=1)
    path = inpath + date
    filelist = os.listdir(path)
    if len(filelist) <= 0:
        continue
    changdi = ['Dunhuang','Libya1','Libya4','Arabia2','Lanai','Algeria5','Sonora','Algeria3','Mauritania2']
    for item in filelist :
        if "original.txt" in item:
            continue
        for i in range(0,9):
            p = re.compile(r'FY3D_mersi_%s_(.*).txt' % changdi[i])
            m = p.match(item)
            if m:
                fp = open(os.path.join(path,item),'r')
                data = fp.readlines()
                fp.close()
                txtname = 'FY3D_mersi_%s.dat' % changdi[i]
                outname = os.path.join(outpath,txtname)
                if not os.path.isfile(outname):
                    fpout = open(outname,'a+')
                    fpout.write(data[0])
                    fpout.write(data[1])
                    fpout.write(data[2])
                    fpout.write(data[3])
                    fpout.write(data[4])
                    fpout.write(data[5])
                    fpout.close()
                fpout = open(outname,'a+')
                # fpout.write(data[4])
                fpout.write(data[6])

                fpout.close()

################
dt = sdt
while dt <=edt:
    date = dt.strftime("%Y%m%d")
    dt += datetime.timedelta(days=1)
    path = inpath + date
    filelist = os.listdir(path)
    if len(filelist) <= 0:
        continue
    changdi = ['Dunhuang','Libya1','Libya4','Arabia2','Lanai','Algeria5','Sonora','Algeria3','Mauritania2']
    for item in filelist :
        if "original.txt" not in item:
            continue
        for i in range(0,9):
            p = re.compile(r'FY3D_mersi_%s_(.*).txt' % changdi[i])
            m = p.match(item)
            # print "---",m
            if m:
                fp = open(os.path.join(path,item),'r')
                data = fp.readlines()
                fp.close()
                txtname = 'FY3D_mersi_%s.dat' % changdi[i]
                outname = os.path.join(outpath,txtname)
                outname = outname.replace(".dat","_original.dat")
                if not os.path.isfile(outname):
                    print outname
                    fpout = open(outname,'a+')
                    fpout.write(data[0])
                    fpout.write(data[1])
                    fpout.write(data[2])
                    fpout.write(data[3])
                    fpout.write(data[4])
                    fpout.close()
                print outname
                fpout = open(outname,'a+')
                fpout.write(data[5])

                fpout.close()