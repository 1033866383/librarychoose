HTTP_ERROR_CODE = {
    400: 'Bad request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'The requested URL was not found on the server.',
    405: 'Method not allowed'
}


class SetCode(object):
    def __init__(self, code=500, msg='Internal server error'):
        self.code = code
        self.msg = msg


class Code():
    ERROR = SetCode()
    SUCCESS = SetCode(0, '请求成功')
    BAD_REQUEST = SetCode(400, 'Bad request')
    NOT_FOUND = SetCode(404, 'Not found')
    LOGIN_ERROR = SetCode(401, 'Unauthorized')
    NO_permission = SetCode(403, 'Forbidden')

    NO_PARAM = SetCode(10001, 'No parameter')

    NAME_ALREADY_EXIST = SetCode(10003, 'The name has already existed')

    # api
    API_NOT_FOUNT = SetCode(10004, '接口不存在!')
    API_EXIST = SetCode(10005, '接口已存在!')
    API_ID_IS_NUll = SetCode(10006, '接口id不能为空!')

    # env
    ENV_NOT_FOUNT = SetCode(20001, '环境配置不存在')
    ENV_ID_IS_NUll = SetCode(20002, '配置id不能为空!')
    ENV_ALREADY_EXIST = SetCode(20003, '环境配置已存在')

    CLIENT_ERROR = SetCode(20000, 'Client error')

    VALIDATOR_ERROR = SetCode(30000, 'Validator error')

    GENERATOR_ERROR = SetCode(40000, 'Generator error')

    # user
    USER_INFO_ERROR = SetCode(5000, '用户名&密码不匹配')
    USER_EXIST = SetCode(5001, '用户信息已存在，请修改信息重新提交')
    USER_NOT_EXIST = SetCode(5002, '用户不存在')
    USER_NAME_EXIST = SetCode(5003, '用户名重复')
    USER_MAIL_EXIST = SetCode(5004, '邮箱重复')
    USER_NOT_ALLOW_RM = SetCode(5005, '用户是超级管理员不允许删除!')  # 只有roles=-99时,走这个提示

    WX_MSG_URL_ERROR = SetCode(6000, 'url must be start with http or https ')
    WX_MSG_URL_NEED = SetCode(6001, 'url is required')
