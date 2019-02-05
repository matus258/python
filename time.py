#!/usr/bin/python3

import boto3
import json
from datetime import datetime
now = datetime.now()

if now.month-1 == 1:

    start_time = datetime(now.year-1,now.month-1+11,now.day)
else:
    start_time=datetime(now.year,now.month-1,now.day)

end_time=datetime(now.year,now.month,now.day)

print(start_time)