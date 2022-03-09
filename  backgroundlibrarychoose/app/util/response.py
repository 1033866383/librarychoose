from flask import jsonify

from app.util.code import Code


def response(data={}, msg=None, status_code=200, status=Code.SUCCESS.code, error_code=None, cookie=None):
    message = msg if msg else 'success'
    if error_code:
        message = error_code.msg if not msg else '{}: {}'.format(
            error_code.msg, msg)
        status = error_code.code
    try:
        output = jsonify({"status": status, "data": data, "msg": message})
    except TypeError as e:
        output = jsonify({"status": -1, "data": data, "msg": str(e)})
    resp = output
    resp.status_code = status_code
    if cookie and isinstance(cookie, dict):
        for item in cookie.items():
            resp.set_cookie(item[0], item[1])
    return resp
