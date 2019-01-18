import xlwt
import numpy
import matplotlib.pyplot as plt
import os
def WriteEXL(outputxl,filename_all,size_all):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('L1Bsize')
    for i in range(len(size_all)):
        worksheet.write(i,0,label=filename_all[i])
        worksheet.write(i,1,label=size_all[i])
    workbook.save(outputxl)

if __name__=="__main__":
    inputL1B = r"D:\temp_10.24.189.195\20190109\test_201901.txt"
    outputxl = inputL1B.replace(".txt","2.xls")
    outputPicture = inputL1B.replace(".txt",".png")

    size_all = []
    filename_all = []
    with open(inputL1B) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            size = line[4]
            filename = line[8]
            size_all.append(float(size)/1024/1024)
            filename_all.append(filename)

    if os.path.exists(outputxl) == False:
        WriteEXL(outputxl, filename_all, size_all)

    size_all2 = numpy.zeros(len(size_all))
    for i in range(len(size_all)):
        size_all2[len(size_all)-i-1] = size_all[i]
    plt.plot(size_all2)
    plt.title("L1B size")
    plt.xlabel("1 min (20190101 to 20190109)")
    plt.ylabel("M")
    # plt.xticks((11500,),("20190108193510"))
    # plt.show()
    # if os.path.exists(outputPicture) == False:
    plt.savefig(outputPicture)
