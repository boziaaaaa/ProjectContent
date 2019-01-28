#coding = utf-8
import os

import datetime

def getEveryDay(startT,endT):
    result = []
    startTime = datetime.datetime.strptime(startT,"%Y%m%d")
    endTime = datetime.datetime.strptime(endT,"%Y%m%d")
    while startTime <= endTime:
        temp = datetime.datetime.strftime(startTime,"%Y%m%d")
        result.append(temp)

        startTime = startTime + datetime.timedelta(1)

    return result
if __name__ == "__main__":
    # startT = "20180501"
    # endT = "20180531"
    # result1 = getEveryDay(startT,endT)
    #
    # startT = "20180201"
    # endT = "20180228"
    # result2 = getEveryDay(startT,endT)
    #
    # startT = "20180801"
    # endT = "20180831"
    # result3 = getEveryDay(startT,endT)
    #
    # startT = "20171101"
    # endT = "20171130"
    # result4 = getEveryDay(startT,endT)
    # result = []
    # result.extend(result1)
    # result.extend(result2)
    # result.extend(result3)
    # result.extend(result4)

    # result = result1,result2,result3,result4
    startT = "20170101"
    endT =   "20180101"
    result = getEveryDay(startT,endT)
    print result

    for d in result:
        # cmd = "python ./Picture_SST_SingleOrbit.py "+d+" D"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_SingleOrbit.py "+d+" N"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AD D"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AD N"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" TD D"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" TD N"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AM D"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AM N"
        # os.system(cmd)
        cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AQ D"
        os.system(cmd)
        cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AQ N"
        os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AY D"
        # os.system(cmd)
        # cmd = "python ./Picture_SST_AD_TD_AM_AQ_AY.py "+d+" AY N"
        # os.system(cmd)