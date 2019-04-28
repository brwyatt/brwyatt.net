from brwyatt_web.logging import setup_logging


log = setup_logging()


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    return {
        'statusCode': 200,
        'headers': {},
        'body': f'SIGNOUT: {event}',
    }
