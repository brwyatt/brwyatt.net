import logging
import os


log = logging.getLogger(__name__)


class PathSecurityException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


def load_static_asset(asset_type, file_name):
    """
    """
    log.info('Loading static asset: {0}: {1}'.format(asset_type, file_name))

    static_path = os.environ.get('STATIC_PATH',
                                 os.path.join(os.getcwd(), 'static'))
    log.debug('static_path = {}'.format(static_path))

    asset_dir = os.path.abspath(os.path.join(static_path, asset_type))
    log.debug('asset_dir = {}'.format(asset_dir))
    if static_path != os.path.commonpath([static_path, asset_dir]):
        errmsg = 'Asset directory is outside static assets directory'
        log.error(errmsg)
        raise PathSecurityException(errmsg)
    elif not os.path.isdir(asset_dir):
        errmsg = 'Asset type "{}" is invalid or does not exist'.format(
            asset_type)
        log.error(errmsg)
        raise FileNotFoundException(errmsg)

    file_path = os.path.abspath(os.path.join(asset_dir, file_name))
    log.debug('asset file_path = {}'.format(file_path))
    if asset_dir != os.path.commonpath([asset_dir, file_path]):
        errmsg = 'Requested asset is outside of expected asset directory'
        log.error(errmsg)
        raise PathSecurityException(errmsg)
    elif not os.path.isfile(file_path):
        errmsg = 'Asset file could not be found'
        log.error(errmsg)
        raise FileNotFoundException(errmsg)

    log.info('Asset size: {}'.format(os.path.getsize(file_path)))

    with open(file_path, 'r') as asset:
        content = asset.read()

    log.info('Successfully fetched "{}" asset "{}"'.format(asset_type,
                                                           file_name))

    return content
