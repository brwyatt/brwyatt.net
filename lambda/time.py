from datetime import datetime
from json import dumps


def handler(event, context):
    return {
        'statusCode': '200',
        'body': dumps({
            'time': str(datetime.utcnow())
        })
    }
