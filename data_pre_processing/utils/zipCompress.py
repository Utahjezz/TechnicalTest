import zipfile
import os


def zipdir(path, ziph):
    abs_src = os.path.abspath(path)
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            absname = os.path.abspath(os.path.join(dirname, file))
            arcname = absname[len(abs_src) + 1:]
            ziph.write(absname, arcname)


def start_zip(path, filename):
    print "Start zipping directory ", path
    zipf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
    zipdir(path, zipf)
    zipf.close()
    print "Stop zipping, output file = ", filename
