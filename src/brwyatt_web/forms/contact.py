import logging

from brwyatt_web.forms.helpers import delete_xsrf_token, validate_xsrf_token


log = logging.getLogger(__name__)


def submit(email, subject, body, xsrf, source_ip):
    log.info('Submitting Contact Form')
    if not validate_xsrf_token(xsrf, 'Contact', source_ip):
        return {
            'statusCode': '400',
            'headers': {},
            'body': 'Invalid XSRF',
        }

    delete_xsrf_token(xsrf, 'Contact', source_ip)
    return {
        'statusCode': '200',
        'headers': {},
        'body': 'So far so good...',
    }
