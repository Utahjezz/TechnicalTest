from classifier.custom_classifier import CustomClassifier
import falcon, json, traceback, config.config as config
import logging

class ClassifierResource():

    def __init__(self, classifier):
        self.classifier = classifier

    # def on_post(self, req, res):
    #     try:
    #         name = req['doc']['name']
    #         inputDataPath = config.config.compressed_data_path
    #         return self.classifier.create_custom_classifier(name, inputDataPath)
    #     except Exception as ex:
    #         traceback.print_exc()
    #         raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

    def on_post(self, req, resp):
        try:
            proceed = True
            # Input params : { "imageId": "xyz", "threshold" : 0.8}
            logging.info("POST request for classification " + json.dumps(req.context['doc']))
            imageId = req.context['doc']['imageId']
            threshold = req.context['doc']['threshold']

            # if active it will check the classifier status before proceeding with the classification
            if config.classifier_check_status_before_classification:
                status = self.classifier.getClassifierStatus()['status']
                proceed = status == "ready"

            if proceed:
                response = json.dumps(self.classifier.classify_image(imageId=imageId, threshold=threshold))
                logging.info("result of classification " + response)
                resp.status = "200"
            else:
                response = {
                    "msg": "Impossible to classify",
                    "classifier_status" : status,
                    "imageId": imageId
                }
                response = json.dumps(response)
                resp.status = "500"

            resp.body = response
        except Exception as ex:
            traceback.print_exc()
            logging.error("POST request for classification failed")

class ClassifierStatusResource():

    def __init__(self, classifier):
        self.classifier = classifier

    def on_get(self, req, resp):
        try:
            logging.info("GET request for classification ")
            response = json.dumps(self.classifier.getClassifierStatus())
            logging.info("result of status request " + response)
            resp.body = response
        except Exception as ex:
            traceback.print_exc()
            logging.error("GET request for classifier status failed")