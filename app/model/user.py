from __future__ import annotations
from odmantic import Model,Field
from typing import Any
from datetime import datetime
from pydantic import EmailStr
from app.config.debs import permissionType
from enum import Enum
# if TYPE_CHECKING:
#     from . import Token

Base = Model


def currentTimeFactory():
    return datetime.now().replace(microsecond=0)



class Role(str,Enum):
    user = 'user'
    admin = 'admin'
    super = 'superadmin'


class UsersModel(Model):
   created_At: datetime = Field(default_factory=currentTimeFactory)
   updated_At: datetime = Field(default_factory=currentTimeFactory)
   full_name: str = Field(default='')
   email:EmailStr
   is_verified: bool = Field(default=False)
   is_super:bool = Field(default=False)
   password: Any = Field(default='')
   role: Role
   permissions:permissionType
