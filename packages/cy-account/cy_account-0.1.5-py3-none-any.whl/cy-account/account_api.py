import json

import redis as redis
from fastapi import HTTPException
from cy_request import ServerForRequest
from user_info import UserInfo

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

    def __get_user_info(self, account_api_server, user_id: int) -> UserInfo:
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
