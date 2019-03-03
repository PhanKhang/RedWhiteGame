import copy
import random

class Node:
    def __init__(self, size, childnum, value):
        self.size = size
        self.chilnum = childnum
        self.children = []
        # в продакшн коде это значение евристики для ноды
        self.value = value
        # в продашн, если гол стейт - 1, определять виктори чеккером, тут тупо 0 всегда
        self.state = 0
        def calculateWeight():
            return random.randint(1, 10)

        #self.weight = calculateWeight()


        def populateChildren():
            for i in range(childnum):
                #newvalue = copy.copy(value)
                newvalue = random.randint(1, 100)
                newnode = Node(self.size - 1, childnum, newvalue)
                self.children.append(newnode)

        if size > 0:
            populateChildren()


mmvalue = []
abvalue = []

def getE3(valuelist, maxP):
    if maxP:
        res = max(valuelist, key=lambda x: x.value)
        return res.value
    else:
        res = min(valuelist,  key=lambda x: x.value)
        return res.value


def minimax(node, depth, maxP, level, trace):
    if depth == 0 or node.state == 1:
        return node.value
    if level == 2 and trace:
        if maxP:
            mmvalue.append(max(node.children, key=lambda x: x.value))
        else:
            arr = node.children
            mmvalue.append(min(arr, key=lambda x: x.value))
    if maxP:
        node.value = -9999999
        for childnode in node.children:
            node.value = max(node.value, minimax(childnode, depth -1, False, level+1, trace))
        return node.value
    else:
        node.value = 9999999
        for childnode in node.children:
            node.value = min(node.value, minimax(childnode, depth - 1, True, level+1, trace))
        return node.value

def alphabeta(node, depth, a, b, maxP, level, trace):
    if depth == 0 or node.state == 1:
        return node.value
    if level == 2 and trace:
        if maxP:
            abvalue.append(max(node.children, key=lambda x: x.value))
        else:
            abvalue.append(min(node.children, key=lambda x: x.value))
    if maxP:
        node.value = -9999999
        newchildren = []
        for childnode in node.children:
            node.value = max(node.value, alphabeta(childnode, depth -1, a, b, False, level+1, trace))
            a = max(a, node.value)
            newchildren.append(childnode)
            if a >= b:
                print("prune!")
                node.children = newchildren
                break
        return node.value
    else:
        node.value = 9999999
        newchildren = []
        if level == 2 and trace:
            abvalue.append(node.value)
        for childnode in node.children:
            node.value = min(node.value, alphabeta(childnode, depth -1, a, b, True, level+1, trace))
            b = min(b, node.value)
            newchildren.append(childnode)
            if a >= b:
                print("prune!")
                node.children = newchildren
                break
        return node.value


def main():
    value = random.randint(1, 100)
    node = Node(2, 2, value)
    minimaxResult = minimax(node, 2, True, 2, True)
    print("minimax l3 value: " + str(getE3(mmvalue, True)))
    print("minimax: "+str(minimaxResult))
    alphabetaResult = alphabeta(node, 2, -9999999, 9999999, True, 2, True)
    print("ab l3 value: " + str(getE3(abvalue, True)))
    print("ab:"+str(alphabetaResult))
    print("Hello")

main()