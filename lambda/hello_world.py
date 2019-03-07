def handler(event, context):
    return {
        'statusCode': '200',
        'body': """
        <html>
        <head>
          <title>Hello World!</title>
        </head>
        <body>
          <h1>Hello World!</h1>
        </body>
        </html>
        """
    }
