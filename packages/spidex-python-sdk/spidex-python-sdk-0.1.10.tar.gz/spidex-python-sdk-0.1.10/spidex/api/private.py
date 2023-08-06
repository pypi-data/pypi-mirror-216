import json
import re
import time
import requests
from spidex.constants import CREATE_API_KEY_URL, ORDER_URL, CANCEL_ORDER_URL, DEPOSIT_URL, DEPOSIT_MARGIN_URL, \
    QUERY_ORDERS_URL, QUERY_POSITION_URL, POOL_ADR,EIP712DOMAIN_DEPOSIT_MARGIN_CONTRACT,WITHDRAW_MARGIN_URL,QUERY_TRADES_URL,QUERY_TRANSFERS_URL,QUERY_ACCOUNT_URL,DELETE_API_KEY_URL,ONBOARDING_URL
from spidex.eth_sign.signers import signature_eip712,signature_eip712_DeriveKey
from spidex.eth_sign.eip712struct_entity import CreateAPIKey, Order, DepositToPool, DepositMargin,WithdrawMargin,DeleteAPIKey,Onboarding
from spidex.constants import EIP712DOMAIN_ORDER_CONTRACT
from decimal import Decimal, getcontext

def get_timestamp():
    return str(int(time.time() * 1000))

def onboarding(self, **kwargs):

    params = {**kwargs}
    derived_pub = signature_eip712_DeriveKey(self.wallet_secret)
    signature_params = {
        "method": 'POST',
        "requestPath": re.sub('rest', 'spidex/v1', ONBOARDING_URL),
                        }
    struct = Onboarding()
    for key, value in signature_params.items():
        struct[key] = value
    epi712_signature = signature_eip712(self.wallet_secret, struct)
    headers = {
        "SPIDEX-ADDRESS": params['maker_address'],
        "SPIDEX-SIGNATURE": epi712_signature,
    }
    url = self.host + ONBOARDING_URL
    response = requests.post(url,  headers=headers, json={'derived_pub': derived_pub})
    datas = {'order_result': 'success', 'datas': response.json()}
    return datas

def create_api_key(self, **kwargs):

    params = {**kwargs}
    time_stamp = get_timestamp()
    signature_params = {
        "method": 'POST',
        "requestPath": re.sub('rest', 'spidex/v1', CREATE_API_KEY_URL),
        'timestamp': time_stamp}
    struct = CreateAPIKey()
    for key, value in signature_params.items():
        struct[key] = value
    epi712_signature = signature_eip712(self.wallet_secret, struct)
    headers = {
        "SPIDEX-TIMESTAMP": time_stamp,
        "SPIDEX-ADDRESS": params['maker_address'],
        "SPIDEX-SIGNATURE": epi712_signature,
    }
    url = self.host + CREATE_API_KEY_URL
    response = requests.post(url,  headers=headers)
    datas = {'order_result': 'success', 'datas': response.json()}
    return datas

def delete_api_key(self, **kwargs):

    params = {**kwargs}
    time_stamp = get_timestamp()
    signature_params = {
        "method": 'DELETE',
        "requestPath": re.sub('rest', 'spidex/v1', DELETE_API_KEY_URL),
        'timestamp': time_stamp}
    struct = DeleteAPIKey()
    for key, value in signature_params.items():
        struct[key] = value
    epi712_signature = signature_eip712(self.wallet_secret, struct)
    headers = {
        "SPIDEX-TIMESTAMP": time_stamp,
        "SPIDEX-ADDRESS": params['maker_address'],
        "SPIDEX-SIGNATURE": epi712_signature,
    }
    url = self.host + DELETE_API_KEY_URL
    response = requests.delete(url,  headers=headers, json={'key': params['key']})
    if response.status_code==200:
        datas = {'order_result': 'success'}
    else:
        datas = {'order_result': 'fail', 'datas': response.json()}
    return datas


