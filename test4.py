import numpy

class Struct():
        def __init__(self):
            self.a = None
            self.b = None
            self.c = None
            self.d = None
def mainPro(struct):
    struct.a *= struct.a
    struct.b *= struct.b
    struct.c *= struct.c
    struct.d *= struct.d
    return struct
if __name__=="__main__":
    struct = Struct()
    struct.a = numpy.zeros((4,4)) + 1
    struct.b = numpy.zeros((4,4)) + 2
    struct.c = numpy.zeros((4,4)) + 3
    struct.d = numpy.zeros((4,4)) + 4
    print struct.b
    struct_result = mainPro(struct)
    print struct_result.b
