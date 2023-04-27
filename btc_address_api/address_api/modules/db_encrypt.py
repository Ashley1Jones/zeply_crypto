import traceback
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets


class EncryptedBinaryField(models.CharField):
    """Encrypts incoming bytes and stores them as character array with the PBKDF2HMAC hash"""

    login_salt = secrets.token_hex(16).encode()

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=login_salt,
                     iterations=100000,
                     backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode()))

    fernet = Fernet(key)

    def from_db_value(self, value: str, expression, connection) -> bytes:
        print(f'Decrypting string: {value}')
        try:
            return EncryptedBinaryField.fernet.decrypt(value.encode())
        except Exception:
            traceback.print_exc()
            raise

    def get_prep_value(self, value: bytes) -> str:
        # storing data
        try:
            print(f'Encrypting data "{value}"')
            encrypted = EncryptedBinaryField.fernet.encrypt(value)
            print(f'Submitting {encrypted} of length {len(encrypted)} to db')
            return encrypted.decode()
        except Exception:
            traceback.print_exc()
            raise
