import requests
import json

from arrival_test.utils.logger import Logger
from arrival_test.test_data.urls import ApiUrls


class AlaskaApiUtils:

    RESPONSE_RESULT_KEYS = ['Status code', 'Response text']

    @staticmethod
    def __get_url(bear_id=None):
        return ApiUrls.BASE_URL + f'/{bear_id}' if bear_id else ApiUrls.BASE_URL
    
    @staticmethod
    def __parse_response(response_obj):
        status_code = response_obj.status_code
        try:
            resp_data = response_obj.json()
        except json.decoder.JSONDecodeError:
            resp_data = response_obj.text

        return status_code, resp_data

    @staticmethod
    def create_bear(bear_data=None):
        Logger.info(f'Performing "POST" request with request body {bear_data}')
        if bear_data:
            response = requests.post(AlaskaApiUtils.__get_url(), data=json.dumps(bear_data))
        else:
            response = requests.post(AlaskaApiUtils.__get_url())
        return AlaskaApiUtils.__parse_response(response)

    @staticmethod
    def get_all_bears():
        response = requests.get(AlaskaApiUtils.__get_url())
        return AlaskaApiUtils.__parse_response(response)
    
    @staticmethod
    def get_bear_by_id(bear_id):
        Logger.info(f'Performing "GET" request')
        response = requests.get(AlaskaApiUtils.__get_url(bear_id))
        return AlaskaApiUtils.__parse_response(response)

    @staticmethod
    def update_bear_by_id(bear_id, new_bear_data):
        response = requests.put(AlaskaApiUtils.__get_url(bear_id), data=json.dumps(new_bear_data))
        return AlaskaApiUtils.__parse_response(response)
    
    @staticmethod
    def delete_all_bears():
        response = requests.delete(AlaskaApiUtils.__get_url())
        return AlaskaApiUtils.__parse_response(response)
    
    @staticmethod
    def delete_bear_by_id(bear_id):
        response = requests.delete(AlaskaApiUtils.__get_url(bear_id))
        return AlaskaApiUtils.__parse_response(response)

    @staticmethod
    def get_app_info():
        response = requests.delete(ApiUrls.INFO_URL)
        return AlaskaApiUtils.__parse_response(response)