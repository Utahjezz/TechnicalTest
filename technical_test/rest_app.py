import falcon, logging, pre_processing
import config.config as config

from middleware.JSONTranslator import JSONTranslator
from resource.ClassifierResource import ClassifierResource
from resource.ClassifierResource import ClassifierStatusResource
from classifier.custom_classifier import CustomClassifier

# start script NEW CLASSIFIER: e.g. gunicorn -b 0.0.0.0:8000 'rest_app:init_new_classifier("/training_set.csv", 200)' --log-config logging.conf --reload --timeout 1800


"""
Init REST App with a new custom classifier instance, 
it takes as input a csv file path and the number of elements to be randomly selected for provided classes
@type csvFile: string
@param csvFile: the absolute path of a csv file (file format: "imageId", "className")
@type numberOfClassElements: number
@param numberOfClassElements: number of element to be randomly selected for each class of the csv file
@return app: a falcon API app for gunicorn o wsgi server
"""
def init_new_classifier(csvFile, numberOfClassElements):
    logging.info("Starting new classifier from scratch")
    logging.debug("pre-processing from training set " + csvFile)
    pre_processing.init_pre_processing(numberOfClassElements, csvFile)
    config.csv_path = csvFile
    customClassifier = CustomClassifier()
    customClassifier.create_custom_classifier('TechnicalTestClassifier', config.compressed_data_path)

    return initialize_rest_app(customClassifier)

# start script EXISTING_CLASSIFIER: e.g. gunicorn -b 0.0.0.0:8000 'rest_app:recharge_classifier("TechnicalTestClassifier_937605586", "/training_set.csv")' --log-config logging.conf --reload --timeout 1800

"""
Init REST App with an existing classifier (e.g.: TechnicalTestClassifier_937605586). it is possible to find this ID
on IBM Watson Api Explorer. It also needs a csv file in order to download images from yoox apis (file format: "imageId", "className")
@type classifierId: string
@param classifierId: the IBM Watson Visual Recognition custom classifier ID
@type csvFile: string
@param csvFile: the absolute path of a csv file (file format: "imageId", "className")
@return app: a falcon API app for gunicorn o wsgi 
"""
def recharge_classifier(classifierId, csvFile):
    logging.info("Starting existing classifier " + classifierId)
    config.csv_path = csvFile
    customClassifier = CustomClassifier()
    customClassifier.recharge_classifier(classifier_id = classifierId)
    return initialize_rest_app(customClassifier)

def initialize_rest_app(customClassifier):
    app = falcon.API(middleware=[JSONTranslator()])
    classifierResource = ClassifierResource(customClassifier)
    logging.info("Registered REST endpoint POST /api/CustomClassifier/classify for image classification")
    app.add_route('/api/CustomClassifier/classify', classifierResource)

    classifierStatusResource = ClassifierStatusResource(customClassifier)
    logging.info("Registered REST endpoint GET /api/CustomClassifier/status for image classification")
    app.add_route('/api/CustomClassifier/status', classifierStatusResource)
    return app