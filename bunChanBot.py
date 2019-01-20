# -*- coding: utf-8 -*-

import subprocess
import sys
import configparser
from PIL import Image
import io
import os
from twython import Twython, TwythonError
from datetime import datetime

import s3Uploader

def tweet():

	config = configparser.ConfigParser()
	config.read(os.path.dirname(os.path.abspath(__file__)) + '/twitter.config')

	twitter = Twython(
		config['KEY']['CONSUMER_KEY'],
		config['KEY']['CONSUMER_SECRET'],
		config['KEY']['ACCESS_TOKEN'],
		config['KEY']['ACCESS_TOKEN_SECRET']); 

	#try:
	#	twitter.update_status(status='Tweet Sample')
	#except TwythonError as e:
	#	print(e)

	image_io = None
	imageFileName = os.path.dirname(os.path.abspath(__file__)) + '/image.jpg'
	videoFileName = os.path.dirname(os.path.abspath(__file__)) + '/video.mp4'

	try:
		subprocess.run('fswebcam -F 1 -S 20 -r 1920×1080 ' + imageFileName, shell=True, check=True)
		subprocess.run('ffmpeg -f alsa -f v4l2 -thread_queue_size 8192 -s 1280x720 -i /dev/video0 -t 20 -c:v h264_omx -b:v 2000k -y ' + videoFileName, shell=True, check=True)
	except subprocess.CalledProcessError as e:
		print(e)

	else:
		photo = Image.open(imageFileName);
		image_io = io.BytesIO()
		photo.save(image_io, format='JPEG')

		image_io.seek(0)
	try:

		dt = datetime.now()

		formattedDateTime = dt.strftime("%Y/%m/%d %H:%M:%S")
		image_ids = twitter.upload_media(media=image_io)
		twitter.update_status(status="Captured at {time} #文鳥".format(time=formattedDateTime), media_ids=[image_ids['media_id']])

		with open(videoFileName, 'rb') as video:
			response = twitter.upload_video(media=video, media_type='video/mp4')
			twitter.update_status(status="Captured video at {time} #文鳥".format(time=formattedDateTime), media_ids=[response['media_id']])

		# Upload object to S3
		bucketName = 'bun-chan-bot-images'
		objectName = "{name}.jpg".format(name=dt.strftime("%Y/%m/%d/%H%M%S"))
		uploader = s3Uploader.s3Uploader(bucketName, objectName, imageFileName)
		uploader.upload()

		objectName = "{name}.mp4".format(name=dt.strftime("%Y/%m/%d/%H%M%S"))
		uploader = s3Uploader.s3Uploader(bucketName, objectName, videoFileName)
		uploader.upload()

	except TwythonError as e:
		print(e)


if __name__ == '__main__':
	tweet()
