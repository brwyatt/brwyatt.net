import logging


log = logging.getLogger(__name__)


def submit(email, subject, body, source_ip):
    log.info('Submitting Contact Form')
    return {
        'statusCode': '200',
        'headers': {},
        'body': 'So far so good...',
    }
