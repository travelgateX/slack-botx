import json
import hashlib
import hmac
import pytest


def create_signature(secret, timestamp, data):
    req = str.encode('v0:' + str(timestamp) + ':') + str.encode(data)
    request_signature= 'v0='+hmac.new(
        str.encode(secret),
        req, hashlib.sha256
    ).hexdigest()
    return request_signature