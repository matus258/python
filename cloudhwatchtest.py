#!/usr/bin/python3

import boto3
import json


regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "sa-east-1"]
res = list()
for region in regions:
	cloudwatch = boto3.client('cloudwatch', region_name=region )

	# List metrics through the pagination interface
	response = cloudwatch.list_metrics(Namespace='AWS/EC2')


print(json.dumps(response, indent=2, default=str))        