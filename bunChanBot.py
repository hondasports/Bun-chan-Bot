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
	try:
		subprocess.run('fswebcam -F 1 -S 20 -r 640x480 ' + os.path.dirname(os.path.abspath(__file__)) +  '/image.jpg', shell=True, check=True)

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
		twitter.update_status(status="Captured at {time}".format(time=formattedDateTime), media_ids=[image_ids['media_id']])

		# Upload object to S3
		bucketName = 'bun-chan-bot-images'
		objectName = "{name}.jpg".format(name=dt.strftime("%Y/%m/%d/%H%M%S"))
		uploader = s3Uploader.s3Uploader(bucketName, objectName, imageFileName)
		uploader.upload()
	
	except TwythonError as e:
		print(e)


if __name__ == '__main__':
	tweet()
