import os
import shutil

continueVal = True
if os.path.exists("sampleSkill/lambda/accessKey.txt") == True or os.path.exists("sampleSkill/lambda/secretKey.txt") == True:
	if raw_input("Files already exist.  Overwrite now? (y/n) ").lower() == 'n':
		continueVal = False
		accessKey = open("sampleSkill/lambda/accessKey.txt").read().strip()
		secretKey = open("sampleSkill/lambda/secretKey.txt").read().strip()
if continueVal == True:
	accessKey = raw_input("AWS Access Key: ")
	secretKey = raw_input("AWS Secret Key: ")
	print("You need to create an S3 Bucket with PUBLIC permissions before using this program")
	print("Bucket ID input Example: bucketname")
	bucketID = "https://s3.amazonaws.com/" + raw_input("S3 Bucket NAME: ") + "/"
	print("Bucket ID saved as: {}".format(bucketID))
	file = open("sampleSkill/lambda/accessKey.txt", "w")
	file.write(accessKey)
	file.close()

	file = open("sampleSkill/lambda/secretKey.txt", "w")
	file.write(secretKey)
	file.close()

	file = open("sampleSkill/lambda/bucketID.txt", "w")
	file.write(bucketID)
	file.close()


def uploadFile(fileName):
	bucketIDVal = open("sampleSkill/lambda/bucketID.txt").read().strip().partition(".com/")[2].partition("/")[0]
	conn = tinys3.Connection(open("sampleSkill/lambda/accessKey.txt").read().strip(),open("sampleSkill/lambda/secretKey.txt").read().strip(),tls=True)
	conn.upload(fileName, open(fileName,'rb'), bucketIDVal)
	return "https://s3.amazonaws.com/{}/{}".format(bucketIDVal, fileName)


if raw_input("Successfully grabbed configuration keys.  Test now? (y/n) ").lower() == 'y':
	try:
		import tinys3
	except:
		raise Exception("You need to run pip install -r requirements.txt")
	os.system("echo 'Echo Linguistics Test Upload' > testUpload.txt")
	fileUpload = uploadFile('testUpload.txt')
	print("Successfully uploaded file to {}".format(fileUpload))
	os.remove("testUpload.txt")

shutil.copyfile('EchoLinguistics.py', 'sampleSkill/lambda/EchoLinguistics.py')


#if raw_input("You need to create a ")
