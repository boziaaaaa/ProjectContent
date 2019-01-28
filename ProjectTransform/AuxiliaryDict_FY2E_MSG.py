import sys

AuxiliaryDataDict = dict()
AuxiliaryNameDict = dict()

resolution = sys.argv[3]

#def SetLatLon(AuxiliaryDataDICT,Resolution):
#    AuxiliaryDataDICT['Latitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+Resolution+'M_NOM_LAT.hdf'
#    AuxiliaryDataDICT['Longitude'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+Resolution+'M_NOM_LON.hdf'
    		
def SetNameAndPath(AuxiliaryNameDICT, AuxiliaryDataDICT, Resolution):
    AuxiliaryNameDICT['SatZenith'] = 'NOMSatelliteZenith'

    
    FilePath = '/FY4COMM/FY4A/PAR/AGRIX/ancillary_data/navigation/fygatNAV.Himawari08.xxxxxxx.'+Resolution+'m.hdf'
    AuxiliaryDataDICT['SatZenith'] = FilePath



AuxiliaryNameDict['Latitude'] = 'Lat'
AuxiliaryNameDict['Longitude'] = 'Lon'

AuxiliaryNameDict['SensorZenith'] = 'SatZenith'
AuxiliaryDataDict['SensorZenith'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATZEN.HDF'

AuxiliaryNameDict['SensorAzimuth'] = 'SatAzimuth'
AuxiliaryDataDict['SensorAzimuth'] = '/FY4COMM/FY4A/COM/AHI8_OBI_'+str(resolution)+'M_NOM_SATAZI.HDF'

AuxiliaryNameDict['LandCover'] = 'LandCover'
AuxiliaryDataDict['LandCover'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LND_'+str(resolution)+'M.HDF'

AuxiliaryNameDict['LandSeaMask'] = 'LandSeaMask'
AuxiliaryDataDict['LandSeaMask'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_LMK_'+str(resolution)+'M.HDF'

AuxiliaryNameDict['DEM'] = 'DEM'
AuxiliaryDataDict['DEM'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_DEM_'+str(resolution)+'M.HDF'

AuxiliaryNameDict['SeaCoast'] = 'SeaCoast'
AuxiliaryDataDict['SeaCoast'] = '/FY4COMM/FY4A/COM/IFL_FY4A_AGRIX_COAST_'+str(resolution)+'M.HDF'


		
		

     
