from kili.client import Kili
import os
from math import *

api_key="11aec368-1804-4df6-bf82-ee050d5a0d54"
api_endpoint=os.getenv("https://cloud.kili-technology.com/label/projects/ckw3h61f100e80kyu284b0x9k/explore?statusIn=LABELED&pageSize=5&currentPage=1&currentLabel=ckw3hh0q9009p0k4f0bov7lw1")
#initialisation Kili
test_asterix=Kili(api_key=api_key,api_endpoint=api_endpoint)
project_id="ckw3h61f100e80kyu284b0x9k"

#récupération des assets(images) de la source project_id
assets=test_asterix.assets(project_id=project_id)

def area(asset,label,length):
#cette condition a été installée car l'image "idefix.jpeg " n'a pas été labellé
    if(asset['externalId']!='idefix.jpeg'):
#recupération des points qui forment les labels
        dimensions=label["jsonResponse"]["JOB_0"]["annotations"][length]["boundingPoly"][0]["normalizedVertices"]
#calcul de la distance entre les deux points sur le même absisse
        abscisseLongueur=dimensions[1]['x']-dimensions[0]['x']
        ordonneLongueur=dimensions[1]['y']-dimensions[0]['y']
#distance égale à la racine carrée de la somme de la différence des coordonnées en abscisse et en ordonnée
        longueur=sqrt(pow(abscisseLongueur,2)+pow(ordonneLongueur,2))
        abscisseLargeur=dimensions[2]['x']-dimensions[1]['x']
        ordonneLargeur=dimensions[2]['y']-dimensions[1]['y']
        largeur=sqrt(pow(abscisseLargeur,2)+pow(ordonneLargeur,2))
        area=longueur*largeur
    else:
        area=0
    return area
    
#récupération des données dans un dictionnaire
def categorie(asset,label):
    dictionnaire={}
    categories=label['jsonResponse']['JOB_0']['annotations']
    length=len(categories)
    dictionnaire['id']=asset['externalId']
    dictionnaire['asterixs']=[]
    dictionnaire['obelixs']=[]
    print(asset['externalId'])
    if(asset['externalId']=='idefix.jpeg'):
        dictionnaire['id']=asset['externalId']
        dictionnaire['asterixs']=[]
        dictionnaire['obelixs']=[]
    else:
        if(length==1):
#ajout de la surface du label asterix dans le dictionnaire avec la clé astérix
            dictionnaire['asterixs'].append(area(asset,label,length-1))
            print(label["jsonResponse"]["JOB_0"]["annotations"][length-1]["boundingPoly"][0]["normalizedVertices"])
        elif(length==2):
#ajout de la surface du label obélix dans le dictionnaire avec la clé obélix
            dictionnaire['asterixs'].append(area(asset,label,length-2))
            print(label["jsonResponse"]["JOB_0"]["annotations"][length-2]["boundingPoly"][0]["normalizedVertices"])
            dictionnaire['obelixs'].append(area(asset,label,length-1))
            print(label["jsonResponse"]["JOB_0"]["annotations"][length-1]["boundingPoly"][0]["normalizedVertices"])
    return dictionnaire

#dictionnaire dans lequel on va stocké le resultat final
result=[]
for asset in assets:
    for label in asset['labels']:
        info=categorie(asset,label)
#ajout des informations de chaque image dans le dictionnaire
        result.append(info)
        break

#affichage du résultat final
for i in result:
    print(f"{i}\n\n")

