import numpy

a = [[1,2],[3,4]]
b = [11,22,33,44,55]
a = numpy.array(a,dtype=int)
b = numpy.array(b,dtype=int)

c = b[numpy.array([[0,0],[1,2],[3,4]])]
print c