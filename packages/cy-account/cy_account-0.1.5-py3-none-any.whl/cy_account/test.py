from cy_account import AccountAPI

if __name__ == '__main__':
    redis_cli = None
    accountAPI = AccountAPI(None, 'localhost:8080', '0')

    code = accountAPI.send_phone_code("13666666666")
    print(code)
    user = accountAPI.login_by_code("13666666666", code['result'])
    print(user)
    token = user['access_token']
    u1 = accountAPI.get_user(token)
    print(u1)
