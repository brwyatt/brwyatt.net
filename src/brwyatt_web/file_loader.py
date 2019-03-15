import base64
import logging
import mimetypes
import os

from brwyatt_web.pages.errors import error400, error404


log = logging.getLogger(__name__)

static_path = os.environ.get('STATIC_PATH',
                             os.path.join(os.getcwd(), 'static'))


def load_static_asset(asset_type, file_name):
    """
    """
    log.info('Loading static asset: {0}: {1}'.format(asset_type, file_name))

    log.debug('static_path = {}'.format(static_path))

    asset_dir = os.path.abspath(os.path.join(static_path, asset_type))
    log.debug('asset_dir = {}'.format(asset_dir))
    if static_path != os.path.commonpath([static_path, asset_dir]):
        errmsg = 'Asset directory is outside static assets directory'
        log.error(errmsg)
        return error400()
    elif not os.path.isdir(asset_dir):
        errmsg = 'Asset type "{}" is invalid or does not exist'.format(
            asset_type)
        log.error(errmsg)
        return error404()

    file_path = os.path.abspath(os.path.join(asset_dir, file_name))
    log.debug('asset file_path = {}'.format(file_path))
    if asset_dir != os.path.commonpath([asset_dir, file_path]):
        errmsg = 'Requested asset is outside of expected asset directory'
        log.error(errmsg)
        return error400()
    elif not os.path.isfile(file_path):
        errmsg = 'Asset file could not be found'
        log.error(errmsg)
        return error404()

    log.info('Asset size: {}'.format(os.path.getsize(file_path)))

    content_type = mimetypes.guess_type(file_name)[0]
    log.info(f'Guessing mimetype as "{content_type}"')

    res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': content_type,
        },
    }

    with open(file_path, 'rb') as asset:
        content = asset.read()

    try:
        log.debug('Attempting to encode string')
        res['body'] = str(content, 'utf-8')
    except UnicodeDecodeError as e:
        log.debug('Unable to encode as string, base64 encoding instead')
        res['body'] = str(base64.b64encode(content), 'utf-8')
        res['isBase64Encoded'] = True

    log.info('Successfully fetched "{}" asset "{}"'.format(asset_type,
                                                           file_name))

    return res
