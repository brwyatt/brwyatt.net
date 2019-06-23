import json
import os
from urllib.parse import parse_qs

from brwyatt_web.logging import setup_logging
from brwyatt_web.pages import render_page
from brwyatt_web.pages.errors import error400


log = setup_logging()

stage = os.environ.get('STAGE', 'Alpha')

webdomain = os.environ.get('WEB_DOMAIN', 'brwyatt.net')


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    queryParams = event['queryStringParameters'] or {}
    postParams = {x: y[0] for x, y in
                  parse_qs(event['body']).items()}

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
        resp = error400(format='json', statusmsg='Missing link click data',
                        event=event)

    if 'headers' not in resp:
        resp['headers'] = {}

    resp['headers']['access-control-allow-methods'] = 'POST,OPTIONS'
    if stage == 'Beta':
        resp['headers']['access-control-allow-origin'] = '*'
    else:
        resp['headers']['access-control-allow-origin'] = f'https://{webdomain}'

    log.debug(f'sending response to client:\n{resp}')
    return resp
