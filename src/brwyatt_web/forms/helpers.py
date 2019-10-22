from datetime import datetime
from uuid import UUID, uuid4, uuid5

from boto3 import resource

xsrf_table = resource('dynamodb', endpoint_url="http://localhost:3000").Table("XSRF")


def save_xsrf_token(token, ttl=7200):
    xsrf_table.put_item(Item={
        "Token": str(token),
        "Expires": int(datetime.utcnow().timestamp())+ttl,
    })


def validate_xsrf_token(form_token, form_name, ip):
    response = xsrf_table.get_item(Key={
        "Token": str(uuid5(uuid5(UUID(form_token), form_name), ip))
    })


    if response.get('Item', {}).get('Expires', 0) < datetime.utcnow().timestamp():
        # Expired
        return False

    return True


def get_xsrf_token_generator(ip):
    def gen_xsrf_token(form_name):
        # Generate a random UUID to send to the user
        form_uuid = uuid4()
        # Save a copy mixed with the form name and IP of the request, this way,
        # we don't store the IP with the token, or the form it belongs to, but
        # ensure the form name and IP of the submission must also match. This
        # way we don't store user-identifying information, nor does a leak of
        # the DB result in usable data.
        save_xsrf_token(uuid5(uuid5(form_uuid, form_name), ip))

        return form_uuid

    return gen_xsrf_token
