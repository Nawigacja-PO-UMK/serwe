import json
import os
import math
import sys
from neo4j import GraphDatabase, basic_auth

client = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Redkowice1"))
Scieszka="/home/mateusz/source/serwe/OSRM.geojson"


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
    return [X,Y]

def query_ways(tx):
    query="MATCH (ways) Return ways"
    return list(tx.run(query))

def leng_way_points(point1,point2):
    return math.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point1[1],2))


def guery_way(tx,args):

    query="MATCH (source:ways{ level:$start_level,X:$x,Y:$y}),(target:ways{level:$end_level,X:$x_end,Y:$y_end}),p = shortestPath((source)-[*]-(target)) Return p"
    result=tx.run(query,start_level= str(args[0]) ,x=args[1][0],y=args[1][1],end_level= str(args[2]),x_end=args[3][0],y_end=args[3][1])
    return result.data("p")

def search_way(startpoint,endpoint,startlevel,endlevel):
    with client.session() as session:
        way=session.read_transaction(guery_way,[startlevel,startpoint,endlevel,endpoint])
        search=[]
        for path in way[0]["p"]:
            if(path!="Routing"):
                search.append(path)
        print(search)



start_point=[int(sys.argv[1]),int(sys.argv[2])]
start_level=str(sys.argv[3])
end_point=[int(sys.argv[4]),int(sys.argv[5])]
end_level=str(sys.argv[6])

start_point=filter_ways(start_point[0],start_point[1],start_level)
end_point=filter_ways(end_point[0],end_point[1],end_level)

#test działąnia
#start_point=filter_ways(18.602784544967676,53.017013352,"-1")
#end_point=filter_ways(18.60239408804935,53.01733814244693,"1")

search_way(start_point,end_point,start_level,end_level)

client.close()
                
