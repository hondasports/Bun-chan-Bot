# -*- coding: utf-8 -*-

import botocore
import boto3
from datetime import datetime


class s3Uploader():
    
    def __init__(self, bucketName, objectName, filePath):
        self.__bucketName = bucketName
        self.__objectName = objectName
        self.__filePath = filePath
        self.__s3 = boto3.client('s3')

    def upload(self):

        if self.isExistObjectFor():
            print("{name} already exist.".format(name=self.__objectName))

            # Need refactoring...
            print("Delete {objectName}.".format(objectName=self.__objectName))
            self.__s3.delete_object(Bucket=self.__bucketName, Key=self.__objectName)

            print("Re-Upload {objectName} to {bucketName}.".format(bucketName=self.__bucketName, objectName=self.__objectName))
            self.uploadObject(self.__filePath)

        else:
            print("Upload {objectName} to {bucketName}.".format(bucketName=self.__bucketName, objectName=self.__objectName))
            self.uploadObject(self.__filePath)

    def uploadObject(self, path):
        with open(path, 'rb') as fh:
            self.__s3.put_object(Body=fh, Bucket=self.__bucketName, Key=self.__objectName)

    def isExistObjectFor(self):
        try:
            self.__s3.head_object(Bucket=self.__bucketName, Key=self.__objectName)
            return True

        except botocore.exceptions.ClientError as e:
            print(e)
            return False

    def isExistBucketFor(self):
        try:
            response = self.__s3.head_bucket(Bucket=self.__bucketName)
            # response = s3.head_bucket(Bucket='test-lambda-on-java')
            print(response)
            return True

        except botocore.exceptions.ClientError as e:
            print("The {bucketName} does not found".format(bucketName=self.__bucketName))
            print(e)

            return False
