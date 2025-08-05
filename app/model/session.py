from __future__ import annotations
from odmantic import Model,Field
from datetime import datetime
from odmantic import ObjectId
# if TYPE_CHECKING:
#     from . import Token

Base = Model


def currentTimeFactory():
    return datetime.now().replace(microsecond=0)




class SessionsModel(Model):
   created_At: datetime = Field(default_factory=currentTimeFactory)
   updated_At: datetime = Field(default_factory=currentTimeFactory)
   userId: ObjectId = Field(default='')
   is_valid: bool = Field(default=True)