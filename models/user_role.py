from enum import (
    Enum,
    auto,
)

from bson.codec_options import TypeCodec
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


class UserRoleCodec(TypeCodec):
    # the Python type acted upon by this type codec
    python_type = type(UserRole.guest)
    # the BSON type acted upon by this type codec
    bson_type = str

    def transform_python(self, value):
        """Function that transforms a custom type value into a type
        that BSON can encode."""
        return UserRole.encoder(value)

    def transform_bson(self, value):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        return UserRole.decoder(value)


userrole_codec = UserRoleCodec()


if __name__ == '__main__':
    g = UserRole.guest
    print('UserRole type', type(UserRole))
    print('UserRole.guest type', type(g))
    print('g.name', g.name)
    print('decoder', UserRole.decoder('guest'))
