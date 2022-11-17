from GameMap import GameMap
from copy import deepcopy

class player_class:
    def __init__(self,player_id):
        self.player_id=player_id
        self.enemy_id=1-player_id
        self.turn=0

    def clarify(self,map_info:GameMap):
        '''分类函数，返回值为一个三元元组，格式为(我方所有据点列表，对方所有据点列表，空据点列表)'''
        my_nodes,enemy_nodes,empty_nodes=[],[],[]
        for node in map_info.nodes:
            if node.belong==self.player_id:
                my_nodes.append(node.number)
            elif node.belong==self.enemy_id:
                enemy_nodes.append(node.number)
            elif node.number!=0:
                empty_nodes.append(node.number)
        return my_nodes,enemy_nodes,empty_nodes

    def generate_power(self,map_info:GameMap,player_id):
        '''返回一个字典，key为节点编号，value为该节点中id为player_id的玩家占据的兵力值'''
        power={}
        for node in map_info.nodes:
            power[node.number]=map_info.nodes[node.number].power[player_id]
        return power

    def generate_boundary(self,map_info:GameMap,my_nodes): 
        '''返回一个字典，key为节点编号，value为该节点的邻接节点中非我方占据的节点编号（列表）'''
        boundary={}
        for node in my_nodes:
            ans=[]
            for neighbor in map_info.nodes[node].get_next():
                if map_info.nodes[neighbor].belong!=self.player_id:
                    ans.append(neighbor)
            boundary[node]=ans
        return boundary

    def generate_steps_to_enemy(self,map_info,enemy_nodes):
        '''到敌方据点步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最少步数'''
        pos={}
        for node in enemy_nodes:
            pos[node]=0
        line=deepcopy(enemy_nodes)
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
                #将未扫描过的节点添加到扫描列表中
                if neighbor not in visited and neighbor not in line:
                    line.append(neighbor)
                #扫描完的节点加入已扫描集合
            visited.add(cur)
        return pos

    def generate_steps_to_enemybase(self, map_info):
        '''到敌方大本营步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到敌方据点的最少步数'''
        if self.player_id == 0:
            enemy_base = map_info.N
        else:
            enemy_base = 1
        return self.generate_steps_to_enemy(map_info, [enemy_base])

    def generate_nearer(self,map_info,node,steps:dict):
        '''返回一个列表，为编号node(int类)的节点的邻接节点中，比node这个点更靠近敌方的点的编号'''
        ans=[]
        for neighbor in map_info.nodes[node].get_next():
            if steps[neighbor]<steps[node]:
                ans.append(neighbor)
        return ans

    def generate_need_aid(self,map_info:GameMap,my_nodes):
        '''返回一个列表，为我方节点中需要支援的节点编号'''
        need_aid=[]
        for node in my_nodes:
            degree=0
            for neighbor in map_info.nodes[node].get_next():
                degree+=map_info.nodes[neighbor].power[self.enemy_id]-map_info.nodes[neighbor].power[self.player_id]
            if degree>20:
                need_aid.append(node)
        return need_aid    

    def player_func(self,map_info:GameMap):
        self.turn+=1
        my_nodes,enemy_nodes,empty_nodes=self.clarify(map_info)
        need_aid = self.generate_need_aid(map_info,my_nodes) 
        my_power=self.generate_power(map_info,self.player_id)
        enemy_power=self.generate_power(map_info,1-self.player_id)
        boundary=self.generate_boundary(map_info,my_nodes)
        steps_to_enemybase = self.generate_steps_to_enemybase(map_info)
        steps_to_enemy = self.generate_steps_to_enemy(map_info, enemy_nodes)
        steps_to_aid = self.generate_steps_to_enemy(map_info, need_aid)
        my_nodes.sort(key=lambda x:-steps_to_enemy[x])
        action=[]
        turn=self.turn
        limit_list=[0,10,10,10,10,18,18,18,25,25,25]
        if turn<=10:
            limit=limit_list[turn]
        else:
            limit=50
        
        for node in my_nodes:
            if len(boundary[node])==0:
                if my_power[node]>limit:
                    total_send = min(map_info.nodes[node].power[self.player_id]-1,my_power[node]-limit)
                    toEnemy = self.generate_nearer(map_info,node,steps_to_enemy)
                    if len(steps_to_aid)!=0:
                       toAid = self.generate_nearer(map_info, node, steps_to_aid)
                    else:
                        toAid=[]
                    
                    power_allocate = {}
                    if turn<=10:
                        for neighbor in map_info.nodes[node].get_next():
                            power_allocate[neighbor] = 0
                            if neighbor in toEnemy:
                                power_allocate[neighbor] += 3
                            # if map_info.nodes[neighbor].belong==-1:     
                            #     power_allocate[neighbor] += 2
                    else:
                        for neighbor in map_info.nodes[node].get_next():
                            power_allocate[neighbor] = 0
                            if neighbor in toEnemy:
                                power_allocate[neighbor] += 3
                            if neighbor in toAid:      
                                power_allocate[neighbor] += 5
                            if map_info.nodes[neighbor].belong==-1:     
                                power_allocate[neighbor] += 2
                    total_weight = 0
                    for allocation in power_allocate.values():
                        total_weight += allocation
                    
                    for neighbor in map_info.nodes[node].get_next():
                        if power_allocate[neighbor] != 0:
                            send = total_send * power_allocate[neighbor] / total_weight  # 加权平均
                            gain=send-send**0.5
                            action.append((node, neighbor, send))
                            my_power[neighbor]+=gain
                    my_power[node]-=total_send
            else:
                if node in need_aid:
                    neighbors=map_info.nodes[node].get_next()
                    if my_power[node]>limit:
                        total_send=min(map_info.nodes[node].power[self.player_id]-1,my_power[node]-limit)
                        to_nodes=[]
                        for neighbor in neighbors:
                            if steps_to_enemy[neighbor]<steps_to_enemy[node] or map_info.nodes[neighbor].belong==-1:
                                to_nodes.append(neighbor)
                        size=len(to_nodes)
                        send=total_send/size
                        gain=send-send**0.5
                        for dest in to_nodes:
                            action.append((node,dest,send))
                            my_power[dest]+=gain
                        my_power[node]-=total_send
                else:
                    if my_power[node]>limit:
                        to_nodes=[]
                        for x in boundary[node]:
                            if enemy_power[x]<my_power[node]-1:
                                to_nodes.append(x)
                        if to_nodes==[]:
                            to_nodes=self.generate_nearer(map_info,node,steps_to_enemybase)
                        size=len(to_nodes)
                        total_send=min(map_info.nodes[node].power[self.player_id]-1,my_power[node]-limit)
                        send=total_send/size
                        gain=send-send**0.5
                        for dest in to_nodes:
                            action.append((node,dest,send))
                            my_power[dest]+=gain
                        my_power[node]-=total_send

        return action