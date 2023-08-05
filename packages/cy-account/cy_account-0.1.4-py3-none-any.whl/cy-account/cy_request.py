import json

from fastapi import HTTPException
import requests


class ServerForRequest:
    APP_ID = 0

    @staticmethod
    def set_app_id(app_id: int):
        ServerForRequest.APP_ID = app_id

    @staticmethod
    def __get_url(server_name: str, path: str):
        if path.startswith('/'):
            url = f"http://{server_name}{path}"
        else:
            url = f"http://{server_name}/{path}"
        # print(url)
        return url

    @staticmethod
    def __get_header():
        return {
            'X-APP-ID': ServerForRequest.APP_ID,
            # 'X-Request-Id': thread_local.request_id
        }

    @staticmethod
    def __before(response):
        if response.status_code == 200:
            # print(response.content)
            if not response.content:
                return response.content

            return json.loads(response.content)
        else:
            detail = json.loads(response.content)['detail']
            # print(detail)
            raise HTTPException(status_code=response.status_code, detail=detail)

    @staticmethod
    def post(server_name: str, path: str, query: dict = None, body: dict = None):

        url = ServerForRequest.__get_url(server_name, path)
        # start_time = time.time()
        body_str = json.dumps(body) if body else None
        response = requests.post(url=url, params=query, data=body_str, headers=ServerForRequest.__get_header())

        return ServerForRequest.__before(response)

    @staticmethod
    def get(server_name: str, path: str, query: dict = None):
        url = ServerForRequest.__get_url(server_name, path)

        response = requests.get(url=url, params=query, headers=ServerForRequest.__get_header())
        return ServerForRequest.__before(response)

    @staticmethod
    def put(server_name: str, path: str, query: dict = None):
        url = ServerForRequest.__get_url(server_name, path)

        response = requests.put(url=url, params=query, headers=ServerForRequest.__get_header())
        return ServerForRequest.__before(response)

    @staticmethod
    def delete(server_name: str, path: str, query: dict = None):
        url = ServerForRequest.__get_url(server_name, path)

        response = requests.delete(url=url, params=query, headers=ServerForRequest.__get_header())
        return ServerForRequest.__before(response)
