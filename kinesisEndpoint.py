import boto3
import os
import json

def batchRecords(records, batchSize = 500):
  recordSets = []
  i = 0
  while records[i:i+batchSize]:
    recordSets.append(records[i:i+batchSize])
    i = i + batchSize

  return recordSets

def addDevice(device, record):
  record['device'] = device
  return record

def kinesisRecord(record):
  return {
    'Data': json.dumps(record).encode(),
    'PartitionKey': record['device']
  }

def lambda_handler(event, context):
  payload = json.loads(event['body'])
  deviceId = event['queryStringParameters']['device']

  kss = boto3.client('kinesis')

  batches = batchRecords(payload)
  for batch in batches:
    batch = list(map(lambda r: addDevice(deviceId, r), batch))
    batch = list(map(kinesisRecord, batch))
  
    kss.put_records(
      Records=batch,
      StreamName=os.environ['KINESIS_STREAM'] 
      )

  return { 
    'statusCode': 201, 
    'headers': {
      'Access-Control-Allow-Origin' : '*',
    } 
  }
