from classifier.custom_classifier import CustomClassifier
import falcon, json, traceback, config.config
import logging

class ClassifierResource():

    def __init__(self, classifier):
        self.classifier = classifier

    def on_post(self, req, res):
        try:
            name = req['doc']['name']
            inputDataPath = config.config.compressed_data_path
            return self.classifier.create_custom_classifier(name, inputDataPath)
        except Exception as ex:
            traceback.print_exc()
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

    def on_get(self, req, res):
        try:
            imageId = req['doc']['imageId']
            return self.classifier.classify_image(imageId)
        except Exception as ex:
            traceback.print_exc()
