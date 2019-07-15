import hashlib
import hmac
import logging


"""
    Slack creates a unique string for your app and shares it with you. Verify
    requests from Slack with confidence by verifying signatures using your
    signing secret.
    On each HTTP request that Slack sends, we add an X-Slack-Signature HTTP
    header. The signature is created by combining the signing secret with the
    body of the request we're sending using a standard HMAC-SHA256 keyed hash.
    https://api.slack.com/docs/verifying-requests-from-slack#how_to_make_a_request_signature_in_4_easy_steps__an_overview
    Args:
        signing_secret: Your application's signing secret, available in the
            Slack API dashboard
        data: The raw body of the incoming request - no headers, just the body.
        timestamp: from the 'X-Slack-Request-Timestamp' header
        signature: from the 'X-Slack-Signature' header - the calculated signature
            should match this.
    Returns:
        True if signatures matches
"""
   
def create_slack_signature(secret:str, timestamp, data)->str:
    req = str.encode('v0:' + str(timestamp) + ':') + str.encode(data)
    request_signature= 'v0='+hmac.new(
        str.encode(secret),
        req, hashlib.sha256
    ).hexdigest()
   
    return request_signature

def validate_slack_signature(signing_secret: str, data: str, timestamp: str, signature: str) -> bool:
    format_req = str.encode(f"v0:{timestamp}:{data}")
    encoded_secret = str.encode(signing_secret)
    request_hash = hmac.new(encoded_secret, format_req, hashlib.sha256).hexdigest()
    calculated_signature = f"v0={request_hash}"
    
    return hmac.compare_digest(calculated_signature, signature)

def validate_github_signature(signing_secret: str, data: str,signature: str) -> bool:
   format_req = str.encode(data)
   request_hash = hmac.new(signing_secret, format_req, hashlib.sha1).hexdigest()
   return hmac.compare_digest(request_hash,signature )
