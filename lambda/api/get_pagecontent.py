from datetime import datetime
from json import dumps

from brwyatt_web.logging import setup_logging


log = setup_logging()


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
            resp = {
                'statusCode': '404',
                'body': json.dumps({
                    'Error': '404',
                    'Message': 'Not found'
                })
            }
        except Exception as e:
            log.critical('Unexpected exception rendering route "{}": {} - {}'
                         .format(queryParams['page'], e.__class__.__name__,
                                 str(e)))
            resp = {
                'statusCode': '500',
                'body': json.dumps({
                    'Error': '500',
                    'Message': 'Server error'
                })
            }
    else:
        log.error('Request did not provide a page parameter')
        resp = {
            'statusCode': '400',
            'body': json.dumps({
                'Error': '400',
                'Message': 'Missing "page" parameter'
            })
        }

    log.debug(f'sending response to client:\n{resp}')
    return resp
