from rest_framework import serializers
from .models import CryptoAddresses


class CryptoInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CryptoAddresses
        fields = ('private_key', 'public_key', 'currency', 'address', 'id')

