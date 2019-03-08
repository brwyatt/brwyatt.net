import json
import os


def handler(event, context):
    return {
        'statusCode': '200',
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': (
            '<html>'
            '<head>'
            '  <title>TEST PAGE</title>'
            '</head>'
            '<body>'
            '  <h1>TEST PAGE</h1>'
            '  <h2>Event</h2>'
            '  <pre>{event}</pre>'
            '  <h2>Context</h2>'
            '  <pre>{context}</pre>'
            '  <h2>/opt</h2>'
            '  <pre>{opt}</pre>'
            '</body>'
            '</html>'
        ).format(
            event=json.dumps(event, indent=4, sort_keys=True),
            context=json.dumps(context, indent=4, sort_keys=True),
            opt=json.dumps(os.listdir('/opt'), indent=4, sort_keys=True)
        )
    }
