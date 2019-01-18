import h5py

if __name__=="__main__":
    # inputFile = r"D:\temp_10.24.189.195\20190109\FY4A-_LMI---_N_REGX_1047E_L1B_EVT-_SING_NUL_20190107104510_20190107105449_7800M_N06V1.HDF"
    inputFile = r"D:\temp_10.24.189.195\20190109\FY4A-_LMI---_N_REGX_1047E_L1B_EVT-_SING_NUL_20190108232510_20190108233449_7800M_N07V1.HDF"
    length = 0
    with h5py.File(inputFile) as f_hdf:
        names = f_hdf["VData"].keys()
        for name in names:
            print name
            data = f_hdf["VData"][name].value
            print len(data)
            length = length + len(data)
    print length
