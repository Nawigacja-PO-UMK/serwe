import json
import os
import math
from neo4j import GraphDatabase

client = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Redkowice1"))
Scieszka="/home/mateusz/source/serwe/OSRM.geojson"


def filter_ways(faktures):
    Ways=[]
    for faktura in faktures:
            if( "highway" in faktura["properties"] and  "level" in faktura["properties"]  ):
                if(faktura["properties"]["highway"]=="corridor" or  faktura["properties"]["highway"]=="steps" ):
                     Ways.append(faktura)

    return Ways

def leng_way_points(point1,point2):
    return math.sqrt(pow(point1[0]-point2[0],2)+pow(point1[1]-point1[1],2))


def Create_graf(tx,args):
    query="MERGE (:ways{ highway:$typway, level:$level,X:$x,Y:$y})"
    result=tx.run(query,typway=args[0]["highway"],level=args[0]["level"],x=args[1][0],y=args[1][1])
    return result

def Create_graf_relation(tx,args):
    query="MATCH (w1:ways{ level:$level,X:$x,Y:$y}) , (w2:ways{ level:$level,X:$x2,Y:$y2}) MERGE (w1)-[:Routing{Leng:$leng}]-(w2) RETURN w1"
    result=tx.run(query,level=args[0]["level"],x=args[1][0],y=args[1][1],x2=args[2][0],y2=args[2][1],leng=(leng_way_points(args[1],args[2])))
    return result


def Create_graf_relation_steps(tx,args):
    query="MATCH (w1:ways{ level:$level1,X:$x,Y:$y}) , (w2:ways{ level:$level2,X:$x2,Y:$y2}) MERGE (w1)-[:Routing{Leng:$leng}]-(w2) RETURN w2"
    result=tx.run(query,level1=str(args[0]),x=args[1][0],y=args[1][1],x2=args[2][0],y2=args[2][1],leng=(leng_way_points(args[1],args[2])),level2=str(args[3]))
    print(args[0],args[3])
    return result

def inconsistency_repair(tx,args):
    query="MATCH (w1:ways{ highway:$typway, level:$level,X:$x,Y:$y}) , (w2:ways{ highway:$typway, level:$level,X:$x2,Y:$y2}) MERGE (w1)-[:Routing{Leng:$leng1}]-(:ways{ highway:$typway, level:$level,X:$xc,Y:$yc})-[:Routing{Leng:$leng2}]-(w2) RETURN w1"
    result=tx.run(query,typway=args[0]["highway"],level=args[0]["level"],x=args[1][0],y=args[1][1],x2=args[2][0],y2=args[2][1],leng1=(leng_way_points(args[1],args[3])),leng2=(leng_way_points(args[2],args[3])),
                  xc=args[3][0],yc=args[3][1])
    return result


def is_consistency(ways,Point):
    lidzba=0
    for way in ways:
        for point in way["geometry"]["coordinates"]:
            if(Point[0]==point[0] and Point[1]==point[1]):
                lidzba=lidzba+1
            if(lidzba>1):
                return True;

    return False;


def query_ways(tx):
    query="MATCH (ways) Return ways"
    return list(tx.run(query))


def search_mini_lenght_ways(x,y,level,leng0=False):
    minway=-1
    X=-1
    Y=-1
    with client.session() as session:
        ways=session.read_transaction(query_ways)
        for way in ways:
            if(way.data("ways")["ways"]["level"]==level ):
                leng= leng_way_points([way.data("ways")["ways"]["X"],way.data("ways")["ways"]["Y"]],[x,y])
                if((leng!=0.0 or leng0) and (leng < minway or minway==-1)):
                    X=way.data("ways")["ways"]["X"]
                    Y=way.data("ways")["ways"]["Y"]
                    minway=leng
    return [X,Y]


def is_steirs(level):

    levels=level.split("-")
    if(len(levels)==1 or (levels[0]=="" and len(levels)==2)):
       return None

    level1=""
    level2=False
    pierwszy=True
    tmp=""
    for number in level:
        if number!="-" or pierwszy or level2 :
            tmp+=number
        else:
            level2=True
            level1=tmp
            tmp=""
        pierwszy=False
    level2=tmp
    return [level1,level2]




def creat_all_relation(way,point):
    with client.session() as session:
        if(~is_consistency(ways,point)):
            if(is_steirs(way["properties"]["level"])==None):
                w=search_mini_lenght_ways(point[0],point[1],way["properties"]["level"])
                session.write_transaction(Create_graf_relation,[way["properties"],point,w])
            else:
                steirs=is_steirs(way["properties"]["level"])
                w1=search_mini_lenght_ways(point[0],point[1],str(steirs[0]),leng0=True)
                w2=search_mini_lenght_ways(point[0],point[1],str(steirs[1]),leng0=True)
                if leng_way_points(w1,point)>leng_way_points(w2,point):
                   w2=w1
                   steirs[1]=steirs[0]
                print(w2,point)
                session.write_transaction(Create_graf_relation_steps,[way["properties"]["level"],point,w2,steirs[1]])

def search_inconsistency(ways):
        i=0
        for way in ways:
            creat_all_relation(way,way["geometry"]["coordinates"][0])
            point=way["geometry"]["coordinates"][len(way["geometry"]["coordinates"])-1]
            creat_all_relation(way,point)
            i+=1


def Create_graf_way(way):
    with client.session() as session:
        lastpoint=-1
        for point in way["geometry"]["coordinates"]:
            session.write_transaction(Create_graf,[way["properties"],point])
            if(lastpoint!=-1):
                session.write_transaction(Create_graf_relation,[way["properties"],point,lastpoint])
            lastpoint=point




def add__ways(ways):
    for way in ways:
        Create_graf_way(way)



f= open(Scieszka,"r")
DANE=json.load(f)
f.close()
ways=filter_ways(DANE["features"])

add__ways(ways)

search_inconsistency(ways)


client.close()
