import tinys3
import time
import os
import sys

try:
	SECRET_KEY = open("secretCode.txt").read().strip()
except:
	raise Exception("No Secret Code File Found.  Run python awsIntegration.py to configure this program.")
try:
	ACCESS_KEY = open("accessKey.txt").read().strip()
except:
	raise Exception("No Access Key File Found.  Run python awsIntegration.py to configure this program.")
try:
	BUCKET_ID = open("bucketID.txt").read().strip()
except:
	raise Exception("No Bucket ID Found.  Run python awsIntegration.py to configure this program.")

def uploadFile(fileName):
	start = time.time()
	finalFileName = fileName.split('/')[-1]
	conn = tinys3.Connection(ACCESS_KEY,SECRET_KEY,tls=True)
	conn.upload(finalFileName, open(fileName,'rb'), BUCKET_ID)
	return "<speak><audio src='https://s3.amazonaws.com/{}/{}'/></speak>".format(BUCKET_ID, fileName)

if __name__ == '__main__':
	print("AWS Configuration\n")
	if os.path.exists("secretCode.txt") or os.path.exists("accessKey.txt") or os.path.exists("bucketID.txt"):
		if raw_input("Current files will be overwritten.  Continue? (Y/N) ").lower() != 'y':
			sys.exit(1)
	if os.path.exists("secretCode.txt") == False:
		raw_input("Input AWS Secret Key: ")
	if os.path.exists("accessKey.txt") == False:
		raw_input("Input AWS Access Key: ")
	if os.path.exists("bucketID.txt") == False:
		raw_input("Input S3 Bucket ID: ")
		