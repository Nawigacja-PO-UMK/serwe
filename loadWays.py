import json
import os
import math
from neo4j import GraphDatabase

client = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Redkowice1"))
Scieszka="/var/www/html/OSRM.jos"


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

    query="MERGE (:ways{ highway:$typway, level:$level,X:$x,Y:$y})-[:Routing{Leng:$leng}]-(:ways{ highway:$typway, level:$level,X:$x2,Y:$y2})"
    result=tx.run(query,typway=args[0]["highway"],level=args[0]["level"],x=args[1][0],y=args[1][1],x2=args[2][0],y2=args[2][1],leng=(leng_way_points(args[1],args[2])))
    return result

def Create_graf_way(way):
    with client.session() as session:
        lastpoint=-1
        for point in way["geometry"]["coordinates"]:
            if(lastpoint!=-1):
                session.write_transaction(Create_graf,[way["properties"],point,lastpoint])
            lastpoint=point



def add__ways(ways):
    for way in ways:
        Create_graf_way(way)





f= open(Scieszka,"r")
DANE=json.load(f)
f.close()
ways=filter_ways(DANE["features"])

add__ways(ways)

client.close()
