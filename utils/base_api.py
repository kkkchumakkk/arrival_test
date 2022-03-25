import requests

from arrival_test.utils.logger import Logger


class RestApiClient:

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.session = requests.Session()

    def __send_request(self, method, endpoint,  data=None):
        if data:
            request = requests.Request(method=method, url=endpoint, data=data)
        else:
            request = requests.Request(method=method, url=endpoint)
        return self.session.send(request.prepare())

    def get(self, url):
        Logger.info(f'Performing "GET" request for url {url}')
        return self.__send_request('GET', url)

    def post(self, url, data):
        Logger.info(f'Performing "POST" request for url {url} with json {data}')
        return self.__send_request('POST', url, data)

    def put(self, url, data):
        Logger.info(f'Performing "PUT" request for url: {url} and json {data}')
        return self.__send_request('PUT', url, data)

    def delete(self, url):
        Logger.info(f'Performing "DELETE" request for url: {url}')
        return self.__send_request('DELETE', url)
