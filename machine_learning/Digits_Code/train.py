import numpy
import operator
def classify(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = numpy.tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    tmp = sorted(distances)
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.values(), reverse=True)
    # tmp = classCount.items()
    sortedClassCount=sorted(classCount.items(),key=lambda x:x[1],reverse=True)
    print(sortedClassCount)
    return sortedClassCount[0][0]
def readFile(filename):
    f = open(filename)
    lines = f.readlines()
    numberOfLines = len(lines)         #get the number of lines in the file
    returnMat = numpy.zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return
    index = 0
    for line in lines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    m = dataSet.shape[0]
    normDataSet = (dataSet - numpy.tile(minVals, (m,1)))/numpy.tile((maxVals-minVals),(m,1))
    return normDataSet

if __name__=="__main__":
    hoRatio = 0.03
    datingDataMat,datingLabels = readFile('./datingTestSet2.txt')       #load dataset from file
    length = datingDataMat.shape[0]
    normMat = autoNorm(datingDataMat)
    numTestVecs = int(length*hoRatio)
    errorCount = 0
    for i in range(numTestVecs):
        classifierResult = classify(normMat[i,:],normMat[numTestVecs:,:],datingLabels[numTestVecs:],10)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1
        print(i)
    print("the total error rate is: %f" % (errorCount/float(numTestVecs)))
    print( errorCount)
