import logging

from brwyatt_web.pages import render_page


log = logging.getLogger(__name__)


def error500(errmsg='Server Error', event={}):
    log.info('Rendering 500!')
    res = render_page('/errors/500', status_msg=errmsg, event=event)
    res['statusCode'] = '500'
    return res
