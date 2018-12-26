import numpy
def getUV(x, y):
    dpp = 20
    f = x > 180
    f |= x < -180
    x+=180
    # x[x < 0] += 360
    x[x > 360] = 360

    x *= dpp
    y = 90 - y
    y[y > 180] = 180
    y[y < 0] = 180
    y *= dpp
    return x.astype('u2'), y.astype('u2'), f == False

if __name__=="__main__":
    y,x = numpy.array([[31.95000, - 114.1000],[31.95000 ,- 114.1000]]).T
    r  = getUV(x, y)
    print r
