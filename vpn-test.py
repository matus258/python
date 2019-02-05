#!/usr/bin/python3

import boto3
import json

ec2 = boto3.client('ec2')
r = ec2.describe_vpn_connections()

print(json.dumps(r, indent=2, default=str))