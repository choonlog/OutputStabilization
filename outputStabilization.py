import re
import sys
import itertools
from sympy.logic.boolalg import to_dnf
from sympy.logic import simplify_logic
import networkx as nx



def canalizing(modeltext, canalizing_node_dic):

    # Strip whitespace
    modeltext = modeltext.strip()

    # Split text lines
    modeltext_lines = modeltext.splitlines()

    all_state_dic = {}
    for line in modeltext_lines:
        target_node = line.split(" = ")[0]
        if target_node in canalizing_node_dic:
            all_state_dic[target_node] = canalizing_node_dic[target_node]
        else:
            all_state_dic[target_node] = ""
    # print("step 1: " + str(canalizing_node_dic))

    process = True
    idx = 1
    while process:

        idx += 1

        canalizing_node_dic_extra = {}
        for line in modeltext_lines:
            target_node = line.split(" = ")[0]
            Boolean_expression = line.split(" = ")[1]
            Boolean_expression_node_list = list(set(re.findall(r'\w+', Boolean_expression.replace("and ", "").replace("or ", " ").replace("not ", " "))))

            if canalizing_node_dic.get(target_node) == None:
                state_already_fixed_dic = {}
                Boolean_expression_node_list_extra = []
                for Boolean_expression_node in Boolean_expression_node_list:
                    if canalizing_node_dic.get(Boolean_expression_node) != None:
                        state_already_fixed_dic[Boolean_expression_node] = str(canalizing_node_dic.get(Boolean_expression_node))
                    else:
                        Boolean_expression_node_list_extra.append(Boolean_expression_node)

                Boolean_expression_node_list = Boolean_expression_node_list_extra.copy()
                combination_number = len(Boolean_expression_node_list)
                result_bool_list = []
                for k in range(0, combination_number + 1):
                    for combi in itertools.combinations(Boolean_expression_node_list, k):
                        state_dic = state_already_fixed_dic.copy()
                        for node in combi:
                            state_dic[node] = "True"
                        for node in set(Boolean_expression_node_list) - set(combi):
                            state_dic[node] = "False"

                        result_bool = eval(re.sub(r"\b(\w+)\b", lambda m: state_dic.get(m.group(1), m.group(1)), Boolean_expression))
                        result_bool_list.append(result_bool)

                        if len(set(result_bool_list)) == 2:
                            exit_check = True
                        else:
                            exit_check = False

                    if exit_check:
                        break

                if len(set(result_bool_list)) == 1:
                    canalizing_node_dic_extra[target_node] = result_bool_list[0]
                    all_state_dic[target_node] = result_bool_list[0]


            else:
                continue


        canalizing_node_dic.update(canalizing_node_dic_extra)

        if len(canalizing_node_dic_extra) == 0:
            process = False
        else:
            pass
            # print("step " + str(idx) + ": " + str(canalizing_node_dic_extra))


    return all_state_dic



def recursive_tree(target_list, path_node_list, all_path_list, directG):
    for target in target_list:
        path_node_list_extra = path_node_list.copy()
        path = list(nx.dfs_edges(directG, source=target))
        if len(path) == 0:
            path = [(target, target)]

        for edge in path:
            for node in edge:
                if node not in path_node_list_extra:
                    path_node_list_extra.append(node)
        last_node = path_node_list_extra[-1]
        if last_node.find("&") > 0:
            divergent_node_list = re.findall(r'\w+', last_node)

            for divergent_node in divergent_node_list:
                if divergent_node in path_node_list_extra:
                    if path_node_list_extra not in all_path_list:
                        all_path_list.append(path_node_list_extra)
                else:
                    recursive_tree([divergent_node], path_node_list_extra, all_path_list, directG)
        else:
            all_path_list.append(path_node_list_extra)

    return all_path_list



