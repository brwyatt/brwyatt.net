from json import dumps

from brwyatt_api import test_str


def handler(event, context):
    return {
        'statusCode': '200',
        'body': dumps({
            'time': test_str
        })
    }
