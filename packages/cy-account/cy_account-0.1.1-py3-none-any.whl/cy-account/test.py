from account_api import AccountAPI
from cy_request import ServerForRequest

if __name__ == '__main__':
    redis_cli = None
    ServerForRequest.set_app_id('0')

    code = AccountAPI.send_phone_code("localhost:8080", "13666666666")
    print(code)
    user = AccountAPI.login_by_code("localhost:8080", "13666666666", code['result'])
    print(user)
    token = user['access_token']
    u1 = AccountAPI(redis_cli).get_user("localhost:8080", token)
    print(u1)
