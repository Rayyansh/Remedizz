# from dataclasses import dataclass
#
#
# @dataclass
# class AppTemplateRequest:
#     pass

from dataclasses import dataclass


@dataclass
class UserCreateData:
    username: str
    user_role: str
    contact_number: str
    profile_picture: str = None
