import falcon, logging, pre_processing

from middleware.JSONTranslator import JSONTranslator
from resource.ClassifierResource import ClassifierResource
from classifier.custom_classifier import CustomClassifier

# start script: gunicorn -b 0.0.0.0:8000 'rest_app:start_app("csv", 200)' --log-config logging.conf --reload


def start_app(csvFile, numberOfClassElements):
    logging.info("Starting pre-processing from training set " + csvFile)
    app = falcon.API(middleware=[JSONTranslator()])
    pre_processing.init_pre_processing(numberOfClassElements, csvFile)
    customClassifier = CustomClassifier()
    classifierResource = ClassifierResource(customClassifier)

    app.add_route('/api/CustomClassifier', classifierResource)
    return app

