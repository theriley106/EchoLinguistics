import os
import shutil
import boto3
import stat
import datetime

lambda_tmp_dir = '/tmp'
ffmpeg_bin = "{0}/ffmpeg.linux64".format(lambda_tmp_dir)
shutil.copyfile('/var/task/ffmpeg.linux64', ffmpeg_bin)
os.chmod(ffmpeg_bin, os.stat(ffmpeg_bin).st_mode | stat.S_IEXEC)


def lambda_handler(event, context):
	os.system('{} -version'.format(ffmpeg_bin))
