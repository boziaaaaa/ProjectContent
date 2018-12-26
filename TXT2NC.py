# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from netCDF4 import Dataset
import numpy
import os


def txt2NC(inputTXT):
    inputNC = inputTXT.replace("_False.txt", ".NC")
    inputNC = inputNC.replace("_LMIF_", "_LMIE_")
    outputNC = inputNC.replace("_LMIE_", "_FALS_")
    EOT = []
    LON = []
    LAT = []
    ER = []
    EXP = []
    EYP = []
    DQF = []
    # get dataset from txt
    datas = {"EOT": EOT, "LON": LON, "LAT": LAT, "ER": ER, "EXP": EXP, "EYP": EYP,"DQF":DQF}
    with open(inputTXT) as f_txt:
        for line in f_txt.readlines():
            if "lon" in line:  # remove the first line
                continue
            else:
                line = line.split()
                if len(line) < 11:
                    continue

                datas["EOT"].append(numpy.float32(line[0]))
                datas["LON"].append(numpy.float32(line[1]))
                datas["LAT"].append(numpy.float32(line[2]))
                datas["ER"].append(numpy.float32(line[3]))
                datas["EXP"].append(numpy.float32(line[4]))
                datas["EYP"].append(numpy.float32(line[5]))
                datas["DQF"].append(numpy.float32(line[6]))

    # os.remove(inputTXT)
    length = len(EOT)
    NC_in = Dataset(inputNC)
    NC_out = Dataset(outputNC, 'w', format='NETCDF4')
    attr_dataset = {}

    # get attrs form LMIE NC
    # write dataset attrs
    for key in datas.keys():
        NC_out.createDimension(key, length)
        NC_out.createVariable(key, 'f4', (key))
        NC_out.variables[key][:] = datas[key]
        for i in NC_in.variables[key].ncattrs():
            if i == "units":
                if "m*m/ster" in NC_in.variables[key].getncattr(i):
                    attr_dataset[i] = u"μ" + NC_in.variables[key].getncattr(i)[2:]
                elif len(NC_in.variables[key].getncattr(i)) == 0:
                  attr_dataset[i] = "NULL"
                else:
                    attr_dataset[i] = NC_in.variables[key].getncattr(i)
            elif isinstance(NC_in.variables[key].getncattr(i), basestring):
              if len(NC_in.variables[key].getncattr(i)) == 0:
                  attr_dataset[i] = "NULL"
              else:
                  attr_dataset[i] = NC_in.variables[key].getncattr(i)
            else:
                attr_dataset[i] = NC_in.variables[key].getncattr(i)
        if key == "LAT":
            attr_dataset["long_name"] = "False Event Latitude"
            attr_dataset["standard_name"] = "False Event Latitude"
        elif key == "LON":
            attr_dataset["long_name"] = "False Event Longitude"
            attr_dataset["standard_name"] = "False Event Longitude"
        elif key == "ER":
            attr_dataset["long_name"] = "False Event Radiance"
            attr_dataset["standard_name"] = "False Event Radiance"
        elif key == "EOT":
            attr_dataset["long_name"] = "False Event Observe Time"
            attr_dataset["standard_name"] = "False Event Observe Time"
        elif key == "EXP":
            attr_dataset["long_name"] = "False Event X Pixel"
            attr_dataset["standard_name"] = "False Event X Pixel"
            attr_dataset["coordinates"] = "EXP"
        elif key == "EYP":
            attr_dataset["long_name"] = "False Event Y Pixel"
            attr_dataset["standard_name"] = "False Event Y Pixel"
        elif key == "DQF":
            attr_dataset["long_name"] = "False Lightening Event Data Quality Flag"
        print attr_dataset
        NC_out.variables[key].setncatts(attr_dataset)
    for i in NC_in.ncattrs():
        attr_global = {}

        if isinstance(NC_in.getncattr(i), basestring):
            if len(NC_in.getncattr(i)) == 0 and isinstance(NC_in.getncattr(i), basestring):
                attr_global[i] = "NULL"
            else:
                attr_global[i] = NC_in.getncattr(i)
        else:
            attr_global[i] = NC_in.getncattr(i)
        if i == "Title":
            attr_global[i] = "False Events In One Minute"
        print attr_global
        NC_out.setncatts(attr_global)

    NC_out.close()
    NC_in.close()
    return 0


if __name__ == "__main__":
    # inputTXT = sys.argv[1]
    inputTXT = "D:\\temp_10.24.189.195\\20180919\\FY4A-_LMI---_N_REGX_1047E_L2-_LMIF_SING_NUL_20180724132510_20180724133449_7800M_N04V1_False.txt"

    status = txt2NC(inputTXT)
    if status == 0:
        print "txt2NC Success!!!", inputTXT
