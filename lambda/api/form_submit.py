import json
import os
from urllib.parse import parse_qs

import brwyatt_web.forms.contact
from brwyatt_web.forms.helpers import validate_xsrf_token
from brwyatt_web.pages.errors import error400, error404
from brwyatt_web.logging import setup_logging

log = setup_logging()

stage = os.environ.get('STAGE', 'Alpha')

webdomain = os.environ.get('WEB_DOMAIN', 'brwyatt.net')

forms = {
    'contact': brwyatt_web.forms.contact.submit
}


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    source_ip = event['requestContext']['identity']['sourceIp']
    form_name = event['pathParameters']['form_name']

    if event['pathParameters']['form_name'] not in forms:
        resp = {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'status': 'Error',
                'message': 'Invalid form',
            }),
        }
    else:
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

        if validate_xsrf_token(postParams.pop('xsrf'), form_name, source_ip):
            resp = forms[form_name](**postParams, source_ip=source_ip)
        else:
            resp = {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': json.dumps({
                    'status': 'Error',
                    'message': 'Invalid XSRF Token',
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
