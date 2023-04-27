import traceback
from django.http import HttpResponseBadRequest, HttpResponseServerError
from .serializers import CryptoInfoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CryptoAddresses
from .modules import address_generators


class CryptoViewSet(viewsets.ModelViewSet):
    """
    Generate model view set that will make all the REST api calls. The only custom REST api call is the post
    which will take a cryptocurrency code and generate the proper keys and address
    """
    queryset = CryptoAddresses.objects.all().order_by('id')
    serializer_class = CryptoInfoSerializer

    @action(detail=False, methods=['post'])
    def generate_address(self, request):
        # Get the cryptocurrency from the request data
        crypto_code = request.data.get('currency')
        try:
            wallet = address_generators.generate_keys(crypto_code)
            print(f'Saving wallet {wallet}')
            saved_row = CryptoAddresses.objects.create(
                currency=crypto_code, address=wallet.address, private_key=wallet.private_key,
                public_key=wallet.public_key)

        except NotImplementedError:
            return HttpResponseBadRequest(f'There is only support for BTC and ETH right now')
        except Exception as e:
            formatted_exception = traceback.format_exc()
            print(f'Failed to generate key because of {formatted_exception}')
            return HttpResponseServerError(formatted_exception)

        return Response({'address': wallet.address, 'id': saved_row.id})


