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


def alphabeta(node, depth, a, b, maxP):
    if depth == 0 or node.state == 1:
        return node.value
    if maxP:
        node.value = -9999999
        newchildren = []
        for childnode in node.children:
            node.value = max(node.value, alphabeta(childnode, depth -1, a, b, False))
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
        for childnode in node.children:
            node.value = min(node.value, alphabeta(childnode, depth -1, a, b, True))
            b = min(b, node.value)
            newchildren.append(childnode)
            if a >= b:
                print("prune!")
                node.children = newchildren
                break
        return node.value


def main():
    value = random.randint(1, 100)
    node = Node(4, 2, value)
    alphabeta(node, 4, -9999999, 9999999, True)
    print("Hello")

main()