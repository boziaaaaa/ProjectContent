import numpy.ctypeslib 
from ctypes import c_int
from ctypes import c_float
       
def useC():
  
  cpp_so = numpy.ctypeslib.load_library("/home/bozi/Downloads/t/a","so")  

  cpp_so.add.argtypes = [c_int,c_int]
  cpp_so.add.restype = c_int
  input1 = 1
  input2 = 2
  output = cpp_so.add(input1,input2)

  p_int = numpy.ctypeslib.ndpointer(dtype = numpy.int32,ndim = 1,flags = "CONTIGUOUS")
  cpp_so.Switch.argtypes = [p_int,p_int]
  cpp_so.Switch.restypes = c_int  
  t1 = numpy.zeros(1)
  t2 = numpy.zeros(1)
  t1[0] = 3
  t2[0] = 4  
  t1 = t1.astype(numpy.int32)
  t2 = t2.astype(numpy.int32)  
  output = cpp_so.Switch(t1,t2)
  t1 = int(t1)
  t2 = int(t2)
  print t1,t2

if __name__ ==    "__main__":
   useC()

