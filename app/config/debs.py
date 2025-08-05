from typing import Generator
from app.db.mongo import MongoConnection
from abc import ABC,abstractmethod
from typing import Literal
def get_db() -> Generator:
    try:
        db = MongoConnection()
        yield db
    finally:
        pass



permissionType = list[Literal['read','write','update','delete'] or Literal['read','write']]

Role = Literal['user','admin','superadmin']

class MainBaseAuth(ABC):
    @abstractmethod
    def permission(self) -> permissionType:
        pass
    role:Role
    
    super:bool = False
    
class Admin(MainBaseAuth):   
    def permission(self) -> permissionType:
        return ['read','write','update','delete']
    role = 'admin'
class User(MainBaseAuth):   
    def permission(self) -> permissionType:
        return ['read','write']
    role = 'user'    
class SuperAdmin(MainBaseAuth):   
    def permission(self) -> permissionType:
        return ['read','write','update','delete']
    role = 'superadmin'    
    super = True

class Factory(ABC):
    @staticmethod
    def create(role:Role)-> MainBaseAuth:
        if(role == 'admin'):
            return Admin()
        elif (role == 'superadmin'):
            return SuperAdmin()
        return User()
    
    
    

