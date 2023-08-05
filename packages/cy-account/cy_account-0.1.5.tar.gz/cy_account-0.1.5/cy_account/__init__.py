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

    def __init__(self, redis_cli: redis.Redis, account_api_server, app_id):
        """
        获取用户信息的时候必须穿参数，不然会返回None
        """
        self.redis_cli = redis_cli
        self.account_api_server = account_api_server
        self.app_id = app_id
        self.serverForRequest = ServerForRequest(app_id=app_id)

    def get_user(self, token, auto_error=True):
        """
        通过token获取用户信息得到的数据是自己的数据，比较详细
        """
        user = self.__get_user_by_token(token)

        # if not uid and auto_error:
        #     raise HTTPException(status_code=401, detail="请登录")
        #
        # user = self.__get_user_for_cache(user_id=uid)

        if not user and auto_error:
            raise HTTPException(status_code=400, detail="用户不存在")

        return user

    def get_user_by_id(self, user_id, auto_error=True, has_detail=False):
        """
       通过user_id获取用户信息得到的数据是别人的数据，要去除一部分数据
       """
        user = self.__get_user_for_cache(user_id=user_id)

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

    def get_user_no_error(self, user_id=0, token=None):
        """
        不抛出异常的情况下返回用户信息
        """
        if user_id:
            return self.get_user_by_id(user_id, auto_error=False)
        if token:
            return self.get_user(token=token)
        return None

    def send_phone_code(self, phone):
        r = self.serverForRequest.post(self.account_api_server, path='/api/v1/users/code', query={'phone': phone})
        return r

    def login_by_code(self, phone, code):
        return self.serverForRequest.post(self.account_api_server, path='/api/v1/users/login',
                                          body={'phone': phone, 'code': code})

    def logout(self, token):
        return self.serverForRequest.post(self.account_api_server, path='/api/v1/users/logout', query={"token": token})

    def __get_user_info(self, user_id: int) -> UserInfo | None:
        """
        接口获取用户信息
        """
        d = self.serverForRequest.get(self.account_api_server, path=f'api/v1/users/{user_id}')
        # print('*******', type(d))
        if not d:
            return None

        return UserInfo(**d)

    def __get_user_for_cache(self, user_id):
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
            user = self.__get_user_info(user_id)
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

    def __get_user_by_token(self, token) -> UserInfo | None:
        if not token:
            return None
        user = self.serverForRequest.get(self.account_api_server, f"api/v1/users/token/{token}")
        if not user:
            return None
        return UserInfo(**user)

    def __get_secret_key(self):
        r = self.redis_cli.hget(CLIENT_AUTH_KEY, self.app_id)
        if r:
            return json.loads(r)['client_secret']
        else:
            raise Exception('核心代码出现异常：无法获取到解密的client_secret')


class ServerForRequest:

    def __init__(self, app_id):
        self.app_id = app_id

    def __get_url(self, server_name: str, path: str):
        if path.startswith('/'):
            url = f"http://{server_name}{path}"
        else:
            url = f"http://{server_name}/{path}"
        # print(url)
        return url

    def __get_header(self, ):

        app_id = self.app_id
        if not app_id:
            raise ValueError("APP_ID 错误，请在启动的时候完成初始化")

        return {
            'X-APP-ID': app_id,
            # 'X-Request-Id': thread_local.request_id
        }

    def __before(self, response):
        if response.status_code == 200:
            # print(response.content)
            if not response.content:
                return response.content

            return json.loads(response.content)
        else:
            detail = json.loads(response.content)['detail']
            # print(detail)
            raise HTTPException(status_code=response.status_code, detail=detail)

    def post(self, server_name: str, path: str, query: dict = None, body: dict = None):

        url = self.__get_url(server_name, path)
        # start_time = time.time()
        body_str = json.dumps(body) if body else None
        response = requests.post(url=url, params=query, data=body_str, headers=self.__get_header())

        return self.__before(response)

    def get(self, server_name: str, path: str, query: dict = None):
        url = self.__get_url(server_name, path)

        response = requests.get(url=url, params=query, headers=self.__get_header())
        return self.__before(response)

    def put(self, server_name: str, path: str, query: dict = None):
        url = self.__get_url(server_name, path)

        response = requests.put(url=url, params=query, headers=self.__get_header())
        return self.__before(response)

    def delete(self, server_name: str, path: str, query: dict = None):
        url = self.__get_url(server_name, path)

        response = requests.delete(url=url, params=query, headers=self.__get_header())
        return self.__before(response)
