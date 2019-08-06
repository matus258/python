#!/usr/bin/python36

## Parameters:
# MetricName. Eg: CurrConnections
# Function. Can be one of the following: Average, Sum, SampleCount, Maximum, or Minimum.
# Dimension. Eg: CacheClusterId=cache,CacheNodeId=0001
# Region. Eg: eu-west-1
# AWS_Access_Key
# AWS_Secret_Access_Key

import sys
import datetime
import boto3

try:
    metName = sys.argv[1]
    funcName = sys.argv[2]
    dimName = sys.argv[3]
    dimValue = sys.argv[4]
    nameSpace = sys.argv[5]
    region = sys.argv[6]
    accessKey = sys.argv[7]
    secretKey = sys.argv[8]

except:
    print("Usage: get_aws.py MetricName Function DimensionName DimensionValue nameSpace Region AWS_ACCESS_KEY AWS_SECRET_ACCESS_KEY")
    print("Example: get_aws.py CurrConnections Average \"CacheClusterId=cache,CacheNodeId=0001\" eu-west-1 ACCESS_KEY SECRET_ACCESS_KEY")
    sys.exit(1)

c = boto3.client('cloudwatch',aws_access_key_id=accessKey, aws_secret_access_key=secretKey, region_name=region)
end = datetime.datetime.utcnow()
start = end - datetime.timedelta(minutes=5)
r = c.get_metric_statistics(
    Namespace= nameSpace,
    MetricName= metName,
    Dimensions= [
        {
            'Name': dimName,
            'Value': dimValue
        },
    ],
    StartTime=start,
    EndTime=end,
    Period=300,
    Statistics=['SampleCount','Average','Sum','Minimum','Maximum'])
try:
    print(r.get("Datapoints")[0].get('Average'))
except Exception as e:
    print(e)
