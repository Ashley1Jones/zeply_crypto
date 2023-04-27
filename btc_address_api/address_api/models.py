from django.db import models
from .modules import db_encrypt


class CryptoAddresses(models.Model):
    """Table for storing keys """
    private_key = db_encrypt.EncryptedBinaryField(max_length=200)
    public_key = models.BinaryField(max_length=200)
    currency = models.CharField(max_length=3)
    address = models.CharField(max_length=200)
    id = models.AutoField(primary_key=True)

