import os

yoox_rest_endpoint = "http://ypic.yoox.biz/ypic/yoox/-resize/180/f/"

curr_path = os.path.dirname(os.getcwd())

raw_data_path = curr_path + "/raw_data/"

compressed_data_path = curr_path + "/compressed_data/"

img_format = "jpg"

compression_format = "zip"

deleteRawFileAfterCompression = True
