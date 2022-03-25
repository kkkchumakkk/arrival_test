import json

from arrival_test.models.bear import Bear, BearsGroup
from arrival_test.utils.base_api import RestApiClient


class BearApiClient(RestApiClient):
    """
    Class for working with Alaska API
    """

    @staticmethod
    def __parse_response(response_obj):
        """
        Method that parses response content in required format
        @return: BearGroup instance if response content contains json and content can be deserialized into python list
                 Bear instance if response content contains json and content can be deserialized into python dict
                 string otherwise

        @param response_obj: response object that was received after performing request

        """
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

    def create_bear(self, bear_data=None):
        """
        Method to create a bear record in

        @return: status code and parsed response content

        @param bear_data(optional): instance of Bear class or None
        """
        data = bear_data.json_repr() if bear_data else None
        response = self.post(self.endpoint, data)
        return BearApiClient.__parse_response(response)

    def delete_all_bears(self):
        """
        Method to delete all bears from DB

        @return: status code and parsed response content
        """
        response = self.delete(self.endpoint)
        return BearApiClient.__parse_response(response)

    def delete_bear_by_id(self, bear_id):
        """
        Method to delete specific bear by id

        @return: status code and parsed response content

        @param bear_id: integer that represents bear id
        """
        response = self.delete(self.endpoint + f'/{bear_id}')
        return BearApiClient.__parse_response(response)

    def get_all_bears(self):
        """
        Method to get all records from DB

        @return: status code and parsed response content
        """
        response = self.get(self.endpoint)
        return BearApiClient.__parse_response(response)

    def get_bear_by_id(self, bear_id):
        """
        Method to get specific bear by id

        @return: status code and parsed response content

        @param bear_id: integer that represents bear id
        """
        response = self.get(self.endpoint + f'/{bear_id}')
        return BearApiClient.__parse_response(response)

    def update_bear_by_id(self, bear_id, new_bear_data):
        """
        Method to update specific bear by id

        @return: status code and parsed response content

        @param bear_id: integer that represents bear id
        @new_bear_data(optional): instance of Bear class
        """
        response = self.put(self.endpoint + f'/{bear_id}', data=new_bear_data.json_repr())
        return BearApiClient.__parse_response(response)
