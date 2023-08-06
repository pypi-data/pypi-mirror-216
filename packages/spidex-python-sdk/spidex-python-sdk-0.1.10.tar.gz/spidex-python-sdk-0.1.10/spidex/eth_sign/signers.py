import web3

from eip712_structs import EIP712Struct, make_domain
from eth_utils import big_endian_to_int
from coincurve import PrivateKey
from spidex.constants import EIP712DOMAIN_NAME, EIP712DOMAIN_VERSION, EIP712DoMAIN_CHAINID

# keccak_hash = lambda x: sha3.keccak_256(x).digest()
keccak_hash = lambda x: web3.Web3.keccak(x)


def signature_eip712(wallet_secret, entity_eip721struct: EIP712Struct, verifying_contract=None):
    my_domain = make_domain(name=EIP712DOMAIN_NAME,
                            version=EIP712DOMAIN_VERSION,
                            chainId=EIP712DoMAIN_CHAINID,
                            verifyingContract=verifying_contract)
    signature_bytes = entity_eip721struct.signable_bytes(my_domain)
    pk = PrivateKey.from_hex(wallet_secret)
    signature = pk.sign_recoverable(signature_bytes, hasher=keccak_hash)
    v = signature[64] + 27
    r = big_endian_to_int(signature[0:32])
    s = big_endian_to_int(signature[32:64])

    eip712_sign = r.to_bytes(32, 'big') + s.to_bytes(32, 'big') + v.to_bytes(1, 'big')
    return eip712_sign.hex()


def signature_eip712_DeriveKey(wallet_secret):
    pk = PrivateKey.from_hex(wallet_secret)
    pubKey = pk.public_key.format(compressed=True).hex()
    return pubKey