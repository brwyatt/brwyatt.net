from brwyatt_web.file_loader import load_static_asset
from brwyatt_web.logging import setup_logging
from brwyatt_web.pages.errors import error500


log = setup_logging()


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    if event['resource'].startswith('/css/'):
        asset_type = 'css'
    elif event['resource'].startswith('/js/'):
        asset_type = 'js'
    else:
        asset_type = 'misc'
        if event['path'] == '/favicon.ico':
            return {
                'statusCode': 301,
                'headers': {
                    'Location': 'https://static.brwyatt.net/favicon.ico',
                },
                'body': '',
            }

    # Use the resource name, if given. Otherwise, use the path
    if event.get('pathParameters') is None:
        event['pathParameters'] = {}
    file_name = event['pathParameters'].get('resource', event['path'][1:])

    log.debug('Fetching "{}" resource with name "{}"'.format(
        asset_type, file_name))

    try:
        return load_static_asset(asset_type, file_name)
    except Exception as e:
        log.critical('Unexpected exception fetching resource "{}/{}": {}'
                     .format(asset_type, file_name, str(e)))
        return error500(event=event)
