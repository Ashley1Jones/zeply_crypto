import binascii
import dataclasses
import secrets
import hashlib
import base58
import ecdsa
import eth_keys
import eth_utils


@dataclasses.dataclass
class CryptoWalletDetails:
    currency: str
    private_key: bytes
    public_key: bytes
    address: str


def generate_keys(crypto_code: str,
                  ) -> CryptoWalletDetails:
    print(f'Generating keys for currency: {crypto_code}')

    match crypto_code:
        case 'BTC':
            wallet = generate_bitcoin()
        case 'ETH':
            wallet = generate_eth()

        # case: add more currencies

        case _:
            raise NotImplementedError(
                f'Currency with code {crypto_code}'
                f' not implemented yet.'
                f'Please try BTC, or ETH')

    return wallet


def generate_bitcoin() -> CryptoWalletDetails:
    # example taken from:
    # https://burakcanekici.medium.com/bitcoin-address-generation-on-python-e267df5ff3a3

    ecdsa_private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    ecdsa_public_key = '04' + ecdsa_private_key.get_verifying_key().to_string().hex()
    public_key_hash = hashlib.sha256(binascii.unhexlify(ecdsa_public_key)).hexdigest()
    ridemp_from_hash = hashlib.new('ripemd160', binascii.unhexlify(public_key_hash))
    prepend_network_byte = '00' + ridemp_from_hash.hexdigest()
    iterated_hash = prepend_network_byte
    for x in range(1, 3):
        iterated_hash = hashlib.sha256(binascii.unhexlify(iterated_hash)).hexdigest()

    checksum = iterated_hash[:8]
    checksum_appended = prepend_network_byte + checksum
    bitcoin_address = base58.b58encode(binascii.unhexlify(checksum_appended))
    return CryptoWalletDetails(
        'BTC', ecdsa_private_key.to_string(), ecdsa_public_key.encode(), bitcoin_address.decode())


def generate_eth() -> CryptoWalletDetails:
    # code used for the following
    # https://stackoverflow.com/questions/51945714/how-do-i-generate-an-ethereum-public-key-from-a-known-private-key-using-python

    private_key = '0x' + secrets.token_hex(32)
    private_key_bytes = eth_utils.decode_hex(private_key)
    private_key_obj = eth_keys.keys.PrivateKey(private_key_bytes)
    public_key = private_key_obj.public_key
    address = public_key.to_checksum_address()
    return CryptoWalletDetails(
        'ETH', private_key_bytes, public_key.to_bytes(), address)

