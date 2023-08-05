__all__ = ["UserInfo", "AccountAPI", "ServerForRequest"]

from typing import Optional
from pydantic import BaseModel, ValidationError

import json
import requests
import redis as redis
from fastapi import HTTPException


class UserInfo(BaseModel):
    """
    user info 的基础模型
    """
    phone: Optional[str] = None
    nick_name: Optional[str] = None
    avatar: Optional[str] = None
    desc: Optional[str] = None
    background: Optional[str] = None
    gender: Optional[int] = 0  # 0不显示  1男 2女
    status: Optional[int] = 1  # 1正常 2冻结
    id: Optional[int] = None

    is_vip: Optional[bool] = False
    vip_end_time: Optional[str] = None
    vip_level: Optional[int] = 1
    points: Optional[int] = 0  # 积分


USER_INFO_CACHE_KEY = 'cy_account-user-info-for-core'
CLIENT_AUTH_KEY = 'account-api-client-auth-hash'


class AccountAPI:

    def __init__(self, redis_cli: redis.Redis):
        """
        获取用户信息的时候必须穿参数，不然会返回None
        """
        self.redis_cli = redis_cli

    def get_user(self, account_api_server, token, auto_error=True):
        """
        通过token获取用户信息得到的数据是自己的数据，比较详细
        """
        user = self.__get_user_by_token(account_api_server, token)

        # if not uid and auto_error:
        #     raise HTTPException(status_code=401, detail="请登录")
        #
        # user = self.__get_user_for_cache(user_id=uid)

        if not user and auto_error:
            raise HTTPException(status_code=400, detail="用户不存在")

        return user

    def get_user_by_id(self, account_api_server, user_id, auto_error=True, has_detail=False):
        """
       通过user_id获取用户信息得到的数据是别人的数据，要去除一部分数据
       """
        user = self.__get_user_for_cache(account_api_server, user_id=user_id)

        if not user and auto_error:
            raise HTTPException(status_code=400, detail="用户不存在")

        if not has_detail:
            user.is_vip = None
            user.vip_level = None
            user.vip_end_time = None
            user.points = None
            user.phone = None
            user.status = None
            user.desc = None
            user.background = None
        else:
            user.is_vip = None
            user.vip_level = None
            user.vip_end_time = None
            user.points = None

        return user

    def get_user_no_error(self, account_api_server, user_id=0, token=None):
        """
        不抛出异常的情况下返回用户信息
        """
        if user_id:
            return self.get_user_by_id(account_api_server, user_id, auto_error=False)
        if token:
            return self.get_user(account_api_server, token=token)
        return None

    @staticmethod
    def send_phone_code(account_api_server, phone):
        r = ServerForRequest.post(account_api_server, path='/api/v1/users/code', query={'phone': phone})
        return r

    @staticmethod
    def login_by_code(account_api_server, phone, code):
        return ServerForRequest.post(account_api_server, path='/api/v1/users/login',
                                     body={'phone': phone, 'code': code})

    @staticmethod
    def logout(account_api_server, token):
        return ServerForRequest.post(account_api_server, path='/api/v1/users/logout', query={"token": token})

    def __get_user_info(self, account_api_server, user_id: int) -> UserInfo | None:
        """
        接口获取用户信息
        """
        d = ServerForRequest.get(account_api_server, path=f'api/v1/users/{user_id}')
        # print('*******', type(d))
        if not d:
            return None

        return UserInfo(**d)

    def __get_user_for_cache(self, account_api_server, user_id):
        """
        缓存中获取用户信息
        """
        if not self.redis_cli:
            raise ValueError("self.redis_cli is None")

        u = self.redis_cli.hget(USER_INFO_CACHE_KEY, user_id)

        if u:
            d = json.loads(u)
            user = UserInfo(**d)
        else:
            # 接口获取
            user = self.__get_user_info(account_api_server, user_id)
        #
        # if user.status == 2:
        #     raise HTTPException(status_code=402, detail="账号已被冻结")
        return user

    #
    # def __get_user_by_token(self, token):
    #     if not token:
    #         return 0
    #     try:
    #         # todo 判断 token 是否有效，如无效则调用account账号验证
    #         payload = jwt.decode(
    #             token, self.__get_secret_key(settings.APP_ID), algorithms="HS256"
    #         )
    #     except (jwt.JWTError, ValidationError):
    #         traceback.print_exc()
    #         return 0
    #     user_id = payload['sub']
    #     return user_id

    def __get_user_by_token(self, account_api_server, token) -> UserInfo | None:
        if not token:
            return None
        user = ServerForRequest.get(account_api_server, f"api/v1/users/token/{token}")
        if not user:
            return None
        return UserInfo(**user)

    def __get_secret_key(self):
        r = self.redis_cli.hget(CLIENT_AUTH_KEY, ServerForRequest.APP_ID)
        if r:
            return json.loads(r)['client_secret']
        else:
            raise Exception('核心代码出现异常：无法获取到解密的client_secret')


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
