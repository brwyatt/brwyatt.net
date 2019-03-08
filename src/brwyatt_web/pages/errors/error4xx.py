import logging

from brwyatt_web.pages import render_page


log = logging.getLogger(__name__)


def error400(errmsg='Client Error'):
    log.info('Rendering 404!')
    res = render_page('/errors/400', status_msg=errmsg)
    res['statusCode'] = 400
    return res


def error404(errmsg='File not found'):
    log.info('Rendering 400!')
    res = render_page('/errors/404', status_msg=errmsg)
    res['statusCode'] = 404
    return res
