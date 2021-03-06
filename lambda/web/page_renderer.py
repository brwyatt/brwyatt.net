from brwyatt_web.exceptions import FileNotFoundException
from brwyatt_web.logging import setup_logging
from brwyatt_web.pages import render_page
from brwyatt_web.pages.errors import error404, error500


log = setup_logging()


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    try:
        resp = render_page(event['path'], format='html', event=event)
    except FileNotFoundException as e:
        log.error('Caught 404 while rendering "{}"'.format(event['path']))
        resp = error404(event=event)
    except Exception as e:
        log.critical('Unexpected exception rendering route "{}": {} - {}'
                     .format(event['path'], e.__class__.__name__, str(e)))
        try:
            resp = error500(event=event)
        except Exception as e:
            log.critical('Failed to process 500 error, falling back to plain '
                         '500. {}: {}'.format(e.__class__.__name__, str(e)))
            resp = {
                'statusCode': '500',
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': (
                    '<h1>Error: 500</h1>'
                    '<p>Server encountered an error while '
                    'attempting to handle another server error.</p>'
                )
            }

    log.debug(f'sending response to client:\n{resp}')
    return resp
