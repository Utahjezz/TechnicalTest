import csv
import sys
import config.config as config
from random import shuffle

from client.img_rest_client import DownloaderThread


class InputImgElement:
    def __init__(self, id, imgClass = None):
        self.id = id
        self.imgClass = imgClass

    def __str__(self):
        return "Img: { id: " + self.id + ", class: " + self.imgClass + "}"

    def __repr__(self):
        return self.__str__()

def readingFromInputFile(csvFile):
    allImages = []
    with open(csvFile) as csvfile:
        print "Opening and importing csv input file"
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        idx = 0
        print "Initializing InputImgElement"
        for idx, row in enumerate(spamreader):
            img = InputImgElement(row[0], row[1])
            allImages.insert(idx, img)
    print "Found ", len(allImages), " elements in ", csvFile
    return allImages


classes = [] # list of classes


def countClasses(elements):
    count = 0
    for el in elements:
        if (el.imgClass not in classes):
            classes.append(el.imgClass)
    print "The input set contains classes: ", classes


def splittingCondition(setClass, elClass):
    return setClass == elClass;


elementsByClassDict = {} # { "className" : InputImgElement}


def splittingElementsByClass(elements, classes):
    for imgClass in classes:
        print "Splitting elements for class: " + imgClass
        subSet = [el for el in elements if splittingCondition(imgClass, el.imgClass)]
        print "Adding elements ", len(subSet), " for class: ", imgClass, " to the dictionary"
        elementsByClassDict[imgClass] = subSet


filteredElementsByClassDict = {} # { "className" : InputImgElement[]}


def shuffleElements(elements):
    shuffle(elements)


def selectingNElementsForClass(classes, elementsByClassDict, numberOfClassElements):
    for imgClass in classes:
        print "Start shuffling total set of class ", imgClass
        shuffleElements(elementsByClassDict[imgClass])
        filteredElementsByClassDict[imgClass] = elementsByClassDict[imgClass][:numberOfClassElements]
        print "Selected", numberOfClassElements, "random elements for class ", imgClass
        # if config.build_negative_set:
            # selectingNElementRandomlyForNegativeSet(imgClass, allElements, numberOfClassElements)

def selectingNElementRandomlyForNegativeSet(imgClass, elements, numberOfNegElements):
    # this function will work as the previous one but for negative samples
    print "Negative values TODO"
    # allNegElements = shuffle(numberOfNegElements)[:numberOfNegElements]

allElements = []

#allNegElements = []

# start the script, it reads from the csv file then split the images based on assigned classes, randomly selects n of them for their class
# finally it starts nClasses threads in order to improve the downloading task required time of execution (a fixed number of threads based
# on the local CPUs capabilities will be more effective)
def init_pre_processing(numberOfClassElements, csvFile): # it could be specified a negative example csv file (numberOfClassElements, csvFile, negCsvFile)
    allElements = readingFromInputFile(csvFile)

    if config.build_negative_set:
        print "It should be modified in order to take neg samples as input"
        # allNegElements = readingFromInputFile(negCsvFile)
    nClasses = countClasses(allElements)
    splittingElementsByClass(allElements, classes)

    selectingNElementsForClass(classes, elementsByClassDict, numberOfClassElements)
    threads = []
    # negThread = DownloaderThread(-1, "Thread-" + "Neg", "negative_samples", allNegElements)
    # negThread.start()
    # threads.append(negThread)
    for idx, imgClass in enumerate(classes):
        thread = DownloaderThread(idx, "Thread-" + imgClass, imgClass, filteredElementsByClassDict[imgClass])
        thread.start()
        threads.append(thread)
    for t in threads:
        t.join()
    print "Pre-processing python script completed! ============================>"

# it could be run standalone for offline data preparation to feed the classifier
if __name__ == '__main__':
    print "<============================ Pre-processing python script started with args: ", sys.argv
    if (len(sys.argv) < 3):
        print "ERROR: [Usage] pre_processing.py <inputFile>.csv <numOfElements>"
    else:
        numberOfClassElements = int(sys.argv[2])
        csvFile = sys.argv[1]
        init_pre_processing(numberOfClassElements, csvFile)
