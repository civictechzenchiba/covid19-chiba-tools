import boto3
import json
s3 = boto3.resource('s3')

def uploadS3(data,key='DataPub.json'):
    bucket = 'covid19chiba'
    obj = s3.Object(bucket, key)
    obj.put( Body=json.dumps(data),ACL='public-read')
    return