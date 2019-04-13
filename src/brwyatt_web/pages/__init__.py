from datetime import datetime
from distutils.util import strtobool
import logging
import os
import yaml

from jinja2 import Environment, FileSystemLoader, select_autoescape

from brwyatt_web.exceptions import (
    FileNotFoundException, InvalidClientRequestException)


log = logging.getLogger(__name__)

gtag_ids = {
    'Beta': 'UA-33472085-6',
    'Gamma': 'UA-33472085-7',
    'Prod': 'UA-33472085-2'
}

webdomain = os.environ.get('WEB_DOMAIN', 'brwyatt.net')
apidomain = os.environ.get('API_DOMAIN', f'api.{webdomain}')
stage = os.environ.get('STAGE', 'Alpha')
stage_color = {'Alpha': 'darkred', 'Beta': 'darkgreen',
               'Gamma': 'indigo'}.get(stage, 'lightblue')

template_path = os.environ.get('TEMPLATE_PATH',
                               os.path.join(os.getcwd(), 'templates'))
templates = Environment(
    loader=FileSystemLoader(template_path),
    autoescape=select_autoescape(['html', 'xml'])
)

templates.globals['now'] = datetime.utcnow

routes_path = os.path.join(template_path, 'routes.yaml')

try:
    with open(routes_path) as f:
        routes = yaml.load(f)
except Exception as e:
    log.error('Error loading routes from file: {}: {}'.format(
        str(e.__class__.__name__), str(e)))
    routes = {}

log.debug('Loaded routes: {}'.format(routes))


def render_page(path, format='html', event={}, status_msg=None):
    log.info(f'Rendering page for "{path}" in "{format}"')

    if event is None:
        event = {}

    query_params = event.get('queryStringParameters', {})
    if query_params is None:
        query_params = {}

    template_vars = {
        'apidomain': apidomain,
        'event': event,
        'gtag_id': gtag_ids.get(stage, gtag_ids.get('Beta', 'UA-xxxxxxxx-x')),
        'hostname': event.get('stageVariables', {}).get('HostName',
                                                        'beta.brwyatt.net'),
        'nav_items': [
            ('Home', '/'),
            ('Projects', '/projects'),
            ('About', '/about'),
            ('Contact', '/contact')
        ],
        'page_path': path,
        'stage': stage,
        'stage_color': stage_color,
        'status_msg': status_msg,
        'style_debug': strtobool(query_params.get(
            'style_debug', str(stage in ['Beta', 'Alpha']))),
        'webdomain': webdomain,
    }

    log.debug(f'Template Vars = {template_vars}')

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

    resp['body'] = page_template.render(base=base, **template_vars)
    log.debug(f'Page rendered as:\n{resp["body"]}')
    return resp
