from brwyatt_web.logging import setup_logging
from brwyatt_web.file_loader import load_static_asset
from brwyatt_web.file_loader import FileNotFoundException, PathSecurityException
from brwyatt_web.pages.errors import error400, error404, error500


log = setup_logging()


def handler(event, context):
    log.info('Serving request from "{}" for "{}"'.format(
        event['requestContext']['identity']['sourceIp'],
        event['path']))
    log.debug('event: {}'.format(event))

    if event['resource'].startswith('/css/'):
        asset_type = 'css'
        content_type = 'text/css'
    elif event['resource'].startswith('/js/'):
        asset_type = 'js'
        content_type = 'application/javascript'
    else:
        log.error('Got unrecognized resource: "{}"'.format(event['resource']))
        return error400()

    file_name = event['pathParameters']['resource']

    log.debug('Fetching "{}" resource with name "{}"'.format(
        asset_type, file_name))

    try:
        return {
            'statusCode': '200',
            'headers': {
                'Content-Type': content_type,
            },
            'body': load_static_asset(asset_type, file_name)
        }
    except FileNotFoundException as e:
        log.error('Unable to find resource "{}/{}": {}'
                  .format(asset_type, file_name, str(e)))
        return error404()
    except PathSecurityException as e:
        log.error('Exception fetching resource "{}/{}": {}'
                  .format(asset_type, file_name, str(e)))
        return error400()
    except Exception as e:
        log.critical('Unexpected exception fetching resource "{}/{}": {}'
                     .format(asset_type, file_name, str(e)))
        return error500()
