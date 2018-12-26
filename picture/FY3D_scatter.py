#coding=utf8
import matplotlib.pyplot as plt
import numpy

def linear_regression(x, y):
    N = len(x)
    sumx = numpy.sum(x)
    sumy = numpy.sum(y)
    # print x * x
    sumx2 = numpy.dot(x , x)
    sumxy = numpy.dot(x , y)
    A = numpy.mat([[N, sumx], [sumx, sumx2]])
    b = numpy.array([sumy, sumxy])
    return numpy.linalg.solve(A, b)

x = numpy.random.randint(1,30,30)
y = numpy.random.randint(1,100,30)

# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.title("FY3D MERSI B05",y=1.06)
# plt.text(-49,5.05,u"Y=啥,RMSE=啥")
# plt.xlabel("EV-SV")
# plt.ylabel("REFsim")
plt.xlim(0,30)
plt.ylim(0,100)
x_mean = []
y_mean = []
for i in range(len(x)/5):
    print i
    mask = x>i*5
    mask &= x<int(i*5+5)
    # print x[mask]
    y_mean.append(numpy.mean(y[mask]))
    x_mean.append(i*5)
print x_mean
print y_mean
plt.scatter(x,y,s=1)
plt.scatter(x_mean,y_mean,s=4,marker="v",color="red")

a0, a1 = linear_regression(x, y)
_X = [0, 5]
_Y = [a0 + a1 * x for x in _X]
plt.plot(_X,_Y,color='red')
plt.legend()
plt.show()
plt.close()

