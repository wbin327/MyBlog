# encoding=utf-8
import jwt
import datetime
from config import DevelopmentConfig
from app.models.user import User


def encode_auth_token(user_id, login_time):
    """
    生成认证Token
    :param user_id: int
    :param login_time: int(timestamp)
    :return: string
    """
    try:
        '''
        “exp”: 过期时间
        “nbf”: 表示当前时间在nbf里的时间之前，则Token不被接受
        “iss”: token签发者
        “aud”: 接收者
        “iat”: 发行时间
        '''
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'iss': 'ken',
            'data': {
                'id': user_id,
                'login_time': login_time
            }
        }

        '''
        jwt.encode(payload, config.SECRET_KEY, algorithm=’HS256′)
        上面代码的jwt.encode方法中传入了三个参数：第一个是payload，这是认证依据的主要信息，第二个是密钥，这里是读取配置文件中的SECRET_KEY配置变量，第三个是生成Token的算法。
        这里稍微讲一下payload，这是认证的依据，也是后续解析token后定位用户的依据，需要包含特定用户的特定信息
        如本例注册了data声明，data声明中包括了用户ID和用户登录时间两个参数，在“用户鉴权”方法中，解析token完成后要利用这个用户ID来查找并返回用户信息给用户。
        '''
        token = jwt.encode(payload=payload, key=DevelopmentConfig.SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    验证token
    :param auth_token: token
    :return: sting
    """
    try:
        '''
        jwt.decode(auth_token, config.SECRET_KEY, options={‘verify_exp’: False})
        上面的options设置不验证过期时间，如果不设置这个选项，token将在原payload中设置的过期时间后过期。
        经过上面解析后，得到的payload可以跟原来生成payload进行比较来验证token的有效性。
        '''
        payload = jwt.decode(auth_token, DevelopmentConfig.SECRET_KEY)
        if 'data' in payload and 'id' in payload['data']:
            return payload
        else:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return 'Token过期'
    except jwt.InvalidTokenError:
        return '无效Token'


def identify(authorization):
    """
    用户鉴权，解析请求头部Authorization,判断是否异常
    :param authorization: request请求头部的Authorization
    :return: 成功则返回user对象,失败返回str
    """
    if authorization:
        auth_tokenArr = authorization.split(" ")
        if auth_tokenArr is None or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
            result = '请传递正确的验证头消息'
        else:
            payload = decode_auth_token(auth_tokenArr[1])
            if not isinstance(payload, str):
                user = User.query.filter_by(id=payload['data']['id']).first()
                if user is None:
                    result = '找不到用户信息'
                else:
                    if user.login_time == payload['data']['login_time']:
                        return user
                    else:
                        result = 'token已更改，请重新登录'
            else:
                result = payload
    else:
        result = '没有提供token,验证失败'
    return result
