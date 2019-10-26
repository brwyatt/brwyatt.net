import json
import os
from urllib.parse import parse_qs

from brwyatt_web.forms.contact import submit
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
    clientHeaders = {key.lower(): value for key, value
                     in event['headers'].items()}
    if clientHeaders.get('content-type', '').lower().startswith(
            'application/x-www-form-urlencoded'):
        postParams = {x: y[0] for x, y in
                      parse_qs(event['body']).items()}
    elif clientHeaders.get('content-type', '').lower().startswith(
            'application/json'):
        postParams = json.loads(event['body'])
    else:
        postParams = {}

    resp = submit(postParams['email'], postParams['subject'],
                  postParams['body'], postParams['xsrf'],
                  event['requestContext']['identity']['sourceIp'])

    if 'headers' not in resp:
        resp['headers'] = {}

    resp['headers']['access-control-allow-methods'] = 'POST,OPTIONS'
    if stage == 'Beta':
        resp['headers']['access-control-allow-origin'] = '*'
    else:
        resp['headers']['access-control-allow-origin'] = f'https://{webdomain}'

    log.debug(f'sending response to client:\n{resp}')
    return resp
