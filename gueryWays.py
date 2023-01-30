import json
import os
import pandas as pd
import math
from neo4j import GraphDatabase

client = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Redkowice1"))
Scieszka="/var/www/html/OSRM.jos"


def filter_ways(x,y,level):
    minway=-1
    X=-1
    Y=-1
    with client.session() as session:
        ways=session.read_transaction(query_ways)
        for way in ways:
            if(way.data("ways")["ways"]["level"]==level):
                leng= leng_way_points([way.data("ways")["ways"]["X"],way.data("ways")["ways"]["Y"]],[x,y])
                if(leng < minway or minway==-1):
                    X=way.data("ways")["ways"]["X"]
                    Y=way.data("ways")["ways"]["Y"]
                    minway=leng
                    print(minway,X,Y)
    return [X,Y]

def query_ways(tx):
    query="MATCH (ways) Return ways"
    return list(tx.run(query))

def leng_way_points(point1,point2):
    return math.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point1[1],2))


def guery_way(tx,args):

    query="MATCH (source:ways{ level:$level,X:$x,Y:$y}),(target:ways{level:$level_end,X:$x_end,Y:$y_end}),p = shortestPath((source)-[*]-(target)) Return p"
    result=tx.run(query,level=args[0],x=args[1][0],y=args[1][1],level_end=args[2],x_end=args[3][0],y_end=args[3][1])
    return list(result)

def search_way(startpoint,endpoint,startlevel,endlevel):
    with client.session() as session:
        way=session.read_transaction(guery_way,[startlevel,startpoint,endlevel,endpoint])
        for path in way:
            print(path.data("p"))



#test działadnia
start_point=filter_ways(18.602784544967676,53.017013352,"0")
end_point=filter_ways(18.60239408804935,53.01733814244693,"0")

print(start_point)
print(end_point)
search_way(start_point,end_point,"0","0")

client.close()