def recursive_common_input(target_list, all_path_list):
    all_path_node_list = []
    for path in all_path_list:
        all_path_node_list.extend(path[1:])
    all_path_node_dic = {i: all_path_node_list.count(i) for i in all_path_node_list}

    descent_node_list = max(all_path_node_dic.items(), key=lambda x: x[1])
    max_node_list = list()
    for key, value in all_path_node_dic.items():
        if value == descent_node_list[1]:
            max_node_list.append(key)

    max_node_dic = {}
    for max_node in max_node_list:
        each_node_list = re.findall(r'\w+', max_node)
        max_node_dic[max_node] = len(each_node_list)

    descent_node_list = min(max_node_dic.items(), key=lambda x: x[1])
    max_node_list = list()
    for key, value in max_node_dic.items():
        if value == descent_node_list[1]:
            max_node_list.append(key)

    control_input_list_list = []
    for max_node in max_node_list:
        all_path_list_extra = all_path_list.copy()
        process = True
        control_input_list = []
        all_path_node_list = []
        while process:

            control_input_list.append(max_node)

            residual_path_list = []
            for path_list in all_path_list_extra:
                if max_node not in path_list:
                    residual_path_list.append(path_list)
            all_path_list_extra = residual_path_list.copy()
            if len(all_path_list_extra) == 0:
                control_input_list_list.append(control_input_list)
                break

            for path in all_path_list_extra:
                all_path_node_list.extend(path[1:])
            all_path_node_dic = {i: all_path_node_list.count(i) for i in all_path_node_list}

            descent_node_list = max(all_path_node_dic.items(), key=lambda x: x[1])
            max_node_list = list()
            for key, value in all_path_node_dic.items():
                if value == descent_node_list[1]:
                    max_node_list.append(key)

            max_node_dic = {}
            for max_node in max_node_list:
                each_node_list = re.findall(r'\w+', max_node)
                max_node_dic[max_node] = len(each_node_list)

            max_node = min(max_node_dic, key=max_node_dic.get)

    return control_input_list_list



def graph_search(residualNet, zeroPlusNodeList, x2n_targetList):
    # Boolean network
    modeltext = residualNet



    # Strip whitespace
    modeltext = modeltext.strip()



    # Replace the logics with symbols
    modeltext = re.sub(r"\band\b", "&", modeltext)
    modeltext = re.sub(r"\bor\b", "|", modeltext)
    modeltext = re.sub(r"\bnot\s", "~", modeltext)



    # Split text lines
    modeltextLine = modeltext.splitlines()



    # Get all nodes
    allNodeList = []
    edgeList = []
    for line in modeltextLine:
        allNodeList += re.findall(r'\w+', line)
        target_node = line.split(" = ")[0]
        source_node = line.split(" = ")[1]

        edgeList.append(tuple([target_node, source_node]))

    # Deduplication
    allNodeList = [x for i, x in enumerate(allNodeList) if i == allNodeList.index(x)]
    x2n_targetList = list(set(allNodeList) & set(x2n_targetList))

    if len(x2n_targetList) == 0:
        new_control_input_list = [zeroPlusNodeList]

    else:

        directG = nx.from_edgelist(edgeList, create_using=nx.DiGraph())

        all_path_list = []
        path_node_list = []
        target_list = x2n_targetList
        all_path_list = recursive_tree(target_list, path_node_list, all_path_list, directG)
        all_path_list_extra = []
        for path in all_path_list:
            if len(path) == 1:
                path.append(path[0])
                all_path_list_extra.append(path)
            else:
                all_path_list_extra.append(path)
        all_path_list = all_path_list_extra.copy()
        control_input_list = recursive_common_input(target_list, all_path_list)

        new_control_input_list = []
        for control_input in control_input_list:
            new_control_input = []
            for clause in control_input:
                if clause.find("&") > 0:
                    clause_node_list = re.findall(r'\w+', clause)
                    new_control_input.extend(clause_node_list)
                else:
                    new_control_input.append(clause)
            new_control_input.sort()
            new_control_input_list.append(new_control_input + zeroPlusNodeList)

        new_control_input_list = [x for i, x in enumerate(new_control_input_list) if i == new_control_input_list.index(x)]
    return new_control_input_list



def mappingSolution(solutionListList, replacedAllNodeList, mappingNodeDic, negMappingNodeDic):
    solutionDicList = []
    for solutionList in solutionListList:
        solutionDic = {}
        for solution in solutionList:
            if solution in replacedAllNodeList:
                solutionDic[list(mappingNodeDic.keys())[list(mappingNodeDic.values()).index(solution)]] = True
            else:
                solutionDic[list(mappingNodeDic.keys())[
                    list(mappingNodeDic.values()).index(negMappingNodeDic[solution])]] = False
        solutionDicList.append(solutionDic)

    return solutionDicList



