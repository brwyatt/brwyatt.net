from brwyatt_web.web import render_error_page


def error500(errmsg='Server Error'):
    return render_error_page('500', errmsg)
