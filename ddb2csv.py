import boto3
import csv
import os
from decimal import Decimal

def ddb2dict(item):
  dict = {}
  for k, v in item.items():
    for t, value in v.items():
      if t == 'N':
        dict[k] = Decimal(value)
      else:
        dict[k] = str(value)
        
  return dict

def copyToS3Bucket(filename):
  s3 = boto3.client('s3')

  with open(filename, 'rb') as csvfile:
    s3.put_object(
      Bucket=os.environ['FACTORS_BUCKET'],
      Key='yesno.csv',
      Body=csvfile
    )

def lambda_handler(event, context):
  ddb = boto3.client('dynamodb')

  with open('/tmp/yesno.csv', 'w', newline='') as csvfile:
    read = True
    last_key = None
    writer = None

    while read:
      resp = None
      if last_key == None:
        resp = ddb.scan(
          TableName=os.environ['FACTORS_TABLE'],
        )
      else:
        resp = ddb.scan(
          TableName=os.environ['FACTORS_TABLE'],
          ExclusiveStartKey=last_key,
        )
      
      if writer == None:
        fields = list(resp['Items'][0].keys())
        fields.remove('time')
        fields.remove('device_id')
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

      last_key = resp.get('LastEvaluatedKey', None)
      if last_key == None:
        read = False

      for item in resp['Items']:
        item.pop('time')
        item.pop('device_id')
        writer.writerow(ddb2dict(item))

    copyToS3Bucket('/tmp/yesno.csv')