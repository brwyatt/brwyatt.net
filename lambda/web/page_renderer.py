from brwyatt_web.logging import setup_logging
from brwyatt_web.pages import render_page
from brwyatt_web.pages.errors import error404, error500
from brwyatt_web.pages.routes import routes


log = setup_logging()


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    if event['path'] in routes:
        log.debug('Path found in route list, rendering.')
        try:
            return render_page(**routes[event['path']]())
        except Exception as e:
            log.critical('Unexpected exception rendering route "{}": {} - {}'
                         .format(event['path'], e.__class__.__name__, str(e)))
            return error500()
    else:
        return error404()
