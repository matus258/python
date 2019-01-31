#!/usr/bin/python3

import boto3
import json

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
#print(json.dumps(response.get('ResponseMetadata').get('HTTPStatusCode'), indent=2, default=str))
#str(1) # '1'
#for key in response.get('Reservations')[0].get('Instances')[0].get('State'):
#   print(key)
#print(json.dumps(response.get('Reservations')[0].get('Instances')[0].get('Tags')[1].get('Key'), indent=2, default=str))

test = response.get('Reservations')[0].get('Instances')[0].get('Tags')[1].get('Key')

if test == "Name":
    print("1")
else:
    print("0")