import os

yoox_rest_endpoint = "http://ypic.yoox.biz/ypic/yoox/-resize/180/f/"

curr_path = os.path.dirname(os.getcwd())

raw_data_path = curr_path + "/raw_data/"

compressed_data_path = curr_path + "/compressed_data/"

temp_data_path = curr_path + "/temp"

classifier_id = "TechnicalTestClassifier_265586659"

img_format = "jpg"

compression_format = "zip"

deleteRawFileAfterCompression = True

api_key = "e1c50c6fa1e311101bed70d8c2cf0ab1c0fbc129"

csv_path = curr_path + "training_set.csv"

print_file_params_long_object = False

classifier_check_status_before_classification = True

classifier_status_training = "training"
classifier_status_ready = "ready"
classifier_status_failed = "failed"
