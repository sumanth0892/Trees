import os
import numpy as np
def loadDataSet(fileName):
    labelMat = []; dataMat = []
    fr = open(fileName,'r')
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        labelMat.append(labelMat[2])
        dataMat.append([lineArr[0],lineArr[1]])
    return dataMat,labelMat

#Building a weak learner with a decision stump
def classify(dataMat,D,thresHold,threshIneq):
    #D is the dimension and thresHold is the cut-off value
    retArray = np.ones((shape(dataMat)[0],1))
    if threshIneq == 'lt':
        retArray[dataMat[:,D]<=thresHold] = -1.0
    else:
        retArray[dataMat[:,D]>thresHold] = -1.0
    return retArray


#Build the stump
def buildStumps(dataMat,labelMat,D):
    dataMat = np.mat(dataMat); labelMat = mat(labelMat)
    m,n = shape(dataMat)
    nSteps = 10.0; bestStump = {}; bestClassEstimate = mat(zeros((m,1)))
    minErr = np.inf
    for i in range(n):
        rMin = dataMat[:,i].min(); rMax = dataMat[:,i].max()
        stepSize = (rMax - rMin)/nSteps
        for j in range(-1,int(nSteps)+1):
            for inequal in ['lt','gt']:
                thresHold = (rMin + float(j)*stepSize)
                predictions = classify(dataMat,i,thresHold,inequal)
                errA = mat(ones((m,1)))
                errA[predictedVals == labelMat] = 0
                weightedErr = D.T*errA
                if weightedErr<minErr:
                    minErr = weightedErr
                    bestClassEstimate = predictions.copy()
                    bestStump['dimension'] = i
                    bestStump['thresHold'] = thresHold
                    bestStump['ineq'] = inequal
    return bestStump,minErr,bestClassEstimate

#The full Adaptive boosting algorithm
def adaBoostTrainDS(dataMat,labelMat,iterations = 40):
    weakArr = []; m = shape(dataMat)[0]; D = mat(ones((m,1))/m)
    aggEstimate = mat(zeros((m,1)))
    for i in range(iterations):
        bestStump,error,classEstimate = buildStump(dataMat,labelMat,D)
        alpha = float(0.5*log(1.0-error)/max(error,1e-15))
        bestStump['alpha'] = alpha
        weakArr.append(bestStump)
        exponent = multiply(-1*alpha*mat(labelMat).T,classEstimate)
        D = multiply(D,exp(exponent))
        D = D/D.sum()
        aggEstimate+=alpha*classEstimate
        aggErrors = multiply(sign(aggEstimate)!=mat(labelMat).T,ones((m,1)))
        errRate = aggErrors.sum()/m
        print("Total error: ",errRate,"\n")
        if errRate == 0.0: break
    return weakArr
