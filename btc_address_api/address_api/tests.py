from django.test import TestCase, TransactionTestCase
from rest_framework.test import RequestsClient
from django.urls import reverse
import web3
import web3.utils
import web3.eth
from web3 import Web3
from rest_framework.response import Response


BASE_URL = 'http://localhost:8000'


def make_generate_address_request(code: str):
    client = RequestsClient()
    url = '/Crypto_Address_Table/generate_address/'
    end_point = BASE_URL + url
    response = client.post(
        end_point, data={'currency': code})
    print(f'Response for generating address {response.json()}')
    return response


class TestGenerateKey(TransactionTestCase):
    def test_generate_bitcoin_address(self):
        """
         Generate bitcoin address and check that is valid with TODO: check bitcoin is valid
        """
        response = make_generate_address_request('BTC')
        self.assertEqual(response.status_code, 200)

    def test_generate_eth_address(self):
        """
        Generate ethereum address and checks that is valid with web3 library
        """
        response = make_generate_address_request('ETH')
        self.assertEqual(response.status_code, 200)
        address = response.json()['address']
        self.assertTrue(Web3().is_address(address))

    def test_get_address(self):
        """
        First generates 10 addresses then grabs the 10th address
        """
        n_generations = 10
        for _ in range(n_generations):
            response = make_generate_address_request('BTC')
            self.assertEqual(response.status_code, 200)

        client = RequestsClient()
        url = '/Crypto_Address_Table/'
        end_point = BASE_URL + url + str(n_generations)
        response = client.get(end_point)
        print(f'Got response with getting addresses {response.json()}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], n_generations)

    def test_list_addresses(self):
        """
        This first generates a list of addresses. These addresses will only exist in the temporary test database
        that django creates, so we create them here.
        """
        n_generations = 10
        for _ in range(n_generations):
            response = make_generate_address_request('BTC')
            self.assertEqual(response.status_code, 200)

        client = RequestsClient()
        url = '/Crypto_Address_Table/'
        end_point = BASE_URL + url
        response = client.get(
            end_point
        )
        print(f'Response for listing address {response.json()}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), n_generations)
