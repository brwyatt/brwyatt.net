def error400(errmsg='Client Error'):
    return {
        'statusCode': '400',
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': (
            '<h1>ERROR: 400</h1>'
            f'<p>{errmsg}</p>'
        )
    }


def error404(errmsg='File not found'):
    return {
        'statusCode': '404',
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': (
            '<h1>ERROR: 404</h1>'
            f'<p>{errmsg}</p>'
        )
    }


def error500(errmsg='Server Error'):
    return {
        'statusCode': '500',
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': (
            '<h1>ERROR: 500</h1>'
            f'<p>{errmsg}</p>'
        )
    }
