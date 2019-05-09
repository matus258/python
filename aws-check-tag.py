#!/usr/bin/python3

import sys
import csv
import boto3

missing = []
found = []
first = 1

if len(sys.argv) < 2:
    print('\033[91mUSAGE: ./aws-check-tag.py [--profile profile] <tag1> [<tag2> <tag3> <...>]')
    exit()

if sys.argv[1] == '--profile':
    try:
        boto3.setup_default_session(profile_name=sys.argv[2])
        first = first + 2
    except:
        print('\033[91mERROR: Profile not found!')
        exit()
    
client = boto3.client('ec2')
response = client.describe_instances()

for r in response['Reservations']:
    for i in r['Instances']:
        if (i['State']['Code'] != 48):
            if i.get('Tags'):
                for t in i['Tags']:
                    if t['Key'] == 'Name':
                        name = t['Value']
                        for a in sys.argv[first:]:
                            failed = True
                            for tt in i['Tags']:
                                if tt['Key'] == a:
                                    found.append(tt['Value'])
                                    found.append(a)
                                    found.append(name)
                                    failed = False
                            if failed:
                                missing.append(a)
                                missing.append(name)
            else:
                missing.append('!!! Instance has no Tags !!!')
                missing.append(name)

with open('./aws-check-tag.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)


    if len(found)>0:
        wr.writerow(['Found in:'])
        print('\033[92mFound in:')
        while len(found)>0:
            out = [found.pop(), found.pop(), found.pop()]
            print(' '.join(out))
            wr.writerow(out)

        if len(missing)>0:
            wr.writerow([])
            print('')



    if len(missing)>0:
        wr.writerow(['Not found in:'])
        print('\033[91mNot found in:')
        while len(missing)>0:
            out = [missing.pop(), missing.pop()]
            print(' '.join(out))
            wr.writerow(out)
