import tinys3
import time

SECRET_KEY = open("secretCode.txt").read().strip()
ACCESS_KEY = open("accessKey.txt").read().strip()
BUCKET_ID = open("bucketID.txt").read().strip()

def uploadFile(fileName):
	start = time.time()
	finalFileName = fileName.split('/')[-1]
	conn = tinys3.Connection(ACCESS_KEY,SECRET_KEY,tls=True)
	conn.upload(finalFileName, open(fileName,'rb'), BUCKET_ID)
	return "<speak><audio src='https://s3.amazonaws.com/{}/{}'/></speak>".format(BUCKET_ID, fileName)
