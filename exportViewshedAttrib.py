''' Created on Jul 4, 2023 @author: tsionas 
Wind Energy for Brussels (WEB) PROJECT 
Buildwind SRL and Université Catholique Louvain-la-Neuve, BELGIUM
co-funded by Innoviris '''

import datetime as dt
from scripting import *
# get a CityEngine instance
ce = CE()
#param initialisation
layerList = []
visList = []
path = 'c:/WEB/ce_results/'
i = 0
scene = ce.getObjectsFrom(ce.scene)
#Select layers
targetFilter = '*SUWT*'
print('Analysis for layers containing: ', targetFilter)
print('Make sure you have selected in the legend ONLY the Analyses layers contaning viewsheds')
#opening file for results
resultsFile = path + targetFilter[1:len(targetFilter)-1] + '.csv'
print('Exporting results to file', resultsFile)
start = dt.datetime.now()
print(start)
#open file (overwrite existing) and extract attributes to console and file
with open(resultsFile, "w") as f:
    #get all layers 
    allLayers = ce.getObjectsFrom(scene, ce.isLayer)
    #get targetFilter related layers
    targetLayers = ce.getObjectsFrom(scene, ce.isLayer, ce.withName(targetFilter))
    for eachLayer in targetLayers:
        #print('Layer:', eachLayer)
        layerList.append(eachLayer)
    #get selection from legend
    cLayers = ce.selection()
    print('Selected layers in legend', cLayers)
    #start examining layer
    if cLayers <> None:
        #get objects (viewsheds) within layers and their attributes
        counter = 0
        for cLayer in cLayers:
            layerName = ce.getName(cLayer)
            counter = counter + 1
            print('-------------------------------')
            print('Layer', counter, 'from')
            print(layerName, 'contains:')
            layerObjects = ce.getObjectsFrom(cLayer)
            for obj in layerObjects:
                print('Objects in layer:')
                print(obj)
                #get observer point as list
                objObsPos = ce.getObserverPoint(obj)
                print('Observer position', objObsPos)
                toFile = '\n' + str(objObsPos) + ', '
                f.write(toFile)
                #get viewing distance
                objDist = ce.getViewDistance(obj)
                print('Distance', objDist)
                toFile = str(objDist) + ', '
                f.write(toFile)
                #get viewshed angles as list
                objAngle = ce.getAnglesOfView(obj)
                print('Viewshed angle', objAngle)
                toFile = str(objAngle) + ', '
                f.write(toFile)
                #get visibility for all layers for selected viewshed as list
                vis = ce.getVisibleSolidAngle(obj, targetLayers)
                for visObj in vis:
                    visList.append(visObj)
                #report visibility per layer
                for i in range(len(layerList)):
                    print(layerList[i], visList[i]*1000)
                    toFile = str(layerList[i]) + ', '
                    f.write(toFile)
                    toFile = str(visList[i]*1000) + ', '
                    f.write(toFile)
                #clear list - method clear is not available here
                visList = []
    else:
        print('No layers selected')
end = dt.datetime.now()
print(end)
duration = end - start
print('Duration:', duration)
print('-----end of script')