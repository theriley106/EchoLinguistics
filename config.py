import os
accessKey = raw_input("AWS Access Key: ")
secretKey = raw_input("AWS Secret Key: ")
print("You need to create an S3 Bucket with PUBLIC permissions before using this program")
print("\nBucket ID Example: https://s3.amazonaws.com/bucketName/")
bucketID = raw_input("S3 Bucket ID: ")
if bucketID[-1] != '/':
	bucketID = bucketID + '/'




file = open("accessKey.txt", "w")
file.write(accessKey)
file.close()

file = open("secretKey.txt", "w")
file.write(secretKey)
file.close()



if raw_input("You need to create a ")