def canalizationEffect(modeltext, canalizingNodeDic):
    '''
    :param modeltext: Network model
    :param canalizingNodeDic: Canalizing node dicttionary
    :return:
        modeltext: Residual network
        canalizedStateVectorDic: Canalized state vector list
        stepCanalizedStateVectorList: Canalized state vector list according to the step
        allStateVectorDic: All state vector dictionary
    '''

    # Strip whitespace
    modeltext = modeltext.strip()

    # Replace the logics with symbols
    modeltext = re.sub(r"\band\b", "&", modeltext)
    modeltext = re.sub(r"\bor\b", "|", modeltext)
    modeltext = re.sub(r"\bnot\b", "~", modeltext)

    # Split text lines
    modeltextLine = modeltext.splitlines()

    # Get all nodes
    allNodeList = []
    for line in modeltextLine:
        allNodeList += re.findall(r'\w+', line)

    # Deduplication
    allNodeList = [x for i, x in enumerate(allNodeList) if i == allNodeList.index(x)]

    # Create a all state vector dictionary with no values
    allStateVectorDic = {}
    for node in allNodeList:
        allStateVectorDic[node] = ""

    # Recursive process
    canalizedStateVectorDic = {}
    stepCanalizedStateVectorList = []
    process = True
    while process:

        # Update canalizing node list
        if canalizingNodeDic:
            for node in canalizingNodeDic:
                allStateVectorDic[node] = canalizingNodeDic[node]

            # Append canalized state vector list according to the step
            stepCanalizedStateVectorList.append(canalizingNodeDic)

            # Merge two dictionaries
            canalizedStateVectorDic = dict(**canalizedStateVectorDic, **canalizingNodeDic)

            # Get canalizing node list
            canalizingNodeList = list(canalizingNodeDic.keys())

            # Split text lines
            modeltextLine = modeltext.splitlines()

            # Apply the canalization effect
            newCanalizingNodeDic = {}
            newModeltext = ""
            for line in modeltextLine:
                str1 = line.split("=")
                stateVariable = str1[0].strip()
                BooleanExpression = str1[1].strip()
                if not stateVariable in canalizingNodeList:
                    for fixedNode in canalizingNodeDic:
                        BooleanExpression = re.sub(r"\b" + fixedNode + r"\b", str(canalizingNodeDic[fixedNode]).lower(), BooleanExpression)
                    simplifiedExpression = simplify_logic(BooleanExpression)
                    if simplifiedExpression in [True, False]:
                        newCanalizingNodeDic[stateVariable] = simplifiedExpression
                    else:
                        newModeltext += stateVariable + " = " + str(simplifiedExpression) + "\n"
            modeltext = newModeltext
            canalizingNodeDic = newCanalizingNodeDic
        else:
            break

    # ordering
    allStateVectorDic = dict(sorted(allStateVectorDic.items(), reverse=False))

    # Remove whitespace
    modeltext = modeltext.strip()

    return modeltext, allStateVectorDic



def allProductCombi(x2n_modeltextLine, x2n_targetList):
    productListList = []
    for line in x2n_modeltextLine:
        BooleanEquationList = line.split(" = ")
        stateVariable = BooleanEquationList[0]
        BooleanExpression = BooleanEquationList[1]

        for target in x2n_targetList:
            if target == stateVariable:
                productList = BooleanExpression.split(" | ")
                productDicList = []
                for product in productList:
                    productDicList.append({stateVariable: product})

                productListList.append(productDicList)

    productCombi = list(itertools.product(*productListList))

    return productCombi



