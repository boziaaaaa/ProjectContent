from DataOuter.HdfDataOuter import *
from DataProvider.NPPProvider import *
from ProjProcessor import *
import sys
from ParameterParser import *
import multiprocessing
import h5py
import numpy
from PIL import Image

L1FilePath = ''

def CreateStdProjProvider(resolution):
    provider = NPPProvider()

    #L1file = L1FilePath+'SVI01_npp_d20170425_t0502570_e0515220_b28457_c20170425074526000000_ipop_dev.h5'
    #Latfile = Lonfile =L1FilePath+'GITCO_npp_d20170425_t0502570_e0515220_b28457_c20170425074526000000_ipop_dev.h5'
    
    L1file = L1FilePath + 'SVI01_npp_' + sys.argv[6] +'_ipop_dev.h5'
    Latfile = Lonfile = L1FilePath + 'GITCO_npp_' + sys.argv[6] + '_ipop_dev.h5'
    
    print(Latfile)
    provider.SetLonLatFile(Latfile,Lonfile)

    print sys.argv[1]
    provider.SetL1File(L1file)
    provider.SetDataDescription('NPP_OBI_'+sys.argv[1])


    AuxiliaryName = dict()
    AuxiliaryPath = dict()
    AuxiliaryName['Latitude'] = 'Latitude'
    AuxiliaryName['Longitude'] = 'Longitude'
    AuxiliaryPath['Latitude'] = AuxiliaryPath['Longitude'] = Latfile
    provider.SetAuxiliaryDataFile(AuxiliaryName, AuxiliaryPath)
    return  provider

def ProcessProj(param,resolution):

    provider = CreateStdProjProvider(resolution)

    dataouter = HdfDataOuter()
    print(param)
    processor = ProjProcessor(provider, dataouter, param)
    processor.PerformProj()
    processor.Dispose()

def ProcessAuxProj(resolution):
    paramparser = ParameterParser()
    auxparam = paramparser.parseXML(sys.argv[2])
    auxparam.OutputPath = sys.argv[5]
    auxparam.ProjectResolution = resolution
    ProcessProj(auxparam, resolution)



def Open(filePath):
        return h5py.File(filePath, 'a')
def ReadHdfDataset(fileHandle,groupPath,datasetPath):
        dataset = N.zeros((1,1,1))
        print(fileHandle.keys())
        if (groupPath in fileHandle.keys()) or groupPath == '/':
            hdfgroup = fileHandle[groupPath]
            if datasetPath in hdfgroup.keys():
                dataset = hdfgroup[datasetPath]
        return dataset
def transA():	
	  #color table
    z1 = [0, 30, 60, 120, 190, 255]
    z2 = [0, 110, 160, 210, 240, 255]
    colorTable = N.zeros(65536)
    range1 = lambda start, end: range(start, end+1)
    for i in range1(0, 10000):
#        a = (255.0 + 0.9999) * (i * 0.0001) / (1.11)
        a = (255.0 + 0.9999) * (i * 0.0001+0.01) / (1.11)        
        for j in range(0, 5):
            if a >= z1[j] and a < z1[j + 1]:
                b = (a - z1[j]) / (z1[j + 1] - z1[j])
                colorTable[i] = z2[j] + (z2[j + 1] - z2[j]) * b
                j = 6
    return colorTable.astype('B')
    #z1 = [0, 30, 60, 120, 190, 255]
    #z2 = [0, 110, 160, 210, 240, 255]

    #colorTable = N.zeros(65536)
    #range1 = lambda start, end: xrange(start, end+1)
    #a = numpy.linspace(0,255.9999/1.11,10000)
    #for j in range(0, 5):
    #    filter = a >= z1[j]
    #    filter &= a < z1[j + 1]
    #    b = (a[filter] - z1[j]) / (z1[j + 1] - z1[j])
    #    colorTable[filter] = z2[j] + (z2[j + 1] - z2[j]) * b
                # j = 6
    #return colorTable


    #short z1[6]= { 0, 30, 60, 120, 190, 255 };
    #short z2[6] = { 0, 110, 160, 210, 240, 255 };
    #visColorTable = new short[65535];
    #                   for (i = 0; i < 65535; i++)
    #                   {
    #                       if (i >= 10000)
    #                       {
    #                           visColorTable[i] = 255;
    #                           continue;
    #                       }
    #                       a = (255 + 0.999f)  (i  0.0001f + 0.01f) / (1.11f);
    #
    #                       for (n = 0; n < 5; n++)
    #                       {
    #                           if (a >= z1[n] && a < z1[n + 1])
    #                           {
    #                               x = (float)(a - z1[n]) / (float)(z1[n + 1] - z1[n]);
    #                               visColorTable[i] = (short)(z2[n] + (z2[n + 1] - z2[n]) * x);
    #                               n = 6;

    #                           }
    #                       }
    #                   }







