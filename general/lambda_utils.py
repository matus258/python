import json
import boto3
from os import environ
from os.path import basename
from base64 import b64decode
from boto3.dynamodb.conditions import Attr
from smtplib import SMTP
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def notify(to_addr, subject, data, dtype='plain', files=[], cc=[]):
    from_addr = environ['SENDER_EMAIL_ADDRESS']
    addr_pass =  boto3.client('kms').decrypt(CiphertextBlob=b64decode(environ['SENDER_EMAIL_PASSWORD']))['Plaintext'].decode('utf-8')
    
    try:
        msg = MIMEMultipart()
        msg['To'] = to_addr
        msg['Cc'] = ', '.join(cc)
        msg['From'] = from_addr
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(str(data), dtype))
        
        for f in files or []:
            with open(f, 'rb') as file:
                part = MIMEApplication(
                    file.read(),
                    Name=basename(f)
                )
            
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

        svr = SMTP('smtp.gmail.com', 587)
        svr.ehlo()
        svr.starttls()
        svr.ehlo()
        svr.login(
            from_addr,
            addr_pass
        )

        svr.sendmail(from_addr, [to_addr]+cc, msg.as_string())

    except Exception as err:
        print(str(err.args[0]), 500)
        return str(err.args[0]), 500
    
    return 'Email sent.', 200


def role_arn_to_session(arn_id,session):
    client = session.client('sts')
    response = client.assume_role(
        RoleArn="arn:aws:iam::"+arn_id+":role/"+environ['AWS_ROLE_NAME'],
        RoleSessionName=environ['AWS_SESSION_NAME']
    )
    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken']
    )

def switch_role(alias,session):
    lbd = session.client('lambda')
    arn_finder = lbd.invoke(
        FunctionName='rivendel_backup_ami_crud:'+ environ['LAMBDA_ENV'],
        Payload=json.dumps({"alias": alias, "type": "list"})
    )['Payload'].read().decode("utf-8")
    arn_id = [*json.loads(arn_finder)][0]
    return role_arn_to_session(arn_id,session)

def boto_session(params):
    session = False
    if params.get('akid') and params.get('aksecret'):
        session = boto3.Session(
            aws_access_key_id=params['akid'],
            aws_secret_access_key=params['aksecret']
        )
    if(session):
        if params['alias']:
            session = switch_role(params['alias'], session)
    return session

def boto_get_all_pages(func, **kwargs):
    results = []
    token = None
    while True:
        if token:
            kwargs.update({'NextPageToken': token})
        elif kwargs.get('NextPageToken'):
            del kwargs['NextPageToken']
        data = func(**kwargs)
        results.append(data)
        token = data.get('NextPageToken')
        if not token:
            break
    return results

def verify_parameters(event, params):
    body = dict()
    headers = dict()
    query = dict()
    if event.get('body') and event['body']:
        body = json.loads(event['body'])
    
    if event.get('headers') and event['headers']:
        headers = event['headers']
    
    if event.get('queryStringParameters') and event['queryStringParameters']:
        query = event['queryStringParameters']
        
    for k,p in params.items():
        if headers.get(k):
            params[k] = headers[k]
        elif body.get(k):
            params[k] = body[k]
        elif query.get(k):
            params[k] = query[k]
        elif event.get(k):
            params[k] = event[k]
        
    return params

def final_response(code, result):
    response = {
        'statusCode': code,
        'body': json.dumps(result, sort_keys=True,indent=4)
    }
    return response
    
def dynamo_to_item(raw):
    # To go from python to low-level format
    boto3.resource('dynamodb')
    serializer = boto3.dynamodb.types.TypeSerializer()
    low_level_copy = {k: serializer.serialize(v) for k,v in raw.items()}
    return low_level_copy

def dynamo_from_item(raw):
    # To go from low-level format to python
    boto3.resource('dynamodb')
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    python_data = {k: deserializer.deserialize(v) for k,v in raw.items()}
    return python_data

def dynamo_get_items(value, key, table):
    ids = []
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table)
    
    response = table.scan(
        FilterExpression=Attr(key).eq(value)
    )
    
    if len(response['Items']) > 0:
        ids = response['Items']
    
    return ids
    
def dynamo_put_item(obj, table):
    client = boto3.client('dynamodb')
    response = client.put_item(TableName=table, Item=obj)