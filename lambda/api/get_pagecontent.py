import json
import os

from brwyatt_web.exceptions import FileNotFoundException
from brwyatt_web.logging import setup_logging
from brwyatt_web.pages import render_page
from brwyatt_web.pages.errors import error400, error404, error500


log = setup_logging()

stage = os.environ.get('STAGE', 'Alpha')

webdomain = os.environ.get('WEB_DOMAIN', 'brwyatt.net')


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    queryParams = event['queryStringParameters'] or {}

    if 'page' in queryParams:
        try:
            resp = render_page(queryParams['page'], format='json', event=event)
        except FileNotFoundException as e:
            log.error('Caught 404 while rendering "{}"'.format(
                queryParams['page']))
            resp = error404(format='json', event=event)
        except Exception as e:
            log.critical('Unexpected exception rendering route "{}": {} - {}'
                         .format(queryParams['page'], e.__class__.__name__,
                                 str(e)))
            try:
                resp = error500(format='json', event=event)
            except Exception as e:
                log.critical('Failed to process 500 error, falling back to '
                             'plain 500. {}: {}'.format(
                                 e.__class__.__name__, str(e)))
                resp = {
                    'statusCode': '500',
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'title': 'Error: 500',
                        'content': '<p>Server encountered an error while '
                            'attempting to handle another server error.</p>',
                        'page': queryParams.get('page', None),
                    })
                }
    else:
        log.error('Request did not provide a page parameter')
        resp = error400(format='json', statusmsg='Missing "page" parameter',
                        event=event)

    if 'headers' not in resp:
        resp['headers'] = {}

    resp['headers']['access-control-allow-methods'] = 'GET,OPTIONS'
    if stage == 'Beta':
        resp['headers']['access-control-allow-origin'] = '*'
    else:
        resp['headers']['access-control-allow-origin'] = f'https://{webdomain}'

    log.debug(f'sending response to client:\n{resp}')
    return resp
