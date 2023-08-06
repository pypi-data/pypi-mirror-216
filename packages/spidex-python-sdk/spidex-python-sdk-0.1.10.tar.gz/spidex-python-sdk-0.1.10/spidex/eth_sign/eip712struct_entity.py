from eip712_structs import EIP712Struct, Address, Uint, Bytes, String

class Onboarding(EIP712Struct):
    method = String()
    requestPath = String()

class CreateAPIKey(EIP712Struct):
    method = String()
    requestPath = String()
    timestamp = String()

class DeleteAPIKey(EIP712Struct):
    method = String()
    requestPath = String()
    timestamp = String()


class Order(EIP712Struct):
    maker_address = Address()
    pool_address = Address()
    spec = Bytes(32)
    side = Uint(8)
    type = Uint(8)
    price = Uint(256)
    amount = Uint(256)
    salt = Uint(256)
    expiration = Uint(256)


class DepositToPool(EIP712Struct):
    poolAddress = Address()
    amount = Uint(256)


class DepositMargin(EIP712Struct):
    spec = Bytes(32)
    pos_address = Address()
    amount = Uint(256)
    salt = Uint(256)


class WithdrawMargin(EIP712Struct):
    spec = Bytes(32)
    pos_address = Address()
    amount = Uint(256)
    salt = Uint(256)