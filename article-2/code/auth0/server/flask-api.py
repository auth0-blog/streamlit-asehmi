"""Python Flask API Auth0 integration example
"""

from functools import wraps
import json
from os import environ as env
import sys
from typing import Dict
import time

from six.moves.urllib.request import urlopen

from dotenv import load_dotenv, find_dotenv
import flask
from flask import Flask, jsonify, _request_ctx_stack, Response
from flask_cors import cross_origin
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
API_AUDIENCE = env.get("API_AUDIENCE")
ALGORITHMS = ["RS256"]
APP = Flask(__name__)


# Format error response and append status code.
class AuthError(Exception):
    """
    An AuthError is raised whenever the authentication failed.
    """
    def __init__(self, error: Dict[str, str], status_code: int):
        super().__init__()
        self.error = error
        self.status_code = status_code

LAST_REQUEST_SEC = 0
@APP.before_request
def update_last_request_ms():
    global LAST_REQUEST_SEC
    LAST_REQUEST_SEC = time.time()

@APP.after_request
def after_request(response):
    # If the request comes from a sandboxed iframe, the origin will be
    # the string "null", which is not covered by the "*" wildcard.
    # To handle this, we set "Access-Control-Allow-Origin: null".
    response.headers.add(
        "Access-Control-Allow-Origin",
        "null" if flask.request.origin == "null" else "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

@APP.errorhandler(AuthError)
def handle_auth_error(ex: AuthError) -> Response:
    """
    serializes the given AuthError as json and sets the response status code accordingly.
    :param ex: an auth error
    :return: json serialized ex response
    """
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header() -> str:
    """Obtains the access token from the Authorization Header
    """
    auth = flask.request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                            "Authorization header must start with "
                            "Bearer"}, 401)
    if len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    if len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                            "Authorization header must be "
                            "Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope: str) -> bool:
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def requires_auth(func):
    """Determines if the access token is valid
    """
    
    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        url = "https://" + AUTH0_DOMAIN + "/.well-known/jwks.json"
        jsonurl = urlopen(url)
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError as jwt_error:
            raise AuthError({"code": "invalid_header",
                             "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, 401) from jwt_error
        if unverified_header["alg"] == "HS256":
            raise AuthError({"code": "invalid_header",
                             "description":
                                "Invalid header. "
                                "Use an RS256 signed JWT Access Token"}, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )
            except jwt.ExpiredSignatureError as expired_sign_error:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401) from expired_sign_error
            except jwt.JWTClaimsError as jwt_claims_error:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                    "incorrect claims, "
                                    "please check the audience and issuer"}, 401) from jwt_claims_error
            except Exception as exc:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                    "Unable to parse authentication "
                                    "token."}, 401) from exc

            _request_ctx_stack.top.current_user = payload
            return func(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    return decorated


# Controllers API
@APP.route("/api/ping", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def ping():
    """No access token required to access this route
    """
    result = {'data': f'Hello from a PUBLIC endpoint! {time.asctime(time.localtime(LAST_REQUEST_SEC))}'}
    return result


@APP.route("/api/pong", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3001, http://localhost:4010"])
@requires_auth
def pong():
    """A valid access token is required to access this route
    """
    auth = flask.request.headers.get("Authorization", None)
    if auth:
        bearer = auth.split(' ')
        if ('Bearer' in bearer) and not ('null' in bearer):
            result = {'data': f'Hello from a SECURE endpoint! {time.asctime(time.localtime(LAST_REQUEST_SEC))}'}
        else:
           result = {"error": "Authentication token is null! Please log in."}
    else:
        result = {"error": "Authentication token not available or expired! Please log in."}

    return result


@APP.route("/api/pong-scoped", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:3001, http://localhost:4010"])
@requires_auth
def pong_scoped():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:messages"):
        result = {'data': "Hello from a private endpoint! "
                          "You need to be authenticated and have a scope of read:messages to see this."}
        return result
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


if __name__ == '__main__':
    PORT = 8888
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    elif env.get("PORT", None):
        PORT=env.get("PORT")

    APP.run(host="0.0.0.0", port=PORT, use_reloader=False)

