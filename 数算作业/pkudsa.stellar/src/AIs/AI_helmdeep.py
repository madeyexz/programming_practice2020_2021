from GameMap import GameMap
#import math
#import DesignGenerator
#from HexagonForce import Generate_Hexagon
from copy import deepcopy

class player_class:
    '''初始化，此类包含一个属性即玩家编号'''
    def __init__(self,player_id):
        self.player_id=player_id

    def cal_dis(self,map_info,node1,node2):
        '''定义相邻两点间距离的函数'''
        dis=map_info.nodes[node2].power[1-self.player_id]
        return dis   

    def clarify(self,map_info):
        '''分类函数，返回值为一个三元元组，格式为(我方所有据点列表，对方所有据点列表，空据点列表)'''
        #初始化返回值，分别为我方据点，对方据点，空据点
        my_nodes=[]
        enemy_nodes=[]
        #顺序扫描所有节点，按照其belong值归类到不同的列表(我方，对方，空)
        for node in map_info.nodes:
            if node.belong==self.player_id:
                my_nodes.append(node.number)
            elif node.belong==1-self.player_id:
                enemy_nodes.append(node.number)
        #print(my_nodes,enemy_nodes)
        return my_nodes,enemy_nodes

    def generate_steps_to_enemy(self,map_info,enemy_nodes):
        '''到某集合步数生成函数，返回值为一个字典，key值为据点编号，value值为该据点到某个给定集合的最近步数,不加权'''
        pos={}
        #print(enemy_nodes)
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
                if neighbor not in visited:
                    line.append(neighbor)
                #扫描完的节点加入已扫描集合
            visited.add(cur)
        return pos

    def generate_need_help(self,map_info,steps_to_enemy):
        help={}
        for anode in map_info.nodes:
            if anode.number!=0 and anode.number!=map_info.N+1:
                node=anode.number
                if steps_to_enemy[node]<=2 and map_info.nodes[node].power[self.player_id]<=50:
                    help[node]=200-map_info.nodes[node].power[self.player_id]
                else:
                    help[node]=80-map_info.nodes[node].power[self.player_id]
        return help

    def generate_dist_to_enemybase(self,map_info):
        '''到某集合距离生成函数，返回值为一个字典，key值为据点编号，value值为该据点到某个给定集合的最近距离,加权'''
        pos={}
        if self.player_id==0:
            enemy_base=map_info.N
        else:
            enemy_base=1
        line=[enemy_base]
        #初始化已扫描集合
        visited=set(enemy_base)
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
    
    def player_func(self,map_info):
        my_nodes,enemy_nodes=self.clarify(map_info)
        steps_to_enemy=self.generate_steps_to_enemy(map_info,enemy_nodes)
        action=[]
        danger_dist=999
        for node in my_nodes:
            if steps_to_enemy[node]<=danger_dist:
                danger_dist=steps_to_enemy[node]
        #print(danger_dist)
        if danger_dist>=1:
            #print('expand!')
            for node in my_nodes:
                if map_info.nodes[node].power[self.player_id]>=25:
                    to_list=[]
                    my_power=map_info.nodes[node].power[self.player_id]
                    boundary=False
                    for neighbor in map_info.nodes[node].get_next():
                        if map_info.nodes[neighbor].belong==-1:
                            boundary=True
                            to_list.append(neighbor)
                    if boundary:
                        if my_power<=50:
                            send=my_power*0.5/len(to_list)
                        else:
                            send=min(my_power-15,my_power*0.8)/len(to_list)
                        action+=[(node,item,send) for item in to_list]
                    elif map_info.nodes[node].power[self.player_id]>=30:
                        #print(node,'spread!')
                        new_to_list=[]
                        for neighbor in map_info.nodes[node].get_next():
                            judge1,judge2=False,False
                            if map_info.nodes[neighbor].power[self.player_id]<map_info.nodes[node].power[self.player_id]:
                                judge1=True
                            if steps_to_enemy[neighbor]<steps_to_enemy[node]:
                                judge2=True
                            if judge1 and judge2:    
                                new_to_list.append(neighbor)
                        #print(new_to_list)
                        new=[(node,neighbor,map_info.nodes[node].power[self.player_id]*0.8/len(new_to_list)) for neighbor in new_to_list]
                        #print(new)
                        action+=new
        else:
            #print('defend!')
            help=self.generate_need_help(map_info,steps_to_enemy)
            #print('help:',help)
            for node in my_nodes:
                my_power=map_info.nodes[node].power[self.player_id]
                if steps_to_enemy[node]<=1:
                    if my_power>=50:
                        weak=None
                        weak_power=999
                        s=0
                        for neighbor in map_info.nodes[node].get_next():
                            s+=1
                            if map_info.nodes[neighbor].power[1-self.player_id]<weak_power:
                                weak_power=map_info.nodes[neighbor].power[1-self.player_id]
                                weak=neighbor
                        send=max(0,my_power-75,my_power-weak_power)/s
                        if send>0:
                            action.append(node,weak,send)
                elif steps_to_enemy[node]<=4:
                    neighbors=[item for item in map_info.nodes[node].get_next()]
                    #print('neighbors:',neighbors)
                    total_help=0
                    my_power=map_info.nodes[node].power[self.player_id]
                    new_action=[]
                    for neighbor in neighbors:  
                        total_help+=help[neighbor]
                    #print('total_help:',total_help)
                    total_send=max(my_power*0.7,my_power-50)
                    #print('total_send:',total_send)
                    for neighbor in neighbors:
                        rate=help[neighbor]/total_help
                        #print('rate:',rate)
                        send=max(0,total_send*rate)
                        #print('send:',send)
                        if send>0:
                            new_action.append((node,neighbor,send))
                        #print('new_action:',new_action)
                        action+=new_action
                else:
                    short=None
                    short_dist=999
                    dist_to_enemybase=self.generate_dist_to_enemybase(map_info)
                    neighbor_list=[item for item in map_info.nodes[node].get_next()]
                    for neighbor in neighbor_list:
                        if dist_to_enemybase[neighbor]<short_dist:
                            short=neighbor
                            short_dist=dist_to_enemybase[neighbor]
                    if map_info.nodes[short].power[1-self.player_id]!=0:
                        send=min(map_info.nodes[short].power[1-self.player_id]+20,map_info.nodes[node].power[self.player_id]*0.8)
                    else:
                        send=min(50,map_info.nodes[node].power[self.player_id]*0.8)
                    action+=[(node,short,send)]
        return action

#以下为调试部分：
#if __name__ == '__main__':
#    player=player_class(0)
#    generate=Generate_Hexagon(4, 0.20, 0.20)
#    map_info=GameMap(generate)
#    for node in map_info.nodes[1].get_next():
#        map_info.nodes[node].set_power((25,0),True)
#        for neighbor in map_info.nodes[node].get_next():
#            map_info.nodes[neighbor].set_power((25,0),True)
#    map_info.nodes[11].set_power((0,25),True)
#    map_info.nodes[12].set_power((0,25),True)
#    map_info.nodes[13].set_power((0,25),True)
#    map_info.nodes[14].set_power((0,25),True)
#    map_info.nodes[map_info.N].set_power((0,25),True)
#    my_nodes,enemy_nodes=player.clarify(map_info)[0],player.clarify(map_info)[1]
#    print(my_nodes)
#    for node in my_nodes:
#        print(node,map_info.nodes[node].power[0])
#    print(player.generate_steps_to_enemy(map_info,enemy_nodes))
#    print(player.player_func(map_info))