#-*-coding=utf-8-*-
import xlrd
import xlwt
import re
import datetime

def writeEXCEL(excelFile,Date_all,True_all ,False_all):

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0, 0, u"日期")
    sheet.write(0, 1, u"成功个数")
    sheet.write(0, 2, u"失败个数")
    for i in range(len(Date_all)):
        Date_all[i] = Date_all[i].replace("-","")
        print Date_all[i]
        sheet.write(i+1, 0, str(Date_all[i]))
        sheet.write(i+1, 1, str(True_all[i]))
        sheet.write(i+1, 2, str(False_all[i]))
    wbk.save(excelFile)
    return 0

def time(inputExcelFile):
    fileHandle = xlrd.open_workbook(inputExcelFile)
    sheet = fileHandle.sheets()[0]
    timeStart = sheet.col_values(1)[1:]
    QA = sheet.col_values(4)[1:]
    dateFlag = str(datetime.datetime.strptime(timeStart[0],"%m/%d/%Y %H:%M:%S")).split(" ")[0]
    True_single = 0
    False_single = 0
    Date_all = []
    True_all = []
    False_all = []
    # 转换成时间数组
    for i in range(len(timeStart)):
        start_each = datetime.datetime.strptime(timeStart[i], "%m/%d/%Y %H:%M:%S")
        day = str(start_each).split(" ")[0]


        if day != dateFlag:
            Date_all.append(dateFlag)
            True_all.append(True_single)
            False_all.append(False_single)
            True_single = 0
            False_single = 0
            dateFlag = day
        if QA[i] == 0:
            True_single = True_single + 1
        else:
            False_single = False_single + 1
    writeEXCEL(ouputExcelFile,Date_all,True_all ,False_all)
if __name__=="__main__":
    inputExcelFile = u"D:/temp_10.24.189.195/programTime/L2 ORI产品20170401_20180306.xlsx"
    ouputExcelFile = "D:/temp_10.24.189.195/programTime/ttt.xls"

    data = time(inputExcelFile)
