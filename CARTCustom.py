class treeNode:
    def __init__(self,feat,val,right,left):
        featureToSplitOn = feat
        valueOfSplit = val
        rightBranch = right
        leftBranch = left

from numpy import *
def loadDataSet(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def binSplitDataSet(dataSet,feature,value):
#Returns the dataset split into two parts
    mat0 = dataSet[nonzero(dataSet[:,feature]>value)[0],:][0]
    mat1 = dataSet[nonzero(dataSet[:,feature]<=value)[0],:][0]
    return mat0,mat1

def createTree(dataSet,leafType = regLeaf,errType = regErr,ops=(1,4)):
#Creates a data structure based on the dataSet
    if feature is None: return value
    retTree['spInd'] = feature
    retTree['spVal'] = value
    lSet,rSet = binSplitDataSet(dataSet,feature,value)
    retTree['left'] = lSet
    retTree['right'] = rset
    return retTree
 
 
def regLeaf(dataSet):
    #Mean of the target variable
    return mean(dataSet)

def regErr(dataSet):
    #Error measurement
    

def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    #Best feature and value to split the data
    if len(set(dataSet[:,-1]).tolist())==1:
        return None,regLeaf(dataSet)
    S=errType(dataSet); tolS=ops[0]; tolN=ops[1]
    bestS=inf; bestIndex=0; bestVal=0; m,n=shape(dataSet)
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0,mat1 = binSplitDataSet(dataSet,featIndex,splitVal)
            if shape(mat0)[0]<tolN or shape(mat0)[0]<tolN:
                return None, leafType(dataSet)
            newS = errType(mat0) + errType(mat1)
            if newS<bestS:
                bestIndex=featIndex
                bestVal=splitVal
                bestS = newS
    if (S-bestS)<tolS:
        return None, leafType(dataSet)
    mat0,mat1 = binSplitDataSet(dataSet,bestIndex,bestVal)
    if shape(mat0)[0]<tolN or shape(mat0)[0]<tolN:
        return None,leafType(dataSet)
    return bestIndex,bestVal

#Post-Pruning the tree to improve the quality of the forecast
def isTree(obj):
    return (type(obj).__name__='dict')

def getMean(tree):
    if isTree(tree['left']): tree['left'] = getMean(tree['left'])
    if isTree(tree['right']): tree['right'] = getMean(tree['right'])
    return (tree['left']+tree['right'])/2.0

def prune(tree,testData):
    #Recursive Pruning fraction
    if shape(testData[:,-1])==0:
        return getMean(tree)
    if isTree(tree['left']) or isTree(tree['right']):
        lSet,rSet = binSplitDataSet(testData,tree['spInd'],tree['spInd'])
    if isTree(tree['left']): tree['left'] = prune(tree['left'],lSet)
    if isTree(tree['right']): tree['right'] = prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge = sum(power(lSet[:,-1],tree['left'],2)) +\
                       sum(power(rSet[:,-1],tree['right'],2))
        treeMean = (tree['left']+tree['right'])/2.0
        errorMerge = sum(power(testData[:,-1]-treeMean,2))
        if errorMerge<errorNoMerge:
            return treeMean
        else: return tree
    else: return tree
    
    
    
    
    

#Leaf generation function for model trees
def modelTreeEval(model,inDat):
 
 

def treeForeCast(tree,inData,modelEval=modelTreeEval):
    #Go to evaluation if you hit a leaf node
    if isTree(tree): return modelEval(tree,inData)
    if inData[tree['spInd']]>inData['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData)
        else:
            return modelEval(tree['right'],inData)
        
def createForeCast(tree,testData,modelEval = None):
    #Evaluate the prediction for each data point in the test set
 


 
 
                  
                                    
