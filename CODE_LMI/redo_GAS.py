import os

filePath = "D:\\temp_10.24.171.20\\"
outputFile = "D:\\temp_10.24.171.42\\result.txt"

f_txt = open(outputFile,"a")

xmlFiles = os.listdir(filePath)
for eachFile in xmlFiles:
    with open(filePath+eachFile) as f:
        lineS = f.readlines()
        for line in lineS:
            if "/COSLSFA/FY3D/GAS/GASPQ FY3DGASPQPQR_FY3D_GASXX_L0_CSOC" in line and "Input=" not in line:
                f_txt.write(line[23:-4])
                f_txt.write('\n')
            elif "/COSLSFA/FY3D/GAS/GASGPS F3DGASGPSXXR_FY3D_GASXX_L0_CSOC_" in line and "Input=" not in line:
                f_txt.write(line[23:-4])
                f_txt.write('\n')
            elif "/COSLSFA/FY3D/GAS/GASPC FY3DGASPCPCR_FY3D_GASXX_L0_CSOC" in line and "Input=" not in line:
                f_txt.write(line[23:-4])
                f_txt.write('\n')
        print "-------------"
f_txt.close()
