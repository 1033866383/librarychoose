import jwt

headers = {
    'alg': "HS256",  # 声明所使用的算法
}


def generate_jwt(token_dict, secret="system_create_is_fbz", algorithm="HS256", headers=headers):
    return jwt.encode(token_dict,
                      secret,
                      algorithm,
                      headers)


def verify_jwt(token, secret="system_create_is_fbz", algorithm="HS256"):
    return jwt.decode(token, secret, algorithm)


if __name__ == '__main__':
    token = generate_jwt({"username": "fanbozhowwu"})
    print(token)
    res = verify_jwt(token)
    print(res)
