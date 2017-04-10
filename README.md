# Technical Test

Creation and use of IBM Watson Visual Recognition API starting from a csv file with a "id" and a relative class

### Installation

Technical Test requires [Python](https://www.python.org) v2.7 to run.

Install the dependencies with [virtualenv](https://virtualenv.pypa.io/en/stable/) and [pip](https://pypi.python.org/pypi/pip).

Create a virtualenv environment
```sh
$ cd technical_test
$ virtualenv venv
$ . venv/bin/activate
```

Install python dependencies with pip install
```sh
(venv) $ pip install -r requirements.txt
```
the requirements.txt file is contained in the git repo.

### Run it (new custom classifier)

```sh
(venv) $ gunicorn -b 0.0.0.0:8000 'rest_app:init_new_classifier("/training_set.csv", 200)' --log-config logging.conf --reload --timeout 18000
```

1) First param is the csv file path on the local machine
2) It is the configurable number of images to be randomly selected for the resulting training set

A gunicorn server will run on the 8000 (or else) port of the machine

### Run it (from existing custom classifier)

```sh
(venv) $ gunicorn -b 0.0.0.0:8000 'rest_app:recharge_classifier("TechnicalTestClassifier_937605586", "/training_set.csv")' --log-config logging.conf --reload --timeout 1800
```

1) The Watson Visual Recognition custom classifier ID to be recharge
2) the csv file path on the local machine (file format "id", "className")

A gunicorn server will run on the 8000 (or else) port of machine

### REST endpoint

Request the classifier status
```http
GET http://localhost:8000/api/CustomClassifier/status
```
Response JSON object
```json
{
  "status": "training",
  "name": "TechnicalTestClassifier",
  "created": "2017-04-10T18:28:08.281Z",
  "classes": [
    {
      "class": "small_leather_goods"
    },
    {
      "class": "tops__tees"
    }
    // ...
  "classifier_id": "TechnicalTestClassifier_937605586"
}
```

Classify an image from the csv file
```http
POST http://localhost:8000/api/CustomClassifier/classify
```
Request JSON body
```json
{
	"imageId": "46370982ql"
}
```
Response JSON Object
```json

```
