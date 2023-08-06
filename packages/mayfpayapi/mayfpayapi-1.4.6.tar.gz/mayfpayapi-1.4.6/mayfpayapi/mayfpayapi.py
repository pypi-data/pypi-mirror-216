import time
import hashlib
import hmac
import json
import requests

class KassaAPI:
    def __init__(self, api_token, public_key, secret_key, kassa_id):
        self.api_token = api_token
        self.public_key = public_key
        self.secret_key = secret_key
        self.kassa_id = kassa_id
        self.base_url = 'https://mayfpay.top/api/v1/'

    def _generate_headers(self, payload_str):
        timestamp = str(time.time())
        XApiSignature = hmac.new(self.secret_key.encode(), payload_str.encode(), hashlib.sha256).hexdigest()
        headers = {
            'timestamp': timestamp,
            'x-api-public-key': self.public_key,
            'x-api-signature': XApiSignature,
        }
        return headers

    def _post_request(self, endpoint, params):
        payload_str = json.dumps(params)
        headers = self._generate_headers(payload_str)
        r = requests.post(url=endpoint, data=params, headers=headers)
        return r.json()

    def _get_request(self, endpoint, params):
        payload_str = json.dumps(params)
        headers = self._generate_headers(payload_str)
        r = requests.get(endpoint, params=params, headers=headers)
        return r.json()


    def create_invoice(self, pay_method_id, amount, order_id,
                sub_pay_method_id=None,expire_invoice=None, en=None, comment=None, data=None):

        self.order_id = order_id
        self.expire_invoice = expire_invoice
        self.en = en
        self.comment = comment
        self.data = data
        self.pay_method_id = pay_method_id
        self.sub_pay_method_id = sub_pay_method_id
        self.amount = amount    


        params = {
            'order_id': self.order_id,
            'api_token': self.api_token,
            'kassa_id': self.kassa_id,
            'PayMethodId': self.pay_method_id,
            'amount': self.amount,
        }
        if self.sub_pay_method_id:
            params.update({'SubPayMethodId': self.sub_pay_method_id})
        if self.expire_invoice:
            params.update({'expire_invoice': self.expire_invoice})
        if self.en:
            params.update({'en': self.en})
        if self.comment:
            params.update({'comment': self.comment})
        if self.data:
            params.update({'data': self.data})

        return self._post_request(f'{self.base_url}kassa/invoice/create', params)

    def get_balance(self):
        params = {
            'api_token': self.api_token,
            'kassa_id': self.kassa_id,
        }

        return self._get_request(f'{self.base_url}kassa/balance', params)

    def check_invoice(self, order_id):
        params = {
            'order_id': order_id,
            'api_token': self.api_token,
        }

        return self._get_request(f'{self.base_url}kassa/invoice/check', params)
 

 
class WalletAPI:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = 'https://mayfpay.top/api/v1/'

    def _post_request(self, endpoint, params):
        r = requests.post(url=endpoint, data=params)
        return r.json()

    def _get_request(self, endpoint, params):
        r = requests.get(endpoint, params=params)
        return r.json()

    def wallet_balance(self):
        params = {
            'api_token': self.api_token,
        }

        return self._get_request(f'{self.base_url}wallet', params)

    def wallet_transfer(self, wallet_service, method, fee_type, amount, call_back_url=None, kassa_id=None, extra_wallet_service=None):
        params = {
            'api_token': self.api_token,
            'amount': amount,
            'method': method,
            'fee_type': fee_type,
            'wallet_service': wallet_service,
        }
        if call_back_url:
            params.update({'call_back_url': call_back_url})
        if kassa_id:
            params.update({'kassa_id': kassa_id})
        if extra_wallet_service:
            params.update({'extra_wallet_service': extra_wallet_service})

        return self._post_request(f'{self.base_url}wallet/transfer/create', params)

    def wallet_transfer_check(self, id):
        params = {
            'api_token': self.api_token,
            'id': id,
        }
        return self._post_request(f'{self.base_url}wallet/transfer/check', params)


