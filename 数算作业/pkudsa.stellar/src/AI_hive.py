from GameMap import GameMap
import math
import DesignGenerator
from HexagonForce import Generate_Hexagon
from copy import deepcopy
from collections import defaultdict

class player_class:
    '''初始化，此类包含一个属性即玩家编号'''
    def __init__(self,player_id):
        self.player_id=player_id

    def cal_dis(self,map_info,node1,node2):
        '''定义相邻两点间距离的函数'''
        dis1=math.sqrt(map_info.nodes[node1].power[self.player_id])
        dis2=map_info.nodes[node2].power[1-self.player_id]
        dis=dis1+dis2
        return dis

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

    def generate_steps_to_alist(self,map_info,alist):
        '''到某集合步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到某个给定集合的最近步数,不加权'''
        pos={}
        for node in alist:
            pos[node]=0
        if map_info.N+1 in alist:
            alist.remove(map_info.N+1)
        line=deepcopy(alist)
        #初始化已扫描集合
        visited=set(line)
        #当未扫描列表非空时，不断从队首取元素，扫描它的邻接元。每次更新最短距离
        while line:
            cur=line.pop(0)
            for neighbor in map_info.nodes[cur].get_next():
                if neighbor not in pos:
                    pos[neighbor]=pos[cur]+1
                else:
                    pos[neighbor]=min(pos[cur]+1,pos[neighbor])
                pos[neighbor]=min(pos[cur]+1,pos[neighbor])
                #将未扫描过的节点添加到扫描列表中
                if neighbor not in visited:
                    line.append(neighbor)
                #扫描完的节点加入已扫描集合
            visited.add(cur)
        return pos
    
    def generate_steps_to_me(self,map_info,my_nodes):
        '''到我方据点步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到我方据点的最近步数,不加权'''
        return self.generate_steps_to_alist(map_info,my_nodes)

    def generate_steps_to_enemy(self,map_info,enemy_nodes):
        '''到敌方据点步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最近步数,不加权'''
        return self.generate_steps_to_alist(map_info,enemy_nodes)

    def generate_steps_to_mybase(self,map_info):
        '''到我方大本营步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最近步数,不加权'''
        if self.player_id==0:
            my_base=1
        else:
            my_base=map_info.N
        return self.generate_steps_to_alist(self,map_info,[my_base])

    def generate_steps_to_enemybase(self,map_info):
        '''到敌方大本营步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最近步数,不加权'''
        if self.player_id==0:
            enemy_base=map_info.N
        else:
            enemy_base=1
        return self.generate_steps_to_alist(self,map_info,[enemy_base])
        
    def generate_dist_to_alist(self,map_info,alist):
        '''到某集合距离生成函数，返回值为一个字典，key值为据点编号，value值为该据点到某个给定集合的最近距离,加权'''
        pos={}
        for node in alist:
            pos[node]=0
        if map_info.N+1 in alist:
            alist.remove(map_info.N+1)
        line=deepcopy(alist)
        #初始化已扫描集合
        visited=set(line)
        #print(map_info.nodes[alist[0]].power)
        #print(pos)
        #print(line)
        #print(visited)
        #当未扫描列表非空时，不断从队首取元素，扫描它的邻接元。每次更新最短距离
        while line:
            cur=line.pop(0)
            #print(map_info.nodes[cur].get_next())
            for neighbor in map_info.nodes[cur].get_next():
                if neighbor not in pos:
                    pos[neighbor]=pos[cur]+self.cal_dis(map_info,neighbor,cur)
                else:
                    pos[neighbor]=min(pos[cur]+self.cal_dis(map_info,cur,neighbor),pos[neighbor])
                #将未扫描过的节点添加到扫描列表中
                if neighbor not in visited:
                    line.append(neighbor)
                #扫描完的节点加入已扫描集合
            visited.add(cur)
        return pos
    
    def generate_dist_to_me(self,map_info,my_nodes):
        '''到我方据点步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到我方据点的最近步数,不加权'''
        return self.generate_dist_to_alist(map_info,my_nodes)

    def generate_dist_to_enemy(self,map_info,enemy_nodes):
        '''到敌方据点步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最近步数,不加权'''
        return self.generate_dist_to_alist(map_info,enemy_nodes)

    def generate_dist_to_mybase(self,map_info):
        '''到我方大本营步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最近步数,不加权'''
        if self.player_id==0:
            my_base=1
        else:
            my_base=map_info.N
        return self.generate_dist_to_alist(self,map_info,[my_base])

    def generate_dist_to_enemybase(self,map_info):
        '''到敌方大本营步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最近步数,不加权'''
        if self.player_id==0:
            enemy_base=map_info.N
        else:
            enemy_base=1
        return self.generate_dist_to_alist(map_info,[enemy_base])

