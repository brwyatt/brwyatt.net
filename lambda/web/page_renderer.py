from brwyatt_web.web import render_page
from brwyatt_web.web.errors import error404
from brwyatt_web.web.routes import routes


def handler(event, context):
    if event['path'] in routes:
        return render_page(**routes[event['path']]())
    else:
        return error404()
