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
            '  <title>STATIC TEST</title>'
            '</head>'
            '<body>'
            '  <h1>STATIC TEST</h1>'
            '  <h2>path</h2>'
            '  <pre>{path}</pre>'
            '  <h2>resource</h2>'
            '  <pre>{resource}</pre>'
            '  <h2>css</h2>'
            '  <pre>{css_dir}</pre>'
            '  <h2>js</h2>'
            '  <pre>{js_dir}</pre>'
            '</body>'
            '</html>'
        ).format(
            path=event['path'],
            resource=event['resource'],
            css_dir='\n'.join(os.listdir('/opt/static/css')),
            js_dir='\n'.join(os.listdir('/opt/static/js'))
        )
    }