def trans(d,bb=0):
	print type(d)
	d2 = numpy.array(d, dtype='f4')
	f= d2>10000
	d2[f]=numpy.nan
	dmax = numpy.nanmax(d2)
	dmix = numpy.nanmin(d2)
	print dmax,dmix
	delta = dmax - dmix
	d2 -=dmix
	d2/=delta
	if bb:
		d2 = d2**bb
	d2*=255
	return d2.astype('B')

def trans__(d):
  colortable = transA()
  image = numpy.empty_like(d,dtype=colortable.dtype)
  for i,j in enumerate(d):
    image[i]=colortable[tuple(j),]

  return image

if __name__ == '__main__':
    DataResolution = sys.argv[3]  #2017_4_7
    DataTime = sys.argv[1]        #2017_4_7
    DataTime = int(DataTime[9:11])#2017_4_7
    #if((DataResolution == '500' or DataResolution == '1000') and (DataTime>12 and DataTime<22)):
    #    exit()
    L1FilePath = sys.argv[4]
    paramparser = ParameterParser()
    param = paramparser.parseXML(sys.argv[2])
    param.OutputPath = sys.argv[5]

    L1FilePath = sys.argv[4]
    ProcessProj(param, int(sys.argv[3]))



    HDFFilePath = '/mnt/hgfs/D/temp_NPP/result/NPP_OBI_'+sys.argv[1]+'_NPP.HDF'
    OutImageFileName = '/mnt/hgfs/D/temp_NPP/result/NPP_OBI_'+sys.argv[1]+'_NPP.jpg'
    print(HDFFilePath)
    print(OutImageFileName)


    fileHandle = Open(HDFFilePath)

    Band1 = ReadHdfDataset(fileHandle,'/','EVB1')
    Band2 = ReadHdfDataset(fileHandle,'/','EVB2')
    Band4 = ReadHdfDataset(fileHandle,'/','EVB4')

    Height,Width = Band1.shape


   
    print('0000000000000000000000000000')
    Band1 = N.array(Band1)
    #b=trans(Band1) 
    #g=trans(Band2) 
    #r=trans(Band4)  
    #r=trans(Band1) 
    #g=trans(Band2) 
    #b=trans(Band4)      
    b=trans(Band1,bb=1) # bb bigger Image Redder
    g=trans(Band2,bb=1.65) # bb bigger Image 
    r=trans(Band4,bb=1.65)  # bb bigger Image Bluer
    print('22222222222222222222222222222222222')

    rgbArray = N.zeros(( Height,Width, 3), 'uint8')
    rgbArray[..., 0] = r
    rgbArray[..., 1] = g
    rgbArray[..., 2] = b
    #rgbArray[..., 0] = b
    #rgbArray[..., 1] = g
    #rgbArray[..., 2] = r
    print('33333333333333333333333333333333333')

    img = Image.fromarray(rgbArray,mode="RGB")
    #img = Image.fromarray(rgbArray)
    img.save(OutImageFileName)
    #thumb = OutImageFileName.replace('.PNG','_thumb.jpg')
    #img = img.resize((1400,1200),Image.ANTIALIAS)
    #img.save(thumb)