def main(modeltext, targetDic):
    # x2n form
    x2n_prefix = "z"

    # Strip whitespace
    modeltext = modeltext.strip()

    # Replace the logics with symbols
    modeltext = re.sub(r"\band\b", "&", modeltext)
    modeltext = re.sub(r"\bor\b", "|", modeltext)
    modeltext = re.sub(r"\bnot\s", "~", modeltext)

    # Split text lines
    modeltextLine = modeltext.splitlines()

    # Get all nodes
    allNodeList = []
    stateVariableList = []
    BooleanExpressionNodeList = []
    for line in modeltextLine:
        allNodeList += re.findall(r'\w+', line)
        stateVariable = line.split(" = ")[0]
        BooleanExpression = line.split(" = ")[1]
        BooleanExpressionNodeList.extend(re.findall(r'\w+', BooleanExpression))
        stateVariableList.append(stateVariable)

    # Output node list
    outputnodeList = list(set(allNodeList) - set(BooleanExpressionNodeList))
    for node in targetDic:
        if node not in outputnodeList:
            # print(node + " is not an output node!")
            # print("Output node list: " + str(outputnodeList))
            sys.exit()

    # Deduplication and sort
    allNodeList = list(set(allNodeList))
    allNodeLen = len(allNodeList)
    allNodeList.sort()
    x2n_NodeDigitLen = len(str(allNodeLen * 2))

    # Replace node names with numbers
    mappingNodeDic = {}
    for i, node in enumerate(allNodeList):
        replacedNode = x2n_prefix + str(i + 1).zfill(x2n_NodeDigitLen)
        mappingNodeDic[node] = replacedNode

    replacedModeltext = ""
    for line in modeltextLine:
        nodeList = re.findall(r'\w+', line)
        for node in nodeList:
            line = re.sub(r"\b" + node + r"\b", mappingNodeDic[node], line)

        BooleanEquationList = line.split(" = ")
        stateVariable = BooleanEquationList[0].strip()
        BooleanExpression = BooleanEquationList[1].strip()

        replacedModeltext += stateVariable + " = " + BooleanExpression + "\n"

    replacedTargetDic = {}
    for node in targetDic:
        replacedTargetDic[mappingNodeDic[node]] = targetDic[node]
    # print(mappingNodeDic)

    # Split text lines
    replacedModeltextLine = replacedModeltext.splitlines()

    # Get all nodes
    replacedAllNodeList = []
    for line in replacedModeltextLine:
        replacedAllNodeList += re.findall(r'\w+', line)

    # Deduplication and sort
    replacedAllNodeList = list(set(replacedAllNodeList))
    replacedAllNodeLen = len(replacedAllNodeList)
    replacedAllNodeList.sort()

    # Mapping negated nodes
    negMappingNodeDic = {}
    for node in replacedAllNodeList:
        posNodeInt = int(re.findall(r'\d+', node)[0])
        posNode = x2n_prefix + str(posNodeInt).zfill(x2n_NodeDigitLen)

        negNodeInt = posNodeInt + replacedAllNodeLen
        negNode = x2n_prefix + str(negNodeInt).zfill(x2n_NodeDigitLen)

        negMappingNodeDic[posNode] = negNode
        negMappingNodeDic[negNode] = posNode

    x2n_targetList = []
    for node in replacedTargetDic:
        if replacedTargetDic[node] == True:
            x2n_targetList.append(node)
        else:
            x2n_targetList.append(negMappingNodeDic[node])
    S_indexList_ori = x2n_targetList.copy()
    ori_x2n_targetList = x2n_targetList.copy()
    x2n_target_complementaryNodeList = [negMappingNodeDic[x] for x in x2n_targetList]


    # SOP and Negate
    posModeltext = ""
    negModeltext = ""
    for line in replacedModeltextLine:
        BooleanEquationList = line.split(" = ")
        stateVariable = BooleanEquationList[0]
        BooleanExpression = BooleanEquationList[1]
        posModeltext += stateVariable + " = " + str(to_dnf(BooleanExpression, True)) + "\n"
        negModeltext += negMappingNodeDic[stateVariable] + " = " + str(
            to_dnf("~(" + BooleanExpression + ")", True)) + "\n"

    # Merge oriModeltext and negModeltext
    x2n_modeltext = posModeltext + negModeltext

    # Replace node names
    x2n_modeltextLine = x2n_modeltext.splitlines()
    x2n_modeltextExtra = ""
    for line in x2n_modeltextLine:
        BooleanEquationList = line.split(" = ")
        stateVariable = BooleanEquationList[0]
        BooleanExpression = BooleanEquationList[1]

        negNodeList = re.findall(r'~\w+', BooleanExpression)
        for negNode in negNodeList:
            BooleanExpression = re.sub(negNode, negMappingNodeDic[negNode.replace("~", "")], BooleanExpression)
        x2n_modeltextExtra += stateVariable + " = " + BooleanExpression + "\n"
    x2n_modeltext = x2n_modeltextExtra.strip()
    x2n_modeltextLine = x2n_modeltext.splitlines()

    # All possible products
    productCombi = allProductCombi(x2n_modeltextLine, x2n_targetList)

    # For all reduced BNs
    solutionListList = []
    BN_num = 0
    for productDicSet in productCombi:
        x2n_targetList = S_indexList_ori.copy()
        S_indexList = S_indexList_ori.copy()
        BN_num += 1

        # Check the conflict of products
        isConflict = False
        productStrList = []
        for productDic in productDicSet:
            productStr = list(productDic.values())[0]
            productStrList.append(re.findall(r'\w+', productStr))
        productSetCombi = list(itertools.product(*productStrList))

        for productSet in productSetCombi:
            productSetCopy = set(productSet).copy()
            for productCopy in productSet:
                if negMappingNodeDic[productCopy] in productSetCopy - {productCopy}:
                    isConflict = True
        if isConflict:
            continue

        # Not conflict products
        x2n_modeltextPossible = ""
        for line in x2n_modeltextLine:
            BooleanEquationList = line.split(" = ")
            stateVariable = BooleanEquationList[0]
            BooleanExpression = BooleanEquationList[1]

            isTarget = False
            for productDic in productDicSet:
                product = productDic.get(stateVariable)
                if product != None:
                    isTarget = True
                    selectedTerm = product

            if isTarget:
                x2n_modeltextPossible += stateVariable + " = " + selectedTerm + "\n"
            else:
                x2n_modeltextPossible += stateVariable + " = " + BooleanExpression + "\n"

        step1 = True
        expandLen = 0
        zeroPlusNodeList = []
        while step1:
            expandLen += 1

            # Recursive expansion(based on each BN)
            x2n_modeltextPossible = x2n_modeltextPossible.strip()
            x2n_modeltextPossibleLine = x2n_modeltextPossible.splitlines()

            productNodeList = []
            for line in x2n_modeltextPossibleLine:
                BooleanEquationList = line.split(" = ")
                stateVariable = BooleanEquationList[0]
                BooleanExpression = BooleanEquationList[1]

                for target in x2n_targetList:
                    if target == stateVariable:
                        productNode = re.findall(r'\w+', BooleanExpression)
                        productNodeList.extend(productNode)

            productNodeList = list(set(productNodeList) - set(S_indexList))
            if len(productNodeList) == 0:
                break

            S_indexList.extend(productNodeList.copy())
            complementaryNodeList = []
            for node in productNodeList:
                complementaryNodeList.append(negMappingNodeDic[node])

            step2 = True
            chainRemovalLen = 0
            while step2:
                chainRemovalLen += 1
                complementaryNodeListExtra = []
                x2n_modeltextPossibleExtra = ""
                for line in x2n_modeltextPossibleLine:
                    BooleanEquationList = line.split(" = ")
                    stateVariable = BooleanEquationList[0]
                    BooleanExpression = BooleanEquationList[1]

                    if stateVariable not in complementaryNodeList + x2n_target_complementaryNodeList:
                        nodeList = re.findall(r'\w+', BooleanExpression)
                        complementaryNodeSet = set(complementaryNodeList)
                        nodeSet = set(nodeList)
                        containList = list(complementaryNodeSet & nodeSet)

                        for node in containList:
                            BooleanExpression = re.sub(node, "false", BooleanExpression)

                        SOP = to_dnf(BooleanExpression, True)
                        if bool(SOP) == False:
                            if stateVariable in S_indexList:
                                if stateVariable not in zeroPlusNodeList:
                                    zeroPlusNodeList.append(stateVariable)
                                x2n_modeltextPossibleExtra += stateVariable + " = " + stateVariable + "\n"
                            else:
                                complementaryNodeListExtra.append(stateVariable)
                        else:
                            x2n_modeltextPossibleExtra += stateVariable + " = " + str(SOP) + "\n"
                x2n_modeltextPossibleExtra = x2n_modeltextPossibleExtra.strip()

                if len(complementaryNodeListExtra) == 0:
                    step2 = False

                x2n_modeltextPossibleLine = x2n_modeltextPossibleExtra.strip().splitlines()
                complementaryNodeList = complementaryNodeListExtra

            x2n_targetList = list(set(productNodeList) - set(zeroPlusNodeList))
            productCombi = allProductCombi(x2n_modeltextPossibleLine, x2n_targetList)

            before_num = 1000
            numConflict = 0
            for productDicSet in productCombi:
                # Check the conflict of products
                isConflict = False
                productStrList = []
                for productDic in productDicSet:
                    productStr = list(productDic.values())[0]
                    productStrList.append(re.findall(r'\w+', productStr))
                productSetCombi = list(itertools.product(*productStrList))

                for productSet in productSetCombi:
                    productSetCopy = set(productSet).copy()
                    for productCopy in productSet:
                        if negMappingNodeDic[productCopy] in productSetCopy - {productCopy}:
                            isConflict = True
                if isConflict:
                    numConflict += 1
                    continue

                productStrList = []
                for productDic in productDicSet:
                    productStr = list(productDic.values())[0]
                    productStrList.extend(re.findall(r'\w+', productStr))

                current_num = len(set(productStrList) - set(S_indexList))
                current_productDicSet = productDicSet

                if current_num < before_num:
                    before_num = current_num
                    before_productDicSet = current_productDicSet

            if numConflict == len(productCombi):
                step_specialCase = True
                constantNodeList = []
                while step_specialCase:
                    incompatibleNodeList = []
                    conflictCheck = False
                    for productDicSet in productCombi:

                        isConflict = False
                        productStrList = []
                        for productDic in productDicSet:
                            productStr = list(productDic.values())[0]
                            productStrList.append(re.findall(r'\w+', productStr))
                        productSetCombi = list(itertools.product(*productStrList))

                        for productSet in productSetCombi:
                            productSetCopy = set(productSet).copy()
                            for productCopy in productSet:
                                if negMappingNodeDic[productCopy] in productSetCopy - {productCopy}:
                                    conflictCheck = True
                                    incompatibleNodeList.append(
                                        list(productDicSet[productSet.index(productCopy)].keys())[0])
                                    incompatibleNodeList.append(
                                        list(productDicSet[productSet.index(negMappingNodeDic[productCopy])].keys())[0])

                    if conflictCheck != True:
                        break

                    incompatibleNodeList = list(set(incompatibleNodeList))
                    incompatibleNodeList.sort()

                    numMaxDic = {}
                    numMinDic = {}
                    selectProductDic = {}
                    numVaraibleList = []
                    for incompatibleNode in incompatibleNodeList:
                        numMaxDic[incompatibleNode] = []
                        before_num = 1000
                        for productDicSet in productCombi:
                            eachProductConflict = False
                            eachProductList = []
                            current_productDicList = []
                            for productDic in productDicSet:
                                if list(productDic.keys())[0] != incompatibleNode:
                                    eachProductList.extend(re.findall(r'\w+', list(productDic.values())[0]))
                                    current_productDicList.append(productDic)
                                elif list(productDic.keys())[0] == incompatibleNode:
                                    numMaxDic[incompatibleNode].append(
                                        len(re.findall(r'\w+', list(productDic.values())[0])))

                            eachProductList = list(set(eachProductList) - {incompatibleNode} - set(S_indexList))
                            eachProductList.sort()

                            current_num = len(eachProductList)
                            current_productDicSet = tuple(current_productDicList)

                            if current_num < before_num:
                                before_num = current_num
                                before_productDicSet = current_productDicSet

                        selectProductDic[incompatibleNode] = [before_productDicSet, before_num]
                        numVaraibleList.append(before_num)

                        numMinDic[incompatibleNode] = before_num
                        numMaxDic[incompatibleNode] = min(numMaxDic[incompatibleNode])

                    itemMinValue = min(numMinDic.items(), key=lambda x: x[1])
                    listOfKeys = list()
                    for key, value in numMinDic.items():
                        if value == itemMinValue[1]:
                            listOfKeys.append(key)

                    if len(listOfKeys) == 1:
                        constantNode = listOfKeys[0]
                        before_productDicSet = selectProductDic[listOfKeys[0]][0]
                    elif len(listOfKeys) > 1:
                        constantNode = max(numMaxDic, key=numMaxDic.get)
                        before_productDicSet = selectProductDic[max(numMaxDic, key=numMaxDic.get)][0]

                    constantNodeList.append(constantNode)
                    productCombi = [before_productDicSet]

                for constantNode in constantNodeList:
                    if constantNode not in zeroPlusNodeList:
                        zeroPlusNodeList.append(constantNode)

                for constantNode in constantNodeList:
                    if constantNode not in S_indexList:
                        S_indexList.append(constantNode)

            productDicSet = before_productDicSet

            # Not conflict products
            x2n_modeltextPossible = ""
            for line in x2n_modeltextPossibleLine:
                BooleanEquationList = line.split(" = ")
                stateVariable = BooleanEquationList[0]
                BooleanExpression = BooleanEquationList[1]

                isTarget = False
                for productDic in productDicSet:
                    product = productDic.get(stateVariable)
                    if product != None:
                        isTarget = True
                        selectedTerm = product

                if isTarget:
                    x2n_modeltextPossible += stateVariable + " = " + selectedTerm + "\n"
                else:
                    x2n_modeltextPossible += stateVariable + " = " + BooleanExpression + "\n"

        # Network modification for FVS application
        S_modeltext = ""
        stateVariable_nodeList = []
        BooleanExpression_noeList = []
        for line in x2n_modeltextPossible.strip().splitlines():
            BooleanEquationList = line.split(" = ")
            stateVariable = BooleanEquationList[0]
            BooleanExpression = BooleanEquationList[1]
            if stateVariable in S_indexList:
                S_modeltext += stateVariable + " = " + BooleanExpression + "\n"

        for line in S_modeltext.strip().splitlines():
            BooleanEquationList = line.split(" = ")
            stateVariable = BooleanEquationList[0]
            BooleanExpression = BooleanEquationList[1]

            stateVariable_nodeList.append(stateVariable)
            BooleanExpression_noeList += re.findall(r'\w+', BooleanExpression)

        inputNodeList = list(set(BooleanExpression_noeList) - set(stateVariable_nodeList))
        for inputNode in inputNodeList:
            S_modeltext += inputNode + " = " + inputNode + "\n"
        S_modeltext = S_modeltext.strip()
        canalizingNodeDic = {zeroPlusNode: True for zeroPlusNode in zeroPlusNodeList}

        # Residual network
        residualNet, _ = canalizationEffect(S_modeltext, canalizingNodeDic)

        # FVS
        if residualNet:
            # solutionList = FVS_finder(residualNet, zeroPlusNodeList)
            solutionList = graph_search(residualNet, zeroPlusNodeList, ori_x2n_targetList)
        else:
            solutionList = [zeroPlusNodeList]
        solutionListList.extend(solutionList)

    try:
        solutionListList = [x for i, x in enumerate(solutionListList) if i == solutionListList.index(x)]
        solutionListList_len = []
        for solutionList in solutionListList:
            solutionListList_len.append(len(solutionList))
        minimum_length = min(solutionListList_len)
        solutionDicList = mappingSolution(solutionListList, replacedAllNodeList, mappingNodeDic, negMappingNodeDic)

        solutionDicList_extra = []
        for solutionDic in solutionDicList:
            if len(solutionDic) == minimum_length:
                solutionDic_len = len(solutionDic)
                # print("solutionDic", solutionDic)
                for length in range(1, solutionDic_len + 1):
                    table_list = list(itertools.combinations(list(solutionDic.keys()), length))
                    table_check = True
                    for table in table_list:
                        canalizingNodeDic = {}
                        for node in table:
                            canalizingNodeDic[node] = solutionDic[node]
                        canalized_node_dic = canalizing(modeltext, canalizingNodeDic)
                        target_check = True
                        for target in targetDic:
                            if canalized_node_dic.get(target) != targetDic[target]:
                                target_check = False
                        if target_check == True:
                            # print(table, canalized_node_dic)
                            table_dic_extra = {}
                            for table_node in table:
                                table_dic_extra[table_node] = solutionDic[table_node]
                            solutionDicList_extra.append(table_dic_extra)

                            table_check = False
                            break
                    if table_check == False:
                        break
        solutionDicList = solutionDicList_extra
    except:
        solutionDicList = []

    return solutionDicList



modeltext = '''
x01 = not x06 and not x04
x02 = x01 or (x07 and x05) or (x03 and x02)
x03 = x01
x04 = (x08 and x07) or (x08 and x05)
x05 = (x07 and x08 and x03) or (x08 and x03 and x01)
x06 = x06 and not x08
x07 = (x02 and x01 and x06) or (x02 and x01 and x07)
x08 = x04 and not x02 and not x01
x09 = x03
x10 = x08 or (x05 and x02) or x11
'''
targetDic = {'x09': True, 'x10': True}



solutionDicList = main(modeltext, targetDic)
print(solutionDicList)
