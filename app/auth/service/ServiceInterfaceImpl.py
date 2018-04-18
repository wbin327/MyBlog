# encoding=utf-8
# from .ServiceInterface import ServiceInterface
import time

from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.dao.auth_dao import Dao
from app.util.public_method import PublicMethod, JsonWebToken


class ServiceInterfaceImpl(object):
    def __init__(self):
        self.dao = Dao()

    def login_check(self, name, password):
        """
            用户登录，登录成功返回token,并将登录时间写入数据库；登录失败则返回失败原因
            :param username: 用户名
            :param password: 密码
            :return: dict
            """
        user = self.dao.query_user_by_name(name)
        if user:
            result = check_password_hash(user.password, password)
            if result:
                user.login_time = time.time()
                self.dao.add(user)
                token = JsonWebToken.encode_auth_token(user_id=user.id, login_time=user.login_time)
                return PublicMethod.true_return(data=token, msg='登录成功')
            else:
                return PublicMethod.false_return(data='', msg='密码错误')
        else:
            return PublicMethod.false_return(data='', msg='用户名不存在')

    def register(self, username, password):
        result = ''
        user = self.dao.query_user_by_name(username)
        if user:
            result = PublicMethod.false_return(data='', msg='用户名已存在')
        else:
            hash_password = generate_password_hash(password)
            excute = self.dao.add_user(username, hash_password)
            if excute is True:
                result = PublicMethod.true_return(data='', msg='注册成功')
            else:
                result = PublicMethod.false_return(data='', msg='注册失败')
        return result


    def get_user(self, authorization):
        result = JsonWebToken.identify(authorization)
        if isinstance(result, str):
            return PublicMethod.false_return(data='', msg=result)
        else:
            id = result['data']['id']
            user = self.dao.get_user_by_id(id)
            return PublicMethod.true_return(data=user.serialize(), msg='success')


if __name__ == '__main__':
    print generate_password_hash('wbin1994')
    print check_password_hash('pbkdf2:sha256:50000$7ucudFac$458f09e47bae587647c1fd98b7711c2e8e354b3b9018f731769af0fd80074e7f', 'wbin1994')
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJrZW4iLCJpYXQiOjE1MTE0ODQ3NDEsImRhdGEiOnsiaWQiOjEsImxvZ2luX3RpbWUiOjE1MTE0ODAwMDAuMH0sImV4cCI6MTUxMTQ4NTM0MX0.p5PmIlPCEAN_IVg7rO1DPSXCjnevLJiFsygoAqDTuVM'
    token2= 'eyJpc3MiOiJrZW4iLCJpYXQiOjE1MTE0ODQ3NDEsImRhdGEiOnsiaWQiOjEsImxvZ2luX3RpbWUiOjE1MTE0ODAwMDAuMH0sImV4cCI6MTUxMTQ4NTM0MX0.'
    print JsonWebToken.decode_auth_token(token2)