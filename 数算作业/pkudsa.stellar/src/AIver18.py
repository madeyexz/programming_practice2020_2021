from random import choices
# from MapDesign import g_design4
import MapDesign
from time import time_ns
from copy import deepcopy
from Node import Node
from GameMap import GameMap
from HexagonForce import Generate_Hexagon
from copy import deepcopy
from collections import defaultdict


# class betterNode():
#     def __init__(self, node, playerID, N):
#         self.playerID = playerID
#         self.enemyID = 0 if self.playerID else 1
#         self.number = node.number
#         self.power = node.power  # 重要！！！power现在起是元组类型！！！
#         self.belong = node.belong
#         self.spawn_rate = node.spawn_rate
#         self.despawn_rate = node.despawn_rate
#         self.power_limit = node.power_limit
#         self.belongRoad = -1
#         self.mainRoadDistance = 99
#         self.ID = 1
#         self.forwardNode = None
#         self.backwardNode = None
#         self.transferNode = None
#         self.boarderDistance = 3
#         self.baseDistance = 99
#         self.next = set(node.get_next())
#         self.nextTwo = set()
#         self.nearMine = set()
#         self.nearMinePower = 0
#         self.nearTwoMinePower = 0
#         self.nearEnemy = set()
#         self.nearTwoEnemy = set()
#         self.nearEnemyPower = 0
#         self.nearTwoEnemyPower = 0
#         self.nearNeutralNode = deepcopy(self.next)
#         if 1 in self.nearNeutralNode:
#             self.nearNeutralNode.remove(1)
#         if N + 1 in self.nearNeutralNode:
#             self.nearNeutralNode.remove(1)
#         self.getPower = 0
#
#     @property
#     def get_next(self):
#         return self.next
#
#     def

# nodeInfo : dict , 訪問方式 nodeInfo[num]


class player_class:  # 格式要求
    def __init__(self, player_id: int):
        """Debug"""
        self.refreshTimer = 0
        """/Debug"""
        self.time = 0  # 運行次數
        self.player_id = player_id
        # 邊界節點表
        # 自家大本營 與敵人大本營 只有在得一次運行player_func才會正確更新
        self.mine_base = None
        self.enemy_base = None
        self.firstTime = True
        # 1:{"主道路" : True,"歸屬": 1 ,"距離主道路" : 1,"身份" : 1, "邊界距離": 0,"附近的友方節點": [], "敵方節點" : [], "中立節點" : [], "輔助...": 0}
        self.nodeInfo = {}
        self.mainRoadNode = []  # 三條主路上的節點 [[1,2,3,4],[1,2,6,8],[...]]
        self.nodes = {}  #
        self.idNodes = {i: set() for i in range(4)}  # 0 為所有主道路的node 1為開拓者 2為邊防者 3為傳輸者
        self.maxTransferDistance = 0
        self.maxMainRoadDistance = 0
        self.maxMineNode = (0, 0)  # 第一個是節點號碼,第二個是數量
        self.attack = False
        self.attackState = 0
        self.baseattackState = 7
        self.attactingNode = 0

    def clarify(self,map_info):
        '''分类函数，返回值为一个三元元组，格式为(我方所有据点列表，对方所有据点列表，空据点列表)'''
        #初始化返回值，分别为我方据点，对方据点，空据点
        my_nodes=[]
        enemy_nodes=[]
        empty_nodes=[]
        #顺序扫描所有节点，按照其belong值归类到不同的列表(我方，对方，空)
        for node in map_info.nodes:
            if node.belong==self.player_id:
                my_nodes.append(node.number)
            elif node.belong==1-self.player_id:
                enemy_nodes.append(node.number)
            else:
                empty_nodes.append(node.number)
        #特殊处理标号为1的节点(没有用)
        empty_nodes.remove(0)
        return (my_nodes,enemy_nodes,empty_nodes)

    def _init2(self, map_info: GameMap):
        # 提取map中所有節點資訊 防止多次递歸調用
        self.nodes = map_info.nodes
        # 長度確定
        self.N = map_info.N

        if self.player_id:
            self.enemy_id = 0
            self.enemy_base = 1
            self.mine_base = self.N
        else:
            self.enemy_id = 1
            self.mine_base = 1
            self.enemy_base = self.N

        # 建立邊界的節點集合
        self.mine_boarder = {self.mine_base}
        self.enemy_boarder = {self.enemy_base}

        # 字典構造 :
        self._buildNodeDict()
        # 道路建造 :
        self.find_mainroad()
        self._refresh_Forward_and_Backward()
        # 字典更新 :
        self._firstDictRefresh()
        # 大本營距離更新
        self._baseDistanceRefresh()

    # 1. 更新nodeInfo#

    # 1.5. 決定先處理哪些節點

    # 2. 每個身份要做的事情
    # 身份 : .

    # 確立自方大本營與敵方大本營

    def player_func(self, map_info: GameMap):
        # 得到地圖後的初始化
        if self.firstTime:
            self.firstTime = False
            self._init2(map_info)
        else:
            self.map_info = map_info
            self.nodes = map_info.nodes
            t1 = time_ns()
            self._refresh()
            self.refreshTimer = time_ns() - t1
        self._refresh_marker()
        nextNodeGen = self.searchNodeGen()
        action = []
        for nodeNum in nextNodeGen:
            action.extend(self.doNode(nodeNum))
        if self.attackState == self.baseattackState:
            action.extend(self.attackSt1())
        elif self.attackState == self.baseattackState - 1:
            action.extend(self.attackSt2())
        self.time += 1
        if self.attackState > 0:
            self.attackState -= 1
        self.tmp_left = [i.power[self.player_id] for i in self.nodes]
        for check in action:
            if not self.isValid(check):
                action.remove(check)
        return action

    def doNode(self, num) -> list:  # return 指令
        if num == 21:
            print("im21")
        if self.nodeInfo[num]["ID"] == 1:  # 身份 1為開拓者 2為邊防者 3為傳輸者
            # your code here
            info = self.nodeInfo[num]
            nowPower = self.nodes[num].power[self.player_id]
            recPower = info['getPower']
            totalPower = nowPower + recPower
            givenNode = info["nearNeutralNode"]
            targetNode = []
            sendedNode = []
            for nodeNum in givenNode:
                if self.check[nodeNum] == 0:
                    if self.nodeInfo[nodeNum]["mainRoadDistance"] == 0:
                        targetNode.insert(0, nodeNum)
                    else:
                        targetNode.append(nodeNum)
                else:
                    if self.nodeInfo[nodeNum]["mainRoadDistance"] == 0:
                        sendedNode.insert(0, nodeNum)
                    else:
                        sendedNode.append(nodeNum)

            if totalPower < 34:
                return []
            if len(targetNode) >= 2:
                if recPower > 50:
                    if nowPower > 120:
                        oneGet = nowPower / 2
                        self.check[targetNode[0]] = 1
                        self.check[targetNode[1]] = 1
                        return [(num, targetNode[0], oneGet - 0.1), (num, targetNode[1], oneGet - 0.1)]
                else:
                    if totalPower > 120:
                        oneGet = (totalPower - 50) / 2
                        self.check[targetNode[0]] = 1
                        self.check[targetNode[1]] = 1
                        return [(num, targetNode[0], oneGet - 0.1), (num, targetNode[1], oneGet - 0.1)]
            if targetNode:
                if recPower > nowPower:
                    self.check[targetNode[0]] = 1
                    return [(num, targetNode[0], nowPower - 0.1)]
                bestPower = 12 * (totalPower + 3) / 23
                if nowPower > 108:
                    self.check[targetNode[0]] = 1
                    return [(num, targetNode[0], totalPower - 50.1)]
                if nowPower > bestPower:
                    self.check[targetNode[0]] = 1
                    return [(num, targetNode[0], bestPower - 0.1)]
                else:
                    self.check[targetNode[0]] = 1
                    return [(num, targetNode[0], nowPower - 0.1)]

            else:
                if totalPower > 50:
                    return [(num, sendedNode[0], min(totalPower - 50, nowPower - 0.1))]
                else:
                    return []

        elif self.nodeInfo[num]["ID"] == 2:
            # your code here
            offensive = False
            enemylist = self.nodeInfo[num]["nearEnemyNode"]
            info = self.nodeInfo[num]
            nowPower = self.nodes[num].power[self.player_id]
            recPower = info['getPower']
            totalPower = nowPower + recPower
            for enemy in enemylist:
                if info["nearTwoMinePower"] >= \
                        self.nodeInfo[enemy]["nearTwoEnemyPower"] * 5:  # if we have power 5 times more than enemy
                    offensive = True  # then start a general offensive
            if not offensive:  # if a general offensive isn't started
                if info["nearNeutralNode"]:
                    situationA = False
                    for enemycode in enemylist:
                        if info["nearMinePower"] >= self.nodeInfo[enemycode]["nearEnemyPower"] * 1.5:
                            situationA = True
                            break
                    if situationA:
                        action = []
                        n1 = len(info["nearNeutralNode"])
                        for neu in info["nearNeutralNode"]:
                            action.append((num, neu, min(nowPower, totalPower / (3 * n1)) - 0.1))
                            self.nodeInfo[neu]["getPower"] += totalPower / (3 * n1) - (totalPower / (3 * n1)) ** 0.5
                        attack_target = list(info["nearEnemyNode"])[0]
                        for candidate in info["nearEnemyNode"]:
                            if self.nodeInfo[candidate]["nearTwoEnemyPower"] <= \
                                    self.nodeInfo[attack_target]["nearTwoEnemyPower"]:
                                attack_target = candidate
                        action.append((num, attack_target, min(totalPower / 3, nowPower) - 0.1))
                        self.nodeInfo[num]["nowPower"] = totalPower / 3
                        return action
                        # to renew get
                    else:
                        neighbor = False
                        for neu in info["nearNeutralNode"]:
                            if self.nodeInfo[neu]["nearEnemyNode"]:
                                neighbor = True
                        if neighbor:
                            attack_target = list(info["nearEnemyNode"])[0]
                            for candidate in info["nearEnemyNode"]:
                                if self.nodeInfo[candidate]["nearTwoEnemyPower"] <= \
                                        self.nodeInfo[attack_target]["nearTwoEnemyPower"]:
                                    attack_target = candidate
                            self.nodeInfo[num]["nowPower"] = totalPower / 3
                            self.nodeInfo[attack_target]["getPower"] += (2 * totalPower / 3) - (
                                    2 * totalPower / 3) ** 0.5
                            return [(num, attack_target, min(2 * totalPower / 3, nowPower - 0.1))]
                        else:
                            actions = []
                            n2 = len(info["nearNeutralNode"])
                            for neu in info["nearNeutralNode"]:
                                actions.append((num, neu, min(totalPower / (3 * n2), nowPower) - 0.1))
                                self.nodeInfo[neu]["getPower"] += totalPower / (3 * n2) - (totalPower / (3 * n2)) ** 0.5
                            self.nodeInfo[num]["nowPower"] = totalPower * (2 / 3)
                            return actions
                else:
                    if info["nearMineNode"]:
                        attack_target = list(info["nearEnemyNode"])[0]
                        for candidate in info["nearEnemyNode"]:
                            if self.nodeInfo[candidate]["nearTwoEnemyPower"] <= \
                                    self.nodeInfo[attack_target]["nearTwoEnemyPower"]:
                                attack_target = candidate
                        if info["nearTwoMinePower"] >= info["nearTwoEnemyPower"]:
                            enemyPower = self.nodes[attack_target].power[self.enemy_id]
                            if totalPower >= 2 * enemyPower:
                                self.nodeInfo[num]["nowPower"] = totalPower / 2
                                return [(num, attack_target, min(nowPower, totalPower / 2) - 0.1)]
                            elif 0.5 * totalPower < enemyPower < 0.8 * totalPower:
                                self.nodeInfo[num]["nowPower"] = totalPower / 3
                                return [(num, attack_target, min(nowPower, (2 / 3) * totalPower) - 0.1)]
                            else:
                                if totalPower <= 50:
                                    return []
                                else:
                                    self.nodeInfo[num]["nowPower"] = 50
                                    return [(num, attack_target, min(totalPower - 50, nowPower) - 0.1)]
            return []
        elif self.nodeInfo[num]["ID"] == 3:
            # your code here
            info = self.nodeInfo[num]
            nowPower = self.nodes[num].power[self.player_id]
            boarderDist = self.nodeInfo[num]["boarderDistance"]
            recPower = info['getPower']
            totalPower = nowPower + recPower
            nearMineNode = info["nearMineNode"]
            action = []
            minNear = min((i for i in nearMineNode if self.nodes[i].belong == self.player_id),
                          key=lambda x: self.nodeInfo[x]["getPower"] + self.nodes[x].power[self.player_id])
            nearExpander = [i for i in nearMineNode if self.nodeInfo[i]["ID"] == 1]
            if nearExpander:
                for i in nearExpander:
                    action.extend(self.asBest(num, i))
                return action
            if self.nodeInfo[minNear]["nowPower"] < 10:
                action.extend(self.asBest(num, minNear))
            nowPower = self.nodeInfo[num]["nowPower"]
            if boarderDist == 2:
                try:
                    nodeNum = min((i for i in nearMineNode if
                                   self.nodeInfo[i]["boarderDistance"] == 1),
                                  key=lambda x: self.nodes[x].power[self.player_id])
                    action.extend(self.asMuch(num, nodeNum))
                    return action
                except ValueError:
                    pass
            elif boarderDist == 1:
                try:
                    nodeNum = min((i for i in nearMineNode if
                                   self.nodeInfo[i]["boarderDistance"] == 0),
                                  key=lambda x: self.nodes[x].power[self.player_id])
                    action.extend(self.asMuch(num, nodeNum))
                    return action
                except ValueError:
                    pass

            if self.nodeInfo[num]["mainRoadDistance"] == 0:
                action.extend(self.asMuch(num, self.nodeInfo[num]["forwardNode"]))
            else:
                action.extend(self.asMuch(num, self.nodeInfo[num]["transferNode"]))
            return action

    def _refresh_marker(self):
        self.check = {i: 0 for i in range(1, self.N + 1)}

    def _refresh(self):
        self.maxMineNode = (0, 0)
        self._refresh_Boarder_and_Node()
        for i in range(1, self.N + 1):
            self.nodeInfo[i]["getPower"] = 0
            self.nodeInfo[i]["nowPower"] = self.nodes[i].power[self.nodes[i].belong]

    def _refreshNode(self, num: int):
        nowNode_in_nodeInfo = self.nodeInfo[num]
        nowNode_in_nodeInfo["nearMineNode"] = set()
        nowNode_in_nodeInfo["nearNeutralNode"] = set()
        nowNode_in_nodeInfo["nearEnemyNode"] = set()
        nowNode_in_nodeInfo["nearMinePower"] = 0
        nowNode_in_nodeInfo["nearEnemyPower"] = 0

        for nodeNum in self.nodes[num].get_next():
            nextNode = self.nodes[nodeNum]
            if nextNode.belong == self.player_id:
                nowNode_in_nodeInfo["nearMineNode"].add(nodeNum)
                nowNode_in_nodeInfo["nearMinePower"] += nextNode.power[self.player_id]
            elif nextNode.belong == -1:
                nowNode_in_nodeInfo["nearNeutralNode"].add(nodeNum)
            else:
                nowNode_in_nodeInfo["nearEnemyNode"].add(nodeNum)
                nowNode_in_nodeInfo["nearEnemyPower"] += nextNode.power[self.enemy_id]

        checkDict = {i: 0 for i in range(1, self.N + 1)}
        if self.nodes[num].belong == self.player_id:
            if num in self.idNodes[self.nodeInfo[num]["ID"]]:
                self.idNodes[self.nodeInfo[num]["ID"]].remove(num)
            if nowNode_in_nodeInfo["nearEnemyNode"]:
                nowNode_in_nodeInfo["ID"] = 2
                self.idNodes[2].add(num)
                nowNode_in_nodeInfo["boarderDistance"] = 0
                checkDict[num] = 3
                for nodeNum in self.nodes[num].get_next():
                    if checkDict[nodeNum] < 3:
                        checkDict[nodeNum] = 2
                        self.nodeInfo[nodeNum]["boarderDistance"] = 1

                for nodeNum in nowNode_in_nodeInfo['secondNearNode']:
                    if checkDict[nodeNum] < 2:
                        checkDict[nodeNum] = 1
                        self.nodeInfo[nodeNum]["boarderDistance"] = 2

            elif nowNode_in_nodeInfo["nearNeutralNode"]:
                self.idNodes[1].add(num)
                nowNode_in_nodeInfo["ID"] = 1

            else:
                self.idNodes[3].add(num)
                nowNode_in_nodeInfo["ID"] = 3

            if checkDict[num] == 0:
                nowNode_in_nodeInfo["boarderDistance"] = 3

        else:
            if num in self.idNodes[self.nodeInfo[num]["ID"]]:
                self.idNodes[self.nodeInfo[num]["ID"]].remove(num)

        nowNode_in_nodeInfo["nearTwoMinePower"] = nowNode_in_nodeInfo["nearMinePower"]
        nowNode_in_nodeInfo["nearTwoEnemyPower"] = nowNode_in_nodeInfo["nearEnemyPower"]

        for nodeNum in nowNode_in_nodeInfo["secondNearNode"]:
            if self.player_id == self.nodes[nodeNum].belong:
                nowNode_in_nodeInfo["nearTwoMinePower"] += self.nodes[nodeNum].power[self.player_id]
            else:
                nowNode_in_nodeInfo["nearTwoEnemyPower"] += self.nodes[nodeNum].power[self.enemy_id]

        if self.player_id == self.nodes[num].belong and self.nodeInfo[num]["ID"] == 2:
            if nowNode_in_nodeInfo["nearTwoMinePower"] - nowNode_in_nodeInfo["nearTwoEnemyPower"] > self.maxMineNode[1]:
                self.maxMineNode = (num, nowNode_in_nodeInfo["nearTwoMinePower"])

    # 重新按立邊界
    def _refresh_Boarder_and_Node(self):
        waitingList = set()
        while self.mine_boarder:
            nodeNum = self.mine_boarder.pop()
            waitingList.add(nodeNum)
            for nodeNum1 in self.nodes[nodeNum].get_next():
                waitingList.add(nodeNum1)

        while self.enemy_boarder:
            nodeNum = self.enemy_boarder.pop()
            waitingList.add(nodeNum)
            for nodeNum1 in self.nodes[nodeNum].get_next():
                waitingList.add(nodeNum1)

        for nodeNum in waitingList:
            self._refreshNode(nodeNum)
            if self.nodes[nodeNum].belong == self.player_id:
                if self.nodeInfo[nodeNum]["nearNeutralNode"] or self.nodeInfo[nodeNum]["nearEnemyNode"]:
                    self.mine_boarder.add(nodeNum)
            elif self.nodes[nodeNum].belong != -1:
                if self.nodeInfo[nodeNum]["nearNeutralNode"] or self.nodeInfo[nodeNum]["nearMineNode"]:
                    self.enemy_boarder.add(nodeNum)

    def _buildNodeDict(self):
        self.nodeInfo = {
            i: {"belongRoad": -1,  # 屬於哪條主道路 0,1,2
                "mainRoadDistance": 99,  # 與道路的距離
                "ID": 1,  # 身份 1為開拓者 2為邊防者 3為傳輸者
                "forwardNode": None,  # 前方的道路節點 ( 方便以後使用 )
                "backwardNode": None,  # 後方的道路節點 ( 方便以後使用 )
                "transferNode": None,  # 用於記錄傳輸者要傳送的Node
                "boarderDistance": 3,  # 與最近邊防者距離3 3代表不在格以內
                "baseDistance": 99,  # 到大本營的距離
                "nearNode": set(self.nodes[i].get_next()),  # 附近的節點
                "nearMinePower": 0,  # 距離為1友軍的power
                "nearTwoMinePower": 0,  # 距離<=2友軍的power
                "nearEnemyPower": 0,  # 距離為1敵軍的power
                "nearTwoEnemyPower": 0,  # 距離<=2敵軍的power
                "secondNearNode": self._allSecondNearNode(i),  # 距離為2的節點集合
                "nearMineNode": set(),  # 附近友方節點表
                "nearEnemyNode": set(),  # 附近敵方節點表
                "nearNeutralNode": None,  # 附近中立節點表
                "nearTwoNode": 0,
                ###important###
                "getPower": 0,  # 得到目前為止被傳送的power數量
                "nowPower": 0  # 扣除給別人的power後剩下的power
                } for i in range(1, self.N + 1)}

        # self.BNodes = [None] + [betterNode(self.nodes[nodeNum], self.player_id, self.N) for nodeNum in
        #                      range(1, self.N + 1)]

        for i in range(1, self.N + 1):
            self.nodeInfo[i]["nearNode"] = set(self.nodes[i].get_next())
            self.nodeInfo[i]["nearNeutralNode"] = deepcopy(self.nodeInfo[i]["nearNode"])
            self.nodeInfo[i]["nearTwoNode"] = len(self.nodeInfo[i]["secondNearNode"]) + len(
                self.nodeInfo[i]["nearNode"])

        for nodeNum in self.nodes[self.mine_base].get_next():
            nowNode_in_nodeInfo = self.nodeInfo[nodeNum]
            nowNode_in_nodeInfo['nearNeutralNode'].remove(self.mine_base)
            nowNode_in_nodeInfo['nearMineNode'].add(self.mine_base)

        for nodeNum in self.nodes[self.enemy_base].get_next():
            nowNode_in_nodeInfo = self.nodeInfo[nodeNum]
            nowNode_in_nodeInfo['nearNeutralNode'].remove(self.enemy_base)
            nowNode_in_nodeInfo['nearMineNode'].add(self.enemy_base)

        # print(self.nodeInfo)

    def find_mainroad(self):
        def findshortest(to_node, from_node, checkDict):
            checkDistance = {i: 99 for i in range(1, self.N + 1)}
            distance = 1
            waitingStack = [from_node]
            checkDistance[from_node] = 0
            while checkDistance[to_node] == 99:
                stack = []
                for _ in range(len(waitingStack)):
                    nodeNum = waitingStack.pop()
                    for nodeNum1 in self.nodes[nodeNum].get_next():
                        if checkDistance[nodeNum1] > distance:
                            checkDistance[nodeNum1] = distance
                            stack.append(nodeNum1)
                distance += 1
                waitingStack.extend(stack)

            distance -= 1
            roadList = [to_node]
            nowNode = to_node
            while distance > 0:
                distance -= 1
                done = False
                buf = set()
                for nodeNum in self.nodes[nowNode].get_next():
                    if checkDistance[nodeNum] == distance:
                        if checkDict[nodeNum] == 1:
                            buf.add(nodeNum)
                        else:
                            roadList.append(nodeNum)
                            nowNode = nodeNum
                            done = True
                            break
                if not done:
                    nowNode = buf.pop()
                    roadList.append(nowNode)

            return roadList

        checkDict = {i: 0 for i in range(1, self.N + 1)}  # 路径1周围的节点
        road1 = findshortest(self.mine_base, self.enemy_base, checkDict)  # 第一条是直连己方大本营和敌方大本营的路
        self.mainRoadNode.append(road1)
        for nodeNum in road1:
            for nodeNum1 in self.nodes[nodeNum].get_next():
                checkDict[nodeNum1] = 1  # 加入距离为一的
            for nodeNum1 in self.nodeInfo[nodeNum]['secondNearNode']:  # 加入距离为2的
                checkDict[nodeNum1] = 1
        neardict = [[] for _ in range(37)]  # 建立‘字典’，key=距离小于2节点的个数，value=满足key的节点组成的列表
        for nodeNum in range(1, self.N + 1):
            if checkDict[nodeNum] == 0:  # 不在路径1周围的节点，放入相应列表中
                neardict[self.nodeInfo[nodeNum]["nearTwoNode"]].append(nodeNum)

        ok_node1 = ok_node2 = 0
        for nearNum in range(36, 10, -1):  # 满足‘周围距离2以内节点最多’的节点
            buf = False
            if neardict[nearNum]:
                for nodeNum in neardict[nearNum]:
                    if checkDict[nodeNum] == 0:
                        ok_node1 = nodeNum  # 若只有1个，选一个
                        buf = True
                        break
            if buf:
                break
                # ok_node2 = neardict[k][-1]  # 若有2个以上，选列表一头一尾的两个（方便表述）
        if ok_node1 == 0:  # 1个节点构建的路径
            return
        else:
            road21 = findshortest(self.mine_base, ok_node1, checkDict)
            road22 = findshortest(ok_node1, self.enemy_base, checkDict)
            road2 = road21[:-1] + road22
            self.mainRoadNode.append(road2)

        for nodeNum in road2:
            for nodeNum1 in self.nodes[nodeNum].get_next():
                checkDict[nodeNum1] = 1  # 加入距离为一的
            for nodeNum1 in self.nodeInfo[nodeNum]['secondNearNode']:  # 加入距离为2的
                checkDict[nodeNum1] = 1

        for nearNum in range(36, 10, -1):  # 满足‘周围距离2以内节点最多’的节点
            buf = False
            if neardict[nearNum]:
                for nodeNum in neardict[nearNum]:
                    if checkDict[nodeNum] == 0:
                        ok_node2 = nodeNum  # 若只有1个，选一个
                        buf = True
                        break
            if buf:
                break
        # 两个节点构建的路径
        if ok_node2 == 0:
            return
        else:
            road31 = findshortest(self.mine_base, ok_node2, checkDict)
            road32 = findshortest(ok_node2, self.enemy_base, checkDict)
            road3 = road31[:-1] + road32
            self.mainRoadNode.append(road3)

    def _refresh_Forward_and_Backward(self):
        for road in self.mainRoadNode[::-1]:
            for i, nodeNum in enumerate(road):
                if i != 0:
                    self.nodeInfo[nodeNum]["backwardNode"] = road[i - 1]
                if i != len(road) - 1:
                    self.nodeInfo[nodeNum]["forwardNode"] = road[i + 1]

    def _allSecondNearNode(self, num: int) -> set:  # num is the original node number
        reSet = set()
        nearNode = self.nodes[num].get_next()

        for nodeNum in nearNode:
            for nodeNum2 in self.nodes[nodeNum].get_next():
                reSet.add(nodeNum2)
        for nodeNum in nearNode:
            if nodeNum in reSet:
                reSet.remove(nodeNum)
        reSet.remove(num)
        return reSet

    def _allLinkRoad(self):  # 對所有節點按定道路 並更新所有transferNode
        waitingList = [[] for _ in range(len(self.mainRoadNode))]
        distance = 1
        transferDict = {i: [] for i in range(1, self.N + 1)}
        for i in range(len(self.mainRoadNode)):
            for nodeNum in self.mainRoadNode[i]:
                if self.nodeInfo[nodeNum]["mainRoadDistance"] > 0:
                    self.nodeInfo[nodeNum]["mainRoadDistance"] = 0
                    self.nodeInfo[nodeNum]['belongRoad'] = i
                    transferDict[nodeNum].append(max(self.nodes[nodeNum].get_next()))
                    waitingList[i].append(nodeNum)

        while any(waitingList):
            for i, stack in enumerate(waitingList):
                newWaiting = []
                while stack:
                    nodeNum = stack.pop()
                    for newNodeNum in self.nodes[nodeNum].get_next():
                        if self.nodeInfo[newNodeNum]['mainRoadDistance'] > distance:
                            self.nodeInfo[newNodeNum]['mainRoadDistance'] = distance
                            self.nodeInfo[newNodeNum]['belongRoad'] = i
                            newWaiting.append(newNodeNum)

                        if self.nodeInfo[newNodeNum]["mainRoadDistance"] == distance:
                            transferDict[newNodeNum].append(nodeNum)

                waitingList[i] = newWaiting
            distance += 1
        self.maxMainRoadDistance = distance - 1

        if self.player_id:
            for nodeNum in transferDict:
                self.nodeInfo[nodeNum]["transferNode"] = min(transferDict[nodeNum])
        else:
            for nodeNum in transferDict:
                self.nodeInfo[nodeNum]["transferNode"] = max(transferDict[nodeNum])
        pass

    def _firstDictRefresh(self):
        self._allLinkRoad()

    def _baseDistanceRefresh(self):
        self.idNodes[1] = {self.mine_base}
        waitingStack = [self.mine_base]
        distance = 1
        self.nodeInfo[self.mine_base]["baseDistance"] = 0

        while waitingStack:
            stack = []
            for i in range(len(waitingStack)):
                nodeNum = waitingStack.pop()
                for nodeNum2 in self.nodes[nodeNum].get_next():
                    if self.nodeInfo[nodeNum2]["baseDistance"] > distance:
                        stack.append(nodeNum2)
                        self.nodeInfo[nodeNum2]["baseDistance"] = distance
            waitingStack.extend(stack)
            distance += 1
        self.maxTransferDistance = distance - 1

    def searchNodeGen(self):  # 用於給出己方出兵順序的生成器
        if self.time > 20 and self.attackState == 0:
            # self.attack = False
            self.attack = choices([True, False],
                                  [self.maxMineNode[1], self.nodeInfo[self.maxMineNode[0]]["nearTwoEnemyPower"]])[0]
            if self.attack:
                self.attackState = self.baseattackState
                self.attack = False
        listTransfer = [[] for _ in range(self.maxMainRoadDistance + 1)]
        listImportantID = [[], []]
        listTransBoarder = [[] for _ in range(2)]
        waitingList = [self.mine_base]
        checkDict = {i: 0 for i in range(1, self.N + 1)}
        checkDict[self.mine_base] = 1
        while waitingList:
            stack = []
            for _ in range(len(waitingList)):
                nodeNum = waitingList.pop()
                if self.nodes[nodeNum].belong == self.player_id:
                    nodeId = self.nodeInfo[nodeNum]["ID"]
                    if nodeId == 3:
                        if self.nodeInfo[nodeNum]["boarderDistance"] == 2:
                            listTransBoarder[1].append(nodeNum)
                        elif self.nodeInfo[nodeNum]["boarderDistance"] == 1:
                            listTransBoarder[0].append(nodeNum)
                        else:
                            listTransfer[self.nodeInfo[nodeNum]["mainRoadDistance"]].append(nodeNum)
                    elif nodeId == 1:  # 1為開拓者
                        listImportantID[0].append(nodeNum)
                    elif nodeId == 2:  # 2為邊防者
                        listImportantID[1].append(nodeNum)

                for nodeNum2 in self.nodes[nodeNum].get_next():
                    if checkDict[nodeNum2] == 0:
                        checkDict[nodeNum2] = 1
                        stack.append(nodeNum2)
            waitingList = stack

        for searchList in listTransfer[:0:-1]:
            for nodeNum in searchList[::-1]:
                yield nodeNum

        for nodeNum in listTransfer[0]:
            yield nodeNum

        if self.attackState < self.baseattackState - 1:
            for nodeNum in listTransBoarder[1]:
                yield nodeNum

            for nodeNum in listTransBoarder[0]:
                yield nodeNum

            for searchList in listImportantID:
                for nodeNum in searchList:
                    yield nodeNum

        else:
            if self.attackState == self.baseattackState:
                self.attackList = listImportantID[1] + listTransBoarder[0] + listTransBoarder[1]
                for nodeNum in listImportantID[0]:
                    yield nodeNum

            elif self.attackState == self.baseattackState - 1:
                self.attackList = [self.maxMineNode[0]] + [self.nodes[self.maxMineNode[
                    0]].get_next()]  # + self.nodeInfo[self.maxMineNode[0]]["secondNearNode"]
                for nodeNum in listTransBoarder[1]:
                    yield nodeNum
                for nodeNum in listTransBoarder[0]:
                    if nodeNum not in self.attackList:
                        yield nodeNum
                for nodeNum in listImportantID[1]:
                    if nodeNum not in self.attackList:
                        yield nodeNum

    def attackSt1(self):
        numMax = self.maxMineNode[0]
        self.attactingNode = numMax
        action = []
        self.attackList.remove(numMax)
        for nearTwo in self.nodeInfo[numMax]["secondNearNode"]:
            if self.nodes[nearTwo].belong == self.player_id:
                nextnumMax = self.nodes[numMax].get_next()
                for nodeNum2 in self.nodeInfo[nearTwo]["nearMineNode"]:
                    if nearTwo in self.attackList and nodeNum2 in nextnumMax:
                        give = self.nodeInfo[nearTwo]["nowPower"]
                        self.nodeInfo[nearTwo]["nowPower"] -= give
                        self.nodeInfo[nodeNum2]["getPower"] += give - give ** 0.5
                        self.attackList.remove(nearTwo)
                        action.append((nearTwo, nodeNum2, give - 0.1))

        for nodeNum in self.attackList[::-1]:
            action.extend(self.doNode(nodeNum))

        return action

    def attackSt2(self):
        numMax = self.attactingNode
        action = []
        for nodeNum in self.nodeInfo[numMax]["nearMineNode"]:
            if self.nodes[nodeNum].belong == self.player_id:
                give = self.nodeInfo[nodeNum]["nowPower"]
                if give > 0:
                    self.nodeInfo[nodeNum]["nowPower"] -= give
                    self.nodeInfo[nodeNum]["getPower"] += give - give ** 0.5
                    action.append((nodeNum, numMax, give-0.1))
        return action

    def isValid(self, action):
        a, b, c = action
        if self.nodes[a].belong != self.player_id:
            return False
        if b not in self.nodes[a].get_next():
            return False
        if self.tmp_left[a] <= c + 0.01:
            return False
        self.tmp_left[a] -= c
        return True

    def asBest(self, fromNode, toNode):
        recPower = self.nodeInfo[fromNode]["getPower"]
        nowPower = self.nodeInfo[fromNode]["nowPower"]
        toNowPower = self.nodes[toNode].power[self.player_id]
        totalPower = recPower + nowPower + toNowPower
        bestPower = 12 * (totalPower + 3) / 23 - toNowPower / 2
        if nowPower + recPower < 34:
            return []
        if nowPower < 15:
            return []
        if totalPower > 100:
            return self.asMuch(fromNode, toNode)
        if nowPower > bestPower:
            give = bestPower
            self.nodeInfo[fromNode]["nowPower"] -= give
            self.nodeInfo[toNode]["getPower"] += give - give ** 0.5
            return [(fromNode, toNode, give - 0.1)]
        else:
            give = nowPower
            self.nodeInfo[fromNode]["nowPower"] -= give
            self.nodeInfo[toNode]["getPower"] += give - give ** 0.5
            return [(fromNode, toNode, give - 0.1)]

    def asMuch(self, fromNode, toNode):
        totalPower = self.nodeInfo[fromNode]["nowPower"] + self.nodeInfo[fromNode]["getPower"]
        nowPower = self.nodeInfo[fromNode]["nowPower"]
        if nowPower < 15:
            return []
        if self.nodeInfo[fromNode]["getPower"] >= 50:
            give = self.nodeInfo[fromNode]["nowPower"]
            self.nodeInfo[fromNode]["nowPower"] -= give
            self.nodeInfo[toNode]["getPower"] += give - give ** 0.5
            return [(fromNode, toNode, give - 0.1)]
        elif totalPower > 50:
            give = totalPower - 50
            if give > 5:
                self.nodeInfo[fromNode]["nowPower"] -= give
                self.nodeInfo[toNode]["getPower"] += give - give ** 0.5
                return [(fromNode, toNode, give - 0.1)]
        return []

    def debugPrintDict(self, num):
        print(self.nodes[num])
        for i in self.nodeInfo[num]:
            print(i, ":", self.nodeInfo[num][i])
        print(self.refreshTimer)

    def debugPrintSelf(self, variable=None):
        print("hello")
        try:
            pass
        except:
            pass


if __name__ == "__main__":
    generate=Generate_Hexagon(4, 0.20, 0.20)
    selfmap=GameMap(generate)
    # selfmap = GameMap(g_design4)
    a = player_class(0)
    print("123")
    a.player_func(selfmap)
    c = list(a.searchNodeGen())
    a.player_func(selfmap)
    print("hello")
    print(a.clarify(selfmap))
    pass
