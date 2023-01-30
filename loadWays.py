import json
import os
from neo4j import GraphDatabase

client = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Redkowice1"))
Scieszka="/var/www/html/OSRM.jos"


def filter_ways(faktures):
    Ways=[]
    for faktura in faktures:
        for keys in faktura["properties"].keys():
            if(keys == "highway"):
                if(faktura["properties"]["highway"]=="corridor"):
                    Ways.append(faktura)

    return Ways

def Create_graf(tx,properties,point,lastpoint):

    query="MERGE (:ways{ highway:$typway, level:$level,X:$x,Y:$y})"
@@@ guery+="-[:Routing{Leng:$leng}]-(:ways{ highway:$typway2, level:$level2,X:$x2,Y:$y2})"
    result=tx.run(query,typway=properties["highway"],level=properties["level"],x=point[1],y=point[2],typway2=properties["highway"],level2=properties["level"],x2=lastpoint[1],y2=lastpoint[2])
    print("działa")
    return result

def Create_graf_way(way,session):
    lastpoint=-1
    for point in way["geometry"]["coordinates"]:
        if(lastpoint!=-1):
            print(session.execute_write(create_graf,way["properties"],point,lastpoint))
            lastpoint=point


def add__ways(ways):
    session=client.session()
    for way in ways:
        Create_graf_way(way,session)
     session.close()




f= open(Scieszka,"r")
DANE=json.load(f)
f.close()
ways=filter_ways(DANE["features"])

add__ways(ways)

client.close()

