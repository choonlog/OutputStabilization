"""
Code author : Chun-Kyung Lee(Korea Advanced Institute of Science and Technology)
Contact: chunkyung@kaist.ac.kr
"""
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import random
import pickle




def main(nodeNum, minIndegree, maxIndegree, outputNum):



    # Load biological Boolean logic from Cell Collective
    totalLogicDic = pickle.load(open("./newTotalLogicDic.p", "rb"))



    # Generate random Boolean network
    a = 100.  # shape
    m = 1.  # mode
    allNodeLength = nodeNum
    allNodeWithoutOutputLength = nodeNum - outputNum
    data = (np.random.pareto(a, allNodeLength) + 1) * m

    data = np.reshape(data, (-1, 1))
    scaler = MinMaxScaler(copy=True, feature_range=(minIndegree, maxIndegree))  # Column을 기준으로 한다.
    scaler.fit(data)
    data = scaler.transform(data)
    data = np.round(data)
    data = np.reshape(data, (-1))
    data = data.tolist()

    indegreeList = list(map(int, data))
    fillNumber = len(str(allNodeLength))
    allNodes = ["x" + str(i).zfill(fillNumber) for i in range(1, allNodeLength + 1)]
    allNodesWithoutOutput = ["x" + str(i).zfill(fillNumber) for i in range(1, allNodeWithoutOutputLength + 1)]
    formatAttr = ""
    formatNormal = ""
    for k in allNodes:
        initialStateLine = k + " = Random" + "\n"
        formatAttr = formatAttr + initialStateLine
    formatAttr = formatAttr + "\n\n"
    for node, indegree in zip(allNodes, indegreeList):
        selectedNodes = random.sample(allNodesWithoutOutput, indegree)
        biologicalRandomLogic = random.choice(totalLogicDic[str(indegree)])
        for n, selectNode in enumerate(selectedNodes):
            existingNode = "z" + str(n + 1).zfill(2)
            biologicalRandomLogic = biologicalRandomLogic.replace(existingNode, selectNode)
        biologicalRandomLogic = biologicalRandomLogic.replace("&", "and").replace("|", "or").replace("~", "not ")
        formatNormal = formatNormal + node + " = " + biologicalRandomLogic + "\n"
        formatAttr = formatAttr + node + " *= " + biologicalRandomLogic + "\n"



    return formatNormal



Boolean_network = main(20, 1, 3, 2)
print(Boolean_network)