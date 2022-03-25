import requests
import json

from arrival_test.utils.logger import Logger
from arrival_test.models.bear import Bear, BearsGroup


class AlaskaApiUtils:

    BASE_URL = 'http://localhost:8091/bear'

    @staticmethod
    def __parse_response(response_obj):
        status_code = response_obj.status_code
        try:
            response_data_from_json = response_obj.json()
            if isinstance(response_data_from_json, list):
                resp_data = BearsGroup(response_data_from_json)
            elif isinstance(response_data_from_json, dict):
                resp_data = Bear(**response_data_from_json)
            else:
                resp_data = response_data_from_json
        except json.decoder.JSONDecodeError:
            resp_data = response_obj.text

        return status_code, resp_data

    @staticmethod
    def create_bear(bear_data=None):
        Logger.info(f'Performing "POST" request with request body {bear_data}')
        if bear_data:
            response = requests.post(AlaskaApiUtils.BASE_URL, data=bear_data)
        else:
            response = requests.post(AlaskaApiUtils.BASE_URL)
        return AlaskaApiUtils.__parse_response(response)

    @staticmethod
    def get_all_bears():
        response = requests.get(AlaskaApiUtils.BASE_URL)
        return AlaskaApiUtils.__parse_response(response)
    
    @staticmethod
    def get_bear_by_id(bear_id):
        url = AlaskaApiUtils.BASE_URL + f'/{bear_id}'
        Logger.info(f'Performing "GET" request for url: {url}')
        response = requests.get(url)
        return AlaskaApiUtils.__parse_response(response)

    @staticmethod
    def update_bear_by_id(bear_id, new_bear_data):
        response = requests.put(AlaskaApiUtils.BASE_URL + f'/{bear_id}', data=new_bear_data)
        return AlaskaApiUtils.__parse_response(response)
    
    @staticmethod
    def delete_all_bears():
        response = requests.delete(AlaskaApiUtils.BASE_URL)
        return AlaskaApiUtils.__parse_response(response)
    
    @staticmethod
    def delete_bear_by_id(bear_id):
        response = requests.delete(AlaskaApiUtils.BASE_URL + f'/{bear_id}')
        return AlaskaApiUtils.__parse_response(response)
