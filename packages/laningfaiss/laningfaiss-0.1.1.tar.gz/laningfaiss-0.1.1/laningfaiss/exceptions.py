class FaissBaseException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


##################################################

class APIException(FaissBaseException):
    """
    索引引擎侧的错误
    """


class TimeoutException(APIException):
    """
    接口访问超时
    """


class ExplicitException(APIException):
    """
    接口主动报错
    """


class UnknownException(APIException):
    """
    未知的错误
    """


##################################################

class ClientException(FaissBaseException):
    """
    用户侧的错误
    """


class InvalidException(ClientException):
    """
    参数的错误
    """
