from jinja2 import Template


def render_page(title='Untitled', content='No Content', status=200, event={}):
    page_template = Template(
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"'
        '  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
        '<html xmlns="http://www.w3.org/1999/xhtml">'
        '  <head>'
        '    <title>brwyatt.net - {{title}}</title>'
        '  </head>'
        '  <body>'
        '    <h1>brwyatt.net</h1>'
        '    <h2>{{title}}</h2>'
        '    <div>{{content}}</div>'
        '  </body>'
        '</html>'
    )

    return {
        'statusCode': str(status),
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': page_template.render(title=title, content=content)
    }


def render_error_page(status, errmsg, event={}):
    return render_page(
        title=f'ERROR: {status}',
        content=errmsg,
        status=status,
        event=event,
    )
