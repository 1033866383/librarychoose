import time
from datetime import datetime, timedelta

import jwt
from flask import current_app

headers = {
    'alg': "HS256",  # 声明所使用的算法
}


def generate_jwt(token_dict, secret="system_create_is_fbz", algorithm="HS256", headers=headers):
    time_now = datetime.now()
    end_time = (time_now + timedelta(days=3)).strftime("%Y-%m-%d 00:00:00")
    end_time = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
    token_dict["end_time"] = end_time
    return jwt.encode(token_dict,
                      secret,
                      algorithm,
                      headers)


def verify_jwt(token, secret="system_create_is_fbz", algorithm="HS256"):
    token_dict = jwt.decode(token, secret, algorithm)
    time_now = datetime.now()
    time_now = time.mktime(time.strptime(time_now.strftime("%Y-%m-%d %H:%M:%S"), '%Y-%m-%d %H:%M:%S'))
    if token_dict.get("end_time", 0) > time_now:
        current_app.logger.info("token info {0}".format(token_dict))
        return token_dict
    else:
        return None


if __name__ == '__main__':
    token = generate_jwt({"username": "fanbozhowwu"})
    print(token)
    res = verify_jwt(token)
    print(res)
