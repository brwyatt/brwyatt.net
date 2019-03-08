from brwyatt_web.web import render_error_page


def error400(errmsg='Client Error'):
    return render_error_page('400', errmsg)


def error404(errmsg='File not found'):
    return render_error_page('404', errmsg)
