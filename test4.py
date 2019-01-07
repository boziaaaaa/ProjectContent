import os
import numpy
import datetime
def GetDates(dateBegin,dateEnd):
    eachDay = []
    dateBegin = datetime.datetime.strptime(str(dateBegin),"%Y%m%d")
    dateEnd = datetime.datetime.strptime(str(dateEnd),"%Y%m%d")
    print dateBegin
    while dateBegin <= dateEnd:
        date_str = datetime.datetime.strftime(dateBegin,"%Y%m%d")
        print date_str
        eachDay.append(date_str)
        dateBegin = dateBegin + datetime.timedelta(1)
    return eachDay
if __name__ == "__main__":
  band = 5
  diff_band1 = []
  dateBegin = 20171219
  dateEnd = 20171220
  dates = GetDates(dateBegin,dateEnd)
  print dates
  for date_str in dates:

      inputPath = "D:\\temp_10.24.34.219\useless\\" + date_str
      files = os.listdir(inputPath)

      for f in files:
          if ".dat" in f and "6SCAL" not in f:
              f = os.path.join(inputPath,f)
              with open(f,"r") as f_txt:
                  lines = f_txt.readlines()
                  for line in lines:
                      if "***" not in line and "FY3D" not in line and "---" not in line and "DSL" not in line:
                        data = line

              data = data.split()
              ref_gc = data[64:(64+19)]
              ref_mn = data[83:(83+19)]
              # print os.path.basename(f)
              # print ref_gc
              # print ref_mn
              # print "------------------"
              diff_tmp = float(ref_gc[band-1]) - float(ref_mn[band-1])
              diff_band1.append(diff_tmp)
  # print diff_band1
  print numpy.mean(diff_band1)