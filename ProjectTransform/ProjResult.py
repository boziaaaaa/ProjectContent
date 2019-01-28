import numpy as N
import ProjOutputData_module as SD
########################################
import h5py

class ProjResult(object):


    def __init__(self):
        super(ProjResult,self).__init__()
        self.U = None
        self.V = None

        self.ResultInfo = None

        self.LatLonRangeMask = None

        self.NeedUpdate = True

        self.__DstProj = None

        self.__Width = 0
        self.__Height = 0
        self.__tv = None
        self.__tu = None
        self.__DataSearchTable = None
        self.__IslatlongProj = False

        self.MaxU = None
        self.MinU = None
        self.MaxV = None
        self.MinV = None

        self.__latlonResRate = float(0.01) / float(1000)
        return

    def SetDstProj(self,dstProj):
        self.__DstProj = dstProj
        if 'latlong' in dstProj.srs:
            self.__IslatlongProj = True

    def Dispose(self):

       del self.U

       del self.V

       del self.ResultInfo

       del self.LatLonRangeMask

       del self.__tv
       del self.__tu
       del self.__DataSearchTable



    def CalProjectMinMax(self, U, V):

        maskU = (U < 999999999)
        maskV = (V < 999999999)

        RealU = U[maskU]
        RealV = V[maskV]
        self.MinU = N.min(RealU[:]).astype(N.float32)
        self.MinV = N.min(RealV[:]).astype(N.float32)
        self.MaxU = N.max(RealU[:]).astype(N.float32)
        self.MaxV = N.max(RealV[:]).astype(N.float32)
        return self.MinU, self.MinV, self.MaxU, self.MaxV

    # def CalProjectMinMax(self,projRange):

    # def CalCenterUV(self,U,V):
    #     self.CalProjectMinMax(U,V)
    #     centU = (self.MaxU-self.MinU)/2+self.MinU
    #     centV = (self.MaxV-self.MinV)/2+self.MinV
    #     return  centU,centV


    def CalProjectWidthAndHeight(self,minU,minV,maxU,maxV,resolution):

        Height = round((maxV- minV) / resolution+ 0.5)
        Width = round((maxU- minU) / resolution+ 0.5)

        #print("LLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        #print Height,Width
        return Height,Width

    def CalUVToIJ(self,resolution,U,V,minU,minV):
        resolutionFactor = float(1)/float(resolution)
        ru = U*resolutionFactor
        rv = V*resolutionFactor
        minUF = minU*resolutionFactor
        minVF = minV*resolutionFactor
        tu = (ru-minUF).astype(N.int32)
        tv = (rv-minVF).astype(N.int32)

        # file = h5py.File('/home/bozi/Downloads/TestData/GetOBSData'+band+'.HDF.h5', 'w')
        # file.create_dataset('tu', data=tu)
        # file.create_dataset('tu', data=tv)
        # file.create_dataset('u', data=U)
        # file.create_dataset('v', data=V)
        # file.close()
        return  tu,tv

    ''' yuanbo 20180918
    def CreateSaveData(self, refdata,resolution,datatype):

        res = resolution
        if self.__IslatlongProj:
            res = self.__latlonResRate*resolution

        if self.NeedUpdate:
            # if self.MaxU == None:
            #self.LatLonRangeMask = self.U<65535######## ji gui wei xing -- Polar Satellite #20170628 yuanbo litttle/Big Range
            #self.CalProjectMinMax(self.U[(self.LatLonRangeMask)], self.V[(self.LatLonRangeMask)])
            self.__Height, self.__Width = self.CalProjectWidthAndHeight( self.MinU, self.MinV, self.MaxU, self.MaxV,res)
            self.__tu, self.__tv = self.CalUVToIJ(res,self.U,self.V,self.MinU,self.MinV)
            temp1 = self.__tu[(self.LatLonRangeMask)]
            temp2 = self.__tv[(self.LatLonRangeMask)]
            self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width ), int(self.__Height), self.__tu[(self.LatLonRangeMask)], self.__tv[(self.LatLonRangeMask)])
            self.NeedUpdate = False
        data = refdata[(self.LatLonRangeMask)]

        # temp = data[8000]
        # file = h5py.File("/home/bozi/Downloads/TestData/MSG_data_result"+str(temp)+".HDF")
        # file.create_dataset("MSG_data_result",data = data)
        saveData  = SD.CreateOutputData(int(self.__Width ), int(self.__Height),datatype,self.__DataSearchTable,data)
        # file.create_dataset("saveData",data = saveData)
        # file.close()
        del data
        return saveData
    '''
    def CreateSaveData(self, refdata, resolution, datatype, datasetName):

        if self.MaxU > 180:  # if is'latlong proj' and longitude is out of range
            print self.V, self.U, self.MaxV, self.MinV, self.MaxU, self.MinU
            self.LatLonRangeMask = (self.V[:, :] <= self.MaxV) & (self.V[:, :] >= self.MinV) & \
                                   (self.U[:, :] <= self.MaxU) & (self.U[:, :] >= self.MinU)

        res = resolution
        if self.__IslatlongProj:
            res = self.__latlonResRate * resolution

        if self.NeedUpdate:
            # if self.MaxU == None:
            #     self.CalProjectMinMax(self.U[(self.LatLonRangeMask)], self.V[(self.LatLonRangeMask)])
            self.__Height, self.__Width = self.CalProjectWidthAndHeight(self.MinU, self.MinV, self.MaxU, self.MaxV, res)
            self.__tu, self.__tv = self.CalUVToIJ(res, self.U, self.V, self.MinU, self.MinV)
            self.__DataSearchTable = SD.CreateOutputSearTable(int(self.__Width), int(self.__Height),
                                                              self.__tu[(self.LatLonRangeMask)],
                                                              self.__tv[(self.LatLonRangeMask)])
            # file = h5py.File("/FY4COMM/FY4A/COM/PRJ/test/searchtable.HDF")
            # file.create_dataset("self.__DataSearchTable",data = self.__DataSearchTable)
            # file.close()
            self.NeedUpdate = False

        if self.__IslatlongProj and ("ongitude" in datasetName):
            saveData = N.linspace(self.MinU, self.MaxU, int(self.__Width))
            saveData = N.tile(saveData, int(self.__Height))
            saveData = saveData.reshape(int(self.__Height), int(self.__Width)).astype('f4')
            if self.MaxU > 180:
                saveData[saveData > 180] -= 360
                saveData[saveData < -180] += 360
        elif self.__IslatlongProj and "atitude" in datasetName:
            saveData = N.linspace(self.MaxV, self.MinV, self.__Height)
            saveData = N.tile(saveData, int(self.__Width))
            saveData = saveData.reshape(int(self.__Width), int(self.__Height)).astype('f4')
            saveData = saveData.T

        else:
            print "========"
            print refdata.shape
            print self.LatLonRangeMask.shape
            data = refdata[(self.LatLonRangeMask)]
            saveData = SD.CreateOutputData(int(self.__Width), int(self.__Height), datatype, self.__DataSearchTable,
                                           data)
            del data

        if (type(saveData[0, 0]) is N.float32):
            FillValue = 65535
            self.FourCorner(saveData, FillValue)
        if (type(saveData[0, 0]) is N.int32):
            FillValue = 65535
            self.FourCorner(saveData, FillValue)
        elif type(saveData[0, 0]) is N.int16:
            FillValue = 32767
            self.FourCorner(saveData, FillValue)
        elif type(saveData[0, 0]) is N.int8:
            FillValue = 127
            self.FourCorner(saveData, FillValue)
        elif type(saveData[0, 0]) is N.uint8:
            FillValue = 255
            self.FourCorner(saveData, FillValue)

        return saveData

    def FourCorner(self, saveData, FillValue):
        # left up
        if saveData[0, 0] == FillValue and saveData[0, 1] != FillValue:
            saveData[0, 0] = saveData[0, 1]
        elif saveData[0, 0] == FillValue and saveData[1, 0] != FillValue:
            saveData[0, 0] = saveData[1, 0]
        elif saveData[0, 0] == FillValue and saveData[1, 1] != FillValue:
            saveData[0, 0] = saveData[1, 1]
        # left down
        if saveData[int(self.__Height - 1), 0] == FillValue and saveData[int(self.__Height - 1), 1] != FillValue:
            saveData[int(self.__Height - 1), 0] = saveData[int(self.__Height - 1), 1]
        elif saveData[int(self.__Height - 1), 0] == FillValue and saveData[int(self.__Height - 1 - 1), 0] != FillValue:
            saveData[int(self.__Height - 1), 0] = saveData[int(self.__Height - 1 - 1), 0]
        elif saveData[int(self.__Height - 1), 0] == FillValue and saveData[int(self.__Height - 1 - 1), 1] != FillValue:
            saveData[int(self.__Height - 1), 0] = saveData[int(self.__Height - 1 - 1), 1]
        # right up
        if saveData[0, int(self.__Width - 1)] == FillValue and saveData[1, int(self.__Width - 1)] != FillValue:
            saveData[0, int(self.__Width - 1)] = saveData[1, int(self.__Width - 1)]
        elif saveData[0, int(self.__Width - 1)] == FillValue and saveData[0, int(self.__Width - 1 - 1)] != FillValue:
            saveData[0, int(self.__Width - 1)] = saveData[0, int(self.__Width - 1 - 1)]
        elif saveData[0, int(self.__Width - 1)] == FillValue and saveData[1, int(self.__Width - 1 - 1)] != FillValue:
            saveData[0, int(self.__Width - 1)] = saveData[1, int(self.__Width - 1 - 1)]
            # right down
        if saveData[int(self.__Height - 1), int(self.__Width - 1)] == FillValue and saveData[
            int(self.__Height - 1 - 1), int(self.__Width - 1)] != FillValue:
            saveData[int(self.__Height - 1), int(self.__Width - 1)] = saveData[
                int(self.__Height - 1 - 1), int(self.__Width - 1)]
        elif saveData[int(self.__Height - 1), int(self.__Width - 1)] == FillValue and saveData[
            int(self.__Height - 1), int(self.__Width - 1 - 1)] != FillValue:
            saveData[int(self.__Height - 1), int(self.__Width - 1)] = saveData[
                int(self.__Height - 1), int(self.__Width - 1 - 1)]
        elif saveData[int(self.__Height - 1), int(self.__Width - 1)] == FillValue and saveData[
            int(self.__Height - 1 - 1), int(self.__Width - 1 - 1)] != FillValue:
            saveData[int(self.__Height - 1), int(self.__Width - 1)] = saveData[
                int(self.__Height - 1 - 1), int(self.__Width - 1 - 1)]

        return
