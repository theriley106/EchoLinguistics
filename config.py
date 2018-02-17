import os
accessKey = raw_input("AWS Access Key: ")
secretKey = raw_input("AWS Secret Key: ")
file = open("accessKey.txt", "w")
file.write(accessKey)
file.close()
file = open("secretKey.txt", "w")
file.write(secretKey)
file.close()
