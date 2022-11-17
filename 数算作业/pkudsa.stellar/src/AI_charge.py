from GameMap import GameMap
import math
import DesignGenerator
from HexagonForce import Generate_Hexagon

class player_class:
    def __init__(self,player_id:int):
        self.player_id=player_id

    #计算“距离”指标：衡量路上的损耗以及因战斗损失的人员
    def cal_dis(self,map_info,node1,node2):
        dis1=math.sqrt(map_info.nodes[node1].power[self.player_id])
        dis2=map_info.nodes[node2].power[1-self.player_id]
        return dis1+dis2

    #寻找dis列表中离start最近的节点
    def find_short_node(self,dis,neighbor,visited):
        short_dis=999
        short_dis_node=None
        for node in dis:
            distance=dis[node]
            if distance<short_dis and node not in visited:
                short_dis=distance
                short_dis_node=node
        return short_dis_node

    #狄克斯特拉算法，计算每个节点离对方大本营最近的路线
    def dijkstra(self,map_info,neighbor,start,end):
        if start==end:
            return end
        dis={}
        parent={}
        for node in neighbor:
            dis[node]=999
        for node in neighbor[start]:
            dis[node]=self.cal_dis(map_info,start,node)
            parent[node]=start
        visited=set()
        visited.add(start)
        node=self.find_short_node(dis,neighbor,visited)
        while node != end:
            distance=dis[node]
            neighbor_list=neighbor[node]
            for item in neighbor_list:
                new_dis=distance+self.cal_dis(map_info,node,item)
                if new_dis<dis[item]:
                    dis[item]=new_dis
                    parent[item]=node
            visited.add(node)
            node=self.find_short_node(dis,neighbor,visited)
        tracker=end
        while parent[tracker]!=start:
            tracker=parent[tracker]
        return tracker

    #策略：沿着最近的路向对方大本营蛮力冲锋，可调参数为每次出兵比
    def player_func(self,map_info:GameMap):
        if self.player_id==0:
            endnode=map_info.N
        else:
            endnode=1
        actions=[]
        my_node=[] 
        neighbor={}
        for node in map_info.nodes:
            new_neighbor=[]
            for next in node.get_next():
                new_neighbor.append(next)
            neighbor[node.number]=new_neighbor
            if node.belong==self.player_id:
                my_node.append(node)
        for node in my_node:
            chosen=self.dijkstra(map_info,neighbor,node.number,endnode)
            actions.append((node.number,chosen,node.power[self.player_id]*0.5))
        return actions

if __name__ == '__main__':
    player=player_class(0)
    generate=Generate_Hexagon(4, 0.20, 0.20)
    map_info=GameMap(generate)
    print(player.player_func(map_info))