import os

continueVal = True
if os.file.exists("accessKey.txt") == True or os.file.exists("secretKey.txt") == True:
	if raw_input("Files already exist.  Overwrite now? (y/n) ").lower() == 'n':
		continueVal = False
		accessKey = open("accessKey.txt").read().strip()
		secretKey = open("secretKey.txt").read().strip()
if continueVal = True:
	accessKey = raw_input("AWS Access Key: ")
	secretKey = raw_input("AWS Secret Key: ")
	print("You need to create an S3 Bucket with PUBLIC permissions before using this program")
	print("Bucket ID Example: https://s3.amazonaws.com/bucketName/")
	bucketID = raw_input("S3 Bucket ID: ")
	if bucketID[-1] != '/':
		bucketID = bucketID + '/'



def uploadFile(fileName):
	bucketIDVal = bucketID.partition(".com/")[2].partition("/")[0]
	conn = tinys3.Connection(accessKey,secretKey,tls=True)
	conn.upload(fileName, open(fileName,'rb'), bucketIDVal)
	return "https://s3.amazonaws.com/{}/{}".format(bucketIDVal, fileName)


if raw_input("Successfully grabbed configuration keys.  Test now? (y/n) ").lower() == 'y':
	import tinys3
	os.system("echo 'Echo Linguistics Test Upload' > testUpload.txt")
	fileUpload = uploadFile('testUpload.txt')
	print("Successfully uploaded file to {}".format(fileUpload))



file = open("accessKey.txt", "w")
file.write(accessKey)
file.close()

file = open("secretKey.txt", "w")
file.write(secretKey)
file.close()



#if raw_input("You need to create a ")
