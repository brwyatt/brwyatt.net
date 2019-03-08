import logging

from jinja2 import Environment, PackageLoader, select_autoescape

from brwyatt_web.exceptions import (
    FileNotFoundException, InvalidClientRequestException)
from brwyatt_web.pages.routes import routes


log = logging.getLogger(__name__)

templates = Environment(
    loader=PackageLoader(__name__, 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def render_page(path, format='html', event={}, status_msg=None):
    resp = {
        'statusCode': '200',
        'headers': {
        }
    }

    if path not in routes:
        raise FileNotFoundException('Invalid route')

    page_template = templates.get_template(routes[path])

    if format.lower() == 'html':
        base = 'base.html'
        resp['headers']['Content-Type'] = 'text/html',
    elif format.lower() == 'json':
        base = 'base.json'
        resp['headers']['Content-Type'] = 'application/json',
    else:
        raise InvalidClientRequestException(f'Unsupported format "{format}"')

    resp['body'] = page_template.render(event=event, base=base,
                                        status_msg=status_msg)
    return resp
