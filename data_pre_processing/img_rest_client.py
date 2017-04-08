import urllib
import os
import threading
import zipCompress
import config

class ImageDownloader:
	def __init__(self, baseUrl):
		self.baseUrl = baseUrl

	def downloadImage(self, ImageID):
		img = urllib.urlopen(self.baseUrl + ImageID + "." + config.img_format)
		buf = img.read()
		return buf

	def compressDirectory(self, pathToZip, destinationDir, imgClass):
		zipDir = destinationDir
		if not os.path.isdir(zipDir):
			os.makedirs(zipDir)
		outputfile = zipDir + imgClass + "." + config.compression_format
		zipCompress.start_zip(pathToZip, outputfile)
		if (config.deleteRawFileAfterCompression):
			self.removeRawFile(pathToZip)

	def downloadAndSaveImage(self, path, inputImgElement):
		path += "/" + inputImgElement.id + "." + config.img_format
		file = open(path, "w+")
		imgBuf = self.downloadImage(inputImgElement.id)
		file.write(imgBuf)

	def downloadAllImagesForClass(self, imgClass, imgElements):
		currdir = os.path.dirname(os.getcwd())
		filePath = config.raw_data_path + imgClass
		directory = filePath
		if not os.path.isdir(filePath):
			os.makedirs(filePath)
		for el in imgElements:
			self.downloadAndSaveImage(directory, el)
		self.compressDirectory(directory, config.compressed_data_path, imgClass)

	def removeRawFile(self, dirToDelete):
		for root, dirs, files in os.walk(dirToDelete, topdown=False):
		    for name in files:
		        os.remove(os.path.join(root, name))
		    for name in dirs:
		        os.rmdir(os.path.join(root, name))

class DownloaderThread(threading.Thread):

	def __init__(self, threadID, name, imgClass, imgElements):
	    threading.Thread.__init__(self)
	    self.threadID = threadID
	    self.name = name
	    self.elements = imgElements
	    self.imgClass = imgClass

	def run(self):
		print "Starting downloader thread: " + self.name
		self.downloader = ImageDownloader(config.yoox_rest_endpoint)
		self.downloader.downloadAllImagesForClass(self.imgClass, self.elements)