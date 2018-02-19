from googletrans import Translator


try:
	SECRET_KEY = open("secretKey.txt").read().strip()
	ACCESS_KEY = open("accessKey.txt").read().strip()
	tempBucketID = open("bucketID.txt").read().strip()
except:
	print("No security credentials set up")
	print("create secretCode.txt and accessKey.txt")
	raise Exception("No config files")

# This just confirms that you have all configuration files
FFMPEG_FILE_LOCATION = "/tmp/ffmpeg.linux64"
# /tmp/ is the only lambda folder you have r/w access to
shutil.copyfile('/var/task/ffmpeg.linux64', FFMPEG_FILE_LOCATION)
# This copies the files in /var/task/ffmpeg.linux64 on every lambda run
os.chmod(FFMPEG_FILE_LOCATION, os.stat(FFMPEG_FILE_LOCATION).st_mode | stat.S_IEXEC)
# This makes that ffmpeg file executable
