#coding=utf-8
import h5py
import os
import xlwt


def writeEXCEL(excelFile,files_L1B,frame_num,event_Num):

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0, 0, u"文件名")
    sheet.write(0, 1, u"总帧数")
    sheet.write(0, 2, u"event总数")
    index = 0
    for f in files_L1B:
        sheet.write(index+1, 0,f)
        sheet.write(index+1, 1, frame_num[index])
        sheet.write(index+1, 2, event_Num[index])
        index = index + 1

    wbk.save(excelFile)
    return 0

if __name__=="__main__":
    inputPath = "D:\\temp_10.24.189.195\\L1B\\"
    outputPath = "D:\\temp_10.24.189.195\\"

    frame_num = []
    event_Num = []
    files_L1B = os.listdir(inputPath)
    for f in files_L1B:
        filename = inputPath+f
        fileHandle = h5py.File(filename,"r")
        dataset = fileHandle["VData"]
        frame_num.append(len(dataset))
        temp = 0
        for dataName in dataset:
            t = dataset[dataName].shape[0]
            temp = temp + t
        event_Num.append(temp)
        fileHandle.close()

    excelFile = outputPath + "L1B_frameNumber_eventNumber.xls"
    writeEXCEL(excelFile,files_L1B,frame_num,event_Num)






