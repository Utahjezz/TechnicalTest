import json
import os

from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition

import config.config as config
import pre_processing
from client.img_rest_client import ImageDownloader
from pre_processing import InputImgElement

"""
The CustomClassifier class is a wrapper for Watson Visualization Recognition API
"""
class CustomClassifier():

    def __init__(self):
        self.visual_recognition = VisualRecognition('2016-05-20', api_key=config.api_key)
        self.downloader = ImageDownloader(config.yoox_rest_endpoint)

    """
    This method creates a new visual custom classifier starting from a file path.
    The path will be a directory containing a group of zip files filled with jpg images, each file represents a class sample data
    @type classifierName: string
    @param classifierName: new custom classifier name
    @type inputDataPath: string
    @param inputDataPath: zip files directory path
    """
    def create_custom_classifier(self, classifierName, inputDataPath): # it could take a negative examples data path as input
        params = {}
        for dirname, subdirs, files in os.walk(inputDataPath):
            for file in files:
                absname = os.path.abspath(os.path.join(dirname, file))
                name = os.path.splitext(os.path.basename(file))[0]
                params[name.replace("-", "_") + "_positive_examples"] = open(absname)
        if config.print_file_params_long_object:
            print params

        # for dirname, subdirs, files in os.walk(negDataPath):
        #     for file in files:
        #         absname = os.path.abspath(os.path.join(dirname, file))
        #         name = os.path.splitext(os.path.basename(file))[0]
        #         params["negative_examples"] = open(absname)

        print "Uploading files to Visual Recognition servers... It will take several time based on the number of images"
        response = self.visual_recognition.create_classifier(classifierName, **params)
        print "Watson classifier created: ", json.dumps(response)
        self.classifier_id = response['classifier_id']

    def sameIdCondition(self, id, inputID):
        return id == inputID

    """
    This method retrieves a classifier by id
    @type classifier_id: string
    @param classifier_id: classifier id
    @return response: Watson's representation of a classifier
    """
    def getClassifiers(self, classifier_id):
        response = self.visual_recognition.get_classifier(classifier_id=classifier_id)
        return response

    """
    This method retrieves this classifier representation
    @return response: Watson's representation of a classifier
    """
    def getClassifierStatus(self):
        return self.getClassifiers(self.classifier_id)

    """
    This method recharge a Watson visual recognition classifier by id
    @type classifier_id: string
    @param classifier_id: classifier id
    """
    def recharge_classifier(self, classifier_id):
        # if the classifier does not exist it will fail
        self.classifier_id = self.getClassifiers(classifier_id)['classifier_id']

    """
    This method requests to the classifier for an image classification starting from its ID
    @type imageId: string
    @param imageId: an image ID contained in the csv training set file
    @return: the visual recognition representation of the requested image classification
    """
    def classify_image_fromTrainingSet(self, imageId, threshold):
        # Read the CSV File
        allImages = pre_processing.readingFromInputFile(config.csv_path)
        # in a production env it should be necessary to handle the not found exception
        imgEl = [el for el in allImages if imageId == el.id][0]
        print config.temp_data_path
        if not os.path.isdir(config.temp_data_path):
            os.makedirs(config.temp_data_path)
        # Download the image
        imgPath = self.downloader.downloadAndSaveImage(config.temp_data_path, imgEl)
        print "Sending classification request to classifier"
        return self.visual_recognition.classify(open(imgPath), classifier_ids=[self.classifier_id], threshold=threshold)

    def classify_image(self, imageId, threshold):
        imgPath = self.downloader.downloadAndSaveImage(config.temp_data_path, InputImgElement(imageId))
        print "Sending classification request to classifier"
        return self.visual_recognition.classify(open(imgPath), classifier_ids=[self.classifier_id], threshold=threshold)

# create_custom_classifier("TechnicalTest", config.compressed_data_path)
# classifier = CustomClassifier()
# classifier.classify_image('46431302ib')
