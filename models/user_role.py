from enum import (
    Enum,
    auto,
)

# from utils import log


class UserRole(Enum):
    '''
    用户身份的分类：游客，普通用户，管理员
    '''
    guest = auto()
    normal = auto()
    admin = auto()

    @classmethod
    def encoder(cls, obj):
        """
        from UserRole to String
        """
        return obj.name

    @classmethod
    def decoder(cls, value):
        """from String to UserRole"""
        return cls[value]
