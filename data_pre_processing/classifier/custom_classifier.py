import json
import os

from watson_developer_cloud import VisualRecognitionV3 as VisualRecognition

import config.config as config
import pre_processing
from client.img_rest_client import ImageDownloader


class CustomClassifier():
    def __init__(self):
        self.visual_recognition = VisualRecognition('2016-05-20', api_key=config.api_key)
        self.downloader = ImageDownloader(config.yoox_rest_endpoint)

    def create_custom_classifier(self, classifierName, inputDataPath):
        params = {}
        for dirname, subdirs, files in os.walk(inputDataPath):
            for file in files:
                absname = os.path.abspath(os.path.join(dirname, file))
                name = os.path.splitext(os.path.basename(file))[0]
                params[name.replace("-", "_") + "_positive_examples"] = open(absname)
        print params

        print "Uploading files..."
        response = json.dumps(self.visual_recognition.create_classifier(classifierName, **params))
        print "Watson classifier created: ", response
        self.classifier_id = response['classifier_id']

    def sameIdCondition(self, id, inputID):
        return id == inputID

    def getClassifiers(self, classifier_id):
        return self.visual_recognition.get_classifier(classifier_id=classifier_id)

    def recharge_classifier(self, classifier_id):
        self.classifier_id = classifier_id

    def classify_image(self, imageId):
        allImages = pre_processing.readingFromInputFile(
            '/Users/giacomogezzi/Documents/Yoox/TechnicalTest/training_set.csv')
        imgEl = [el for el in allImages if imageId == el.id][0]
        print config.temp_data_path
        if not os.path.isdir(config.temp_data_path):
            os.makedirs(config.temp_data_path)
        imgPath = self.downloader.downloadAndSaveImage(config.temp_data_path, imgEl)
        print "Sending classification request to classifier"
        print json.dumps(self.visual_recognition.classify(open(imgPath), classifier_ids=[self.classifier_id]))


# create_custom_classifier("TechnicalTest", config.compressed_data_path)
# classifier = CustomClassifier()
# classifier.classify_image('46431302ib')