#  ---分割线---
# 以下是我根据Notion文档里面描述的逻辑新增的，当然有一部分的实现没法做到太精确
    def generate_vicinity_node(self,map_info,node,dis):
        '''生成与节点相邻的节点列表，返回一个列表'''
        nodes = [node]
        vicinity_node = []
        if self.generate_steps_to_me(map_info,nodes)[node] == int(dis):
            vicinity_node.append(node)
        return vicinity_node

    def generate_vicinity_troop_num(self,map_info,dis):
        '''生成以dis为半径的圆周内的兵力，返回由两个列表组成的元组 (power_ally::list,power_enemy::list)'''
        power_ally = 0
        power_enemy = 0
        for node in map_info.nodes:
            for adjacent_node in self.generate_vicinity_node(map_info,node,dis):
                '''以dis回合为半径计算周围兵力数量'''
                if adjacent_node.belong == self.player_id:
                    power_ally += adjacent_node.power[self.player_id]
                elif adjacent_node.belong == 1-self.player_id:
                    power_enemy += adjacent_node.power[1-self.player_id]
        return power_ally, power_enemy

    def generate_frontline_node(self,map_info):
        '''透过1为半径的圆周内有没有对方势力，若有则是前线，若无则不是前线，返回由两个列表组成的元组 (frontline_ally::list, frontline_enemy::list)'''
        frontline_ally, frontline_enemy = [], []
        for node in map_info.nodes:
            if node.belong == self.player_id:
                for near in self.generate_vicinity_node(self,map_info,node,1):
                    if near.belong != self.player_id:
                        frontline_ally.append(near)
            else:
                for near in self.generate_vicinity_node(self,map_info,node,1):
                    if near.belong == self.player_id:
                        frontline_enemy.append(near)
        return frontline_ally,frontline_enemy

    def generate_pressure_index(self,map_info):
        '''生成地图上所有节点的压力指数，返回值为一个字典，key:value = 节点:压力指数'''
        k,l = 5,5 
        '''有关此二可调试参数的定义请参考策略说明'''
        pressure_dict = {}
        for node in map_info.nodes:
            if node.belong == self.player_id:
                '''生成每个节点到前线节点的距离，取最小值'''
                dis = min(self.generate_dist_to_alist(map_info,self.generate_frontline_node(map_info)[self.player_id]).values())
                num_dif = self.generate_vicinity_troop_num(map_info,node)[1] - self.generate_vicinity_troop_num(map_info,node)[0] 
                pressure = - k * dis + l * num_dif
                pressure_dict[node] = pressure

            elif node.belong == 1-self.player_id:
                '''生成每个节点到前线节点的距离，取最小值'''
                dis = min(self.generate_dist_to_alist(map_info,self.generate_frontline_node(map_info)[1-self.player_id]).values()) 
                num_dif = self.generate_vicinity_troop_num(map_info,node)[0] - self.generate_vicinity_troop_num(map_info,node)[1] 
                pressure = - k * dis + l * num_dif
                pressure_dict[node] = pressure
            
            else:
                pressure_dict[node] == 0
        return pressure_dict

    def generate_shortest_path(self,map_info,fromNode,toNode):
        '''生成最短路径，指导safe_nodes用，返回最短路径的列表'''
        graph = defaultdict(list)
        for node in map_info.nodes():
            graph[node] = node.getnext()
        
        explored = []
        queue = [[fromNode]]

        if fromNode == toNode:
            return
        
        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                neighbours = graph[node]

                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if neighbour == toNode:
                        return new_path
        # print('a connecting path does not exist')
        return 
              




    def player_func(self,map_info):
        action = []
        '''有空插空，没空再计算压力指数，如此才方便计算压力指数与前线节点'''
        my_nodes =  self.clarify(map_info)[0]
        enemy_nodes = self.clarify(map_info)[1] 

        pressure_dict = self.generate_pressure_index(map_info)
        '''设定压力指数最大的前10个在前线的节点为需要帮助的节点'''
        critical_pressure = pressure_dict.values().sorted(-10)
        frontline_node = self.generate_frontline_node(map_info)[0]

        for node in my_nodes:
            '''先判断有无空节点，若有，则将兵力平均分配至相邻的空节点'''
            empty_nodes_tobeoccupied = []            
            for next in node.nextinfo():
                if next.belong == -1:
                    empty_nodes_tobeoccupied.append(next)
            
            '''占领计划 之 兵力分配'''
            if node.power[self.player_id] > 50:
                num_troops = (node.power[self.player_id]-50) / len(empty_nodes_tobeoccupied)
            else:
                num_troops = (node.power[self.player_id]-1) / len(empty_nodes_tobeoccupied)
            '''增至action列表'''
            for empty_node in empty_nodes_tobeoccupied:
              action.append(node,empty_node,num_troops)

        '''前线的节点；需要帮助的节点'''
        node_need_help = []
        for nodef in frontline_node:
            if pressure_dict[nodef] > critical_pressure:
                node_need_help.append(nodef)
            
            '''攻击最近的压力指数最高的敌人节点'''
            near_enemy_lst = [x for x in nodef.getinfo() if x.belong == 1-self.player_id]
            target = near_enemy_lst[0]
            for i in near_enemy_lst:
                if pressure_dict[i] > pressure_dict[target]:
                    target = near_enemy_lst[i]
            
            '''兵力分配'''
            if nodef.power[self.player_id] > 50:
                num_troops = (nodef.power[self.player_id]-50) / len(empty_nodes_tobeoccupied)
            else:
                num_troops = (nodef.power[self.player_id]-1) / len(empty_nodes_tobeoccupied)
            
            action.append(nodef,target,num_troops)


        '''安全节点；帮助距离自己最近的N_nh'''
        safe_nodes = [x for x in my_nodes if pressure_dict[x] < critical_pressure]
        for safe_node in safe_nodes:
            if safe_node.power[self.player_id] > 50:
                num_troops = (safe_node.power[self.player_id]-50) / len(empty_nodes_tobeoccupied)
            else:
                num_troops = (safe_node.power[self.player_id]-1) / len(empty_nodes_tobeoccupied) 

            dis_dict = self.generate_steps_to_alist(map_info,node_need_help)
            help_target = min(dis_dict.keys(), key=(lambda k: dis_dict[k]))
            toNode = self.generate_shortest_path(map_info,safe_node,help_target)[0]
            action.append(safe_node,toNode,num_troops)
                    
        return action            

#以下为调试部分：
if __name__ == '__main__':
    player=player_class(0)
    generate=Generate_Hexagon(4, 0.20, 0.20)
    map_info=GameMap(generate)
    print(player.clarify(map_info))
    print(player.generate_dist_to_enemybase(map_info))
    