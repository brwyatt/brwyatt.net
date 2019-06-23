import json
import os
from urllib.parse import parse_qs

from brwyatt_web.logging import setup_logging


log = setup_logging()

stage = os.environ.get('STAGE', 'Alpha')

webdomain = os.environ.get('WEB_DOMAIN', 'brwyatt.net')


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    queryParams = event['queryStringParameters'] or {}
    if event['headers'].get('Content-Type', '').startswith(
            'application/x-www-form-urlencoded'):
        postParams = {x: y[0] for x, y in
                      parse_qs(event['body']).items()}
    elif event['headers'].get('Content-Type', '').startswith(
            'application/json'):
        postParams = json.loads(event['body'])
    else:
        postParams = {}

    if ('Source' in postParams and 'Destination' in postParams and
            'Text' in postParams):
        logdata = postParams.copy()
        logdata['IPAddress'] = event['requestContext']['identity']['sourceIp']
        logdata['UserAgent'] = event['requestContext']['identity']['userAgent']
        log.info(json.dumps(logdata))
        resp = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'status': 'Success',
                'message': 'Click logged!',
            }),
        }
    else:
        log.error('Request did not include valid link click data')
        resp = 'Missing link click data',
        resp = {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'status': 'Error',
                'message': 'Missing link click data',
            }),
        }

    if 'headers' not in resp:
        resp['headers'] = {}

    resp['headers']['access-control-allow-methods'] = 'POST,OPTIONS'
    if stage == 'Beta':
        resp['headers']['access-control-allow-origin'] = '*'
    else:
        resp['headers']['access-control-allow-origin'] = f'https://{webdomain}'

    log.debug(f'sending response to client:\n{resp}')
    return resp
