from datetime import datetime
import logging
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

from brwyatt_web.exceptions import (
    FileNotFoundException, InvalidClientRequestException)
from brwyatt_web.pages.routes import routes


log = logging.getLogger(__name__)

ga_tracking_ids = {
    'Beta': 'UA-33472085-6',
    'Gamma': 'UA-33472085-7',
    'Prod': 'UA-33472085-2'
}

template_path = os.environ.get('TEMPLATE_PATH',
                               os.path.join(os.getcwd(), 'templates'))
templates = Environment(
    loader=FileSystemLoader(template_path),
    autoescape=select_autoescape(['html', 'xml'])
)

templates.globals['now'] = datetime.utcnow


def render_page(path, format='html', event={}, status_msg=None):
    log.info(f'Rendering page for "{path}" in "{format}"')

    resp = {
        'statusCode': '200',
        'headers': {
        }
    }

    if path not in routes:
        log.error(f'No route found for "{path}"')
        raise FileNotFoundException('Invalid route')

    page_template = templates.get_template(routes[path])

    if format.lower() == 'html':
        base = 'base.html'
        resp['headers']['Content-Type'] = 'text/html'
    elif format.lower() == 'json':
        base = 'base.json'
        resp['headers']['Content-Type'] = 'application/json'
    else:
        log.error('Unsupported format "{format}"')
        raise InvalidClientRequestException(f'Unsupported format "{format}"')

    resp['body'] = page_template.render(
        event=event, base=base, status_msg=status_msg,
        ga_code=ga_tracking_ids.get(event['stageVariables']['Stage'],
                                    ga_tracking_ids.get('Beta', 'xxxx')))
    log.debug(f'Page rendered as:\n{resp["body"]}')
    return resp
