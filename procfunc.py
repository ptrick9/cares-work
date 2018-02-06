import os
import matplotlib.pylab as plt
import cv2
import time
import numpy as np
import xml.dom.minidom
from darknet import *
import random


imageSize = (360, 640, 3)
meta = load_meta("cfg/custom.data")
net = load_net("cfg/tiny-yolo-size.cfg", "tiny-yolo-voc-custom-size_72000.weights", 0)
boxes = make_boxes(net)
probs = make_probs(net)
##must be called to creat default directory


def setupDir(homeFolder, teamName):
    imgDir = homeFolder + '/images'
    resultDir = homeFolder + '/result'
    timeDir = resultDir + '/time'
    xmlDir = resultDir + '/xml'
    myXmlDir = xmlDir + '/' + teamName
    allTimeFile = timeDir + '/alltime.txt'
    if os.path.isdir(homeFolder):
        pass
    else:
        os.mkdir(homeFolder)
        
    if os.path.isdir(imgDir):
        pass
    else:
        os.mkdir(imgDir)
        
    if os.path.isdir(resultDir):
        pass
    else:
        os.mkdir(resultDir)
        
    if os.path.isdir(timeDir):
        pass
    else:    
        os.mkdir(timeDir)
        
    if os.path.isdir(xmlDir):
        pass
    else:
        os.mkdir(xmlDir)

            
    if os.path.isdir(myXmlDir):
        pass
    else:
        os.mkdir(myXmlDir)
    ##create timefile file
    ftime = open(allTimeFile,'a+')
    ftime.close()

    return [imgDir, resultDir, timeDir, xmlDir, myXmlDir, allTimeFile]

## get image name list
def getImageNames(imgDir):
    nameset1 = []
    nameset2 = []
    namefiles= os.listdir(imgDir)
    for f in namefiles:
        if 'jpg' in f:
            imgname = f.split('.')[0]
            nameset1.append(imgname)
    nameset1.sort(key = int)
    for f in nameset1:
        f = f + ".jpg"
        nameset2.append(f)
    imageNum = len(nameset2)
    return [nameset2, imageNum]

def array_to_image(arr):
    arr = arr.transpose(2,0,1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (arr/255.0).flatten()
    data = c_array(c_float, arr)
    im = IMAGE(w,h,c,data)
    rgbgr_image(im)
    return im


def readImagesBatch(imgDir, allImageName, imageNum, iter, batchNumDiskToDram):
    start = iter*batchNumDiskToDram
    end = start + batchNumDiskToDram
    if end > imageNum:
        end = imageNum
    #batchImageData = np.zeros((end-start, imageSize[0], imageSize[1], imageSize[2]))
    batchImageData = []
    for i in range(start, end):
        imgName = imgDir + '/' + allImageName[i]
        #img = cv2.imread(imgName, 1)
        #batchImageData[i-start,:,:] = img[:,:]

        #batchImageData.append(array_to_image(img))
        batchImageData.append(imgName)
    return batchImageData



## detection and tracking algorithm
def detectionAndTracking(inputImageData, batchNum):
    result = np.zeros((batchNum,4))
    for i,file in enumerate(inputImageData):
        #print(file)
        r = detect(net, meta, "%s" % file, .1)
        #print(r)
        try:
            width = r[0][2][2]/2
            height = r[0][2][3]/2
            result[i][0] = r[0][2][0]-width #xmin
            result[i][1] = r[0][2][0]+width #xmax
            result[i][2] = r[0][2][1]-height #ymin
            result[i][3] = r[0][2][1]+height #ymax

            #print(r[0][2])

        except :
            pass
    #result = np.random.randn(batchNum, 4)
    return result

## store the results about detection accuracy to XML files
def storeResultsToXML(resultRectangle, allImageName, myXmlDir):
    for i in range(len(allImageName)):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('annotation')

        doc.appendChild(root)
        nameE = doc.createElement('filename')
        nameT = doc.createTextNode(allImageName[i])
        nameE.appendChild(nameT)
        root.appendChild(nameE)

        sizeE = doc.createElement('size')
        nodeWidth = doc.createElement('width')
        nodeWidth.appendChild(doc.createTextNode("640"))
        nodelength = doc.createElement('length')
        nodelength.appendChild(doc.createTextNode("360"))
        sizeE.appendChild(nodeWidth)
        sizeE.appendChild(nodelength)
        root.appendChild(sizeE)

        object = doc.createElement('object')
        nodeName = doc.createElement('name')
        nodeName.appendChild(doc.createTextNode("NotCare"))
        nodebndbox = doc.createElement('bndbox')
        nodebndbox_xmin = doc.createElement('xmin')
        nodebndbox_xmin.appendChild(doc.createTextNode(str(resultRectangle[i, 0])))
        nodebndbox_xmax = doc.createElement('xmax')
        nodebndbox_xmax.appendChild(doc.createTextNode(str(resultRectangle[i, 1])))
        nodebndbox_ymin = doc.createElement('ymin')
        nodebndbox_ymin.appendChild(doc.createTextNode(str(resultRectangle[i, 2])))
        nodebndbox_ymax = doc.createElement('ymax')
        nodebndbox_ymax.appendChild(doc.createTextNode(str(resultRectangle[i, 3])))
        nodebndbox.appendChild(nodebndbox_xmin)
        nodebndbox.appendChild(nodebndbox_xmax)
        nodebndbox.appendChild(nodebndbox_ymin)
        nodebndbox.appendChild(nodebndbox_ymax)

        #nodebndbox.appendChild(doc.createTextNode("360"))
        object.appendChild(nodeName)
        object.appendChild(nodebndbox)
        root.appendChild(object)

        fileName = allImageName[i].replace('jpg', 'xml')
        fp = open(myXmlDir + "/" + fileName, 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    return

##write time result to alltime.txt
def write(imageNum,runTime,teamName, allTimeFile):
    FPS = imageNum / runTime
    ftime = open(allTimeFile, 'a+')
    ftime.write( "\n" + teamName + " Frames per second:" + str((FPS)) + '\n')
    ftime.close()
    return
