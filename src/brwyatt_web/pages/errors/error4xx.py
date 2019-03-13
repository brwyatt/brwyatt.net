import logging

from brwyatt_web.pages import render_page


log = logging.getLogger(__name__)


def error400(errmsg='Client Error', format='html', event={}):
    log.info('Rendering 400!')
    res = render_page('/errors/400', format=format, status_msg=errmsg,
                      event=event)
    res['statusCode'] = '400'
    return res


def error404(errmsg='File not found', format='html', event={}):
    log.info('Rendering 404!')
    res = render_page('/errors/404', format=format, status_msg=errmsg,
                      event=event)
    res['statusCode'] = '404'
    return res