def order(self, **kwargs):

    signature_params = {**kwargs}
    struct = Order()
    for key, value in signature_params.items():
        if key == 'amount' or key == 'price':
            signature_params[key] = str(value)
            value = int(Decimal(str(value))*10**18)
            value = round(value, -10)
        if key == 'symbol':
            continue
        if key == 'side':
            value = 0 if signature_params['side'] == 'BUY' else 1
        if key == 'type':
            value = 0 if signature_params['type'] == 'LIMIT' else 1
        struct[key] = value

    epi712_signature = signature_eip712(self.wallet_secret, struct, EIP712DOMAIN_ORDER_CONTRACT)
    signature_params.update({"signature": epi712_signature})

    param_string, header = self.sign_deal_post_datas(signature_params, ORDER_URL)
    url = self.host + ORDER_URL
    response = requests.post(url, data=param_string, headers=header)
    datas = {'order_result': 'success', 'datas': response.json()}
    return datas


def cancel_order(self, **kwargs):

    params = {**kwargs}
    param_string, header = self.sign_deal_post_datas(params, CANCEL_ORDER_URL)
    url = self.host + CANCEL_ORDER_URL
    response = requests.post(url, data=param_string, headers=header)
    if response.status_code == 200:
        datas = {'order_result': 'success'}
    else:
        datas = {'order_result': 'fail'}
    return datas

def deposit_to_pool(self, pool_address, signer, amount):

    struct = DepositToPool()
    struct['poolAddress'] = pool_address
    struct['amount'] = int(amount * 1E18)
    epi712_signature = signature_eip712(self.wallet_secret, struct, EIP712DOMAIN_ORDER_CONTRACT)
    params = {
        'pool_address': pool_address,
        'signer': signer,
        'amount': str(amount),
        'signature': epi712_signature,
    }

    param_string, header = self.sign_deal_post_datas(params, DEPOSIT_URL)
    url = self.host + DEPOSIT_URL
    response = requests.post(url, data=param_string, headers=header)

    datas = {'order_result': 'success', 'datas': response.json()}
    return datas

def deposit_margin(self,**kwargs):

    deposit_params = {**kwargs}
    struct = DepositMargin()
    for key, value in deposit_params.items():
        if key == 'amount':
            deposit_params[key] = str(value)
            value = int(value*1E6)
        if key == 'symbol':
            continue
        struct[key] = value
    epi712_signature = signature_eip712(self.wallet_secret, struct, EIP712DOMAIN_DEPOSIT_MARGIN_CONTRACT)
    deposit_params.pop('spec')
    deposit_params.update({'signature': epi712_signature})
    param_string, header = self.sign_deal_post_datas(deposit_params, DEPOSIT_MARGIN_URL)
    url = self.host + DEPOSIT_MARGIN_URL
    response = requests.post(url, data=param_string, headers=header)

    datas = {'order_result': 'success', 'datas': response.json()}
    return datas

def withdraw_margin(self,**kwargs):

    deposit_params = {**kwargs}
    struct = WithdrawMargin()
    for key, value in deposit_params.items():
        if key == 'amount':
            deposit_params[key] = str(value)
            value = int(value*1E6)
        if key == 'symbol':
            continue
        struct[key] = value
    epi712_signature = signature_eip712(self.wallet_secret, struct, EIP712DOMAIN_DEPOSIT_MARGIN_CONTRACT)
    deposit_params.pop('spec')
    deposit_params.update({'signature': epi712_signature})
    param_string, header = self.sign_deal_post_datas(deposit_params, WITHDRAW_MARGIN_URL)
    url = self.host + WITHDRAW_MARGIN_URL
    response = requests.post(url, data=param_string, headers=header)

    datas = {'order_result': 'success', 'datas': response.json()}
    return datas

def get_orders(self, **kwargs):

    params = {**kwargs}
    return self.sign_request('GET', QUERY_ORDERS_URL, params)


def get_position(self,**kwargs):

    params = {**kwargs}
    return self.sign_request('GET', QUERY_POSITION_URL, params)

def get_trades(self,**kwargs):

    params = {**kwargs}
    return self.sign_request('GET', QUERY_TRADES_URL, params)

def get_transfers(self,**kwargs):

    params = {**kwargs}
    return self.sign_request('GET', QUERY_TRANSFERS_URL, params)

def get_account(self):

    return self.sign_request('GET', QUERY_ACCOUNT_URL)


