from __future__ import print_function
import logging
import json
import decimal
import os
import time
from datetime import datetime
from functools import partial
import sys
CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CWD, "modules"))

from influxdb import InfluxDBClient

# enable basic logging to CloudWatch Logs
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def formatted_data(device, datatype, pt):
    return {
        'measurement': datatype,
        'tags': {
            'device': device,
        },
        'time': datetime(*time.gmtime(round(int(pt[datatype]['timestamp'])/1000))[:6]).isoformat(),
        'fields': {
            'x': float(pt[datatype]['x']),
            'y': float(pt[datatype]['y']),
            'z': float(pt[datatype]['z']),
        }
    }

def lambda_handler(event, context):
    payload = json.loads(event['body'])
    client = InfluxDBClient(
        os.environ['INFLUXDB_HOST'], 
        int(os.environ['INFLUXDB_PORT']), 
        os.environ['INFLUXDB_USER'],
        os.environ['INFLUXDB_PWD'],
        os.environ['INFLUXDB_DB']
        )

    deviceId = event['queryStringParameters']['device']

    acceleration_data = partial(formatted_data, deviceId, 'acceleration')
    acc = list(map(acceleration_data, payload))
    client.write_points(acc)

    gyroscope_data = partial(formatted_data, deviceId, 'gyroscope')
    gyro = list(map(gyroscope_data, payload))
    client.write_points(gyro)
    
    result = client.query("select x from acceleration")
    print("Result {0}".format(result))
    client.close()
    return { 'statusCode': 201 };