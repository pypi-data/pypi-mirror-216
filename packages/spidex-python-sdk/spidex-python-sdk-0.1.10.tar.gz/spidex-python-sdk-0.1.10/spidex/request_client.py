import re
import time

from spidex.constants import DEFAULT_API_TIMEOUT
from spidex.error import ClientError, ServerError
from spidex.lib.utils import cleanNoneValue, encoded_string, check_required_parameter
from spidex.constants import ORDER_URL, CANCEL_ORDER_URL
import json
import base64
from json import JSONDecodeError
import hmac
import hashlib
import json
import requests


class Client(object):
    def __init__(self, key=None, secret=None, phrase=None, wallet_secret=None, host=None, api_timeout=DEFAULT_API_TIMEOUT,
                 show_header=False):

        self.key = key
        self.secret = secret
        self.phrase = phrase
        self.wallet_secret = wallet_secret
        self.host = host
        self.show_header = show_header
        self.api_timeout = api_timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "SPIDEX-API-KEY": key,
                "SPIDEX-PASSPHRASE": phrase,
            }
        )

    def get_timestamp(self):
        return str(int(time.time() * 1000))

    def query(self, url_path, payload=None):
        return self.send_request("GET", url_path, payload=payload)

    def post(self, url_path, payload=None, headers=None):
        self.session.headers = headers
        return self.send_request("POST", url_path, payload=payload)

    def sign_deal_post_datas(self, payload, params_URL):
        time_stamp = self.get_timestamp()
        param_string = json.dumps(payload)
        params_URL = re.sub('rest', 'spidex/v1', params_URL)
        message = time_stamp + 'POST' + params_URL + param_string
        base64_decrypt = base64.b64decode(self.secret.encode('utf-8'))
        m = hmac.new(base64_decrypt, message.encode("utf-8"), hashlib.sha256).digest()
        signature = str(base64.b64encode(m), 'utf-8')
        header = {}
        header.update({
            "Content-Type": "application/json;charset=utf-8",
            "SPIDEX-API-KEY": self.key,
            "SPIDEX-PASSPHRASE": self.phrase,
            'SPIDEX-TIMESTAMP': time_stamp,
            'SPIDEX-SIGNATURE': signature
        })
        return param_string, header

    def sign_request(self, http_method, url_path, payload=None):
        if payload is None:
            payload = {}
        time_stamp = self.get_timestamp()

        if http_method == 'GET':
            param_string = '?' + self.prepare_params(payload)
        else:
            param_string = json.dumps(payload)
        params_URL = re.sub('rest', 'spidex/v1', url_path)
        if payload =={}:
            message = time_stamp + http_method + params_URL
        else:
            message = time_stamp + http_method + params_URL + param_string
        signature = self.get_sign(message)
        self.session.headers.update({
            'SPIDEX-TIMESTAMP': time_stamp,
            'SPIDEX-SIGNATURE': signature
        })
        return self.send_request(http_method, url_path, payload)

    def send_request(self, http_method, url_path, payload=None):
        if payload is None:
            payload = {}
        url = self.host + url_path
        if http_method == 'GET':
            params = cleanNoneValue(
                {
                    "url": url,
                    "params": self.prepare_params(payload),
                    "timeout": self.api_timeout,
                }
            )
        elif http_method == 'POST':
            params = cleanNoneValue(
                {
                    "url": url,
                    "json": payload,
                    "timeout": self.api_timeout,
                }
            )
        response = self.dispatch_request(http_method)(**params)
        print(response.content)
        self.handle_exception(response)
        try:
            if url_path in [CANCEL_ORDER_URL, ORDER_URL] and response.status_code == 200:
                return {'order_result': 'success', 'datas': response.json()}
            else:
                data = response.json()
        except ValueError:
            data = response.text
        result = {}
        if self.show_header:
            result["header"] = response.headers

        if len(result) != 0:
            result["data"] = data
            return result
        return data

    def prepare_params(self, params):
        return encoded_string(cleanNoneValue(params))

    def get_sign(self, data):
        base64_decrypt = base64.b64decode(self.secret.encode('utf-8'))
        m = hmac.new(base64_decrypt, data.encode("utf-8"), hashlib.sha256).digest()
        return str(base64.b64encode(m), 'utf-8')

    def dispatch_request(self, http_method):
        return {
            "GET": self.session.get,
            "POST": self.session.post,
        }.get(http_method, "GET")

    def handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, None, response.text, response.headers)
            raise ClientError(status_code, err["code"], err["msg"], response.headers)
        raise ServerError(status_code, response.text)
