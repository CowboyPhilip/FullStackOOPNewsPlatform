from app.services.base import BaseService
from app.model.user import UsersModel
from app.schemas.user import UserCreate,UserPasswordUpdate
from app.utils.utilities import hashPassword,verify_password
from motor.core import AgnosticDatabase
from typing import Any,Optional
from odmantic.query import QueryExpression
from pydantic import EmailStr
from app.config.debs import Factory


class UserService(BaseService[UsersModel,UserCreate,UserPasswordUpdate]):
    
    def __init__(self,model:UsersModel):
        super().__init__(UsersModel)
        self.factory = Factory
 
    async def getUserByEmail(self,email:EmailStr)->UsersModel | None:
        return await self.db.find_one(self.model,self.model.email == email)
    async def GetUser(self,query:Any)-> UsersModel | None:
        return await self.db.find_one(self.model,query)
      
    async def getAllUsers(self,query:Optional[QueryExpression | dict | bool ] = None)-> list[UsersModel] | None:
        if query is not None:
            return await self.db.find(self.model,query)
        return await self.db.find(self.model)
    async def createUser(self,db:AgnosticDatabase,*,Input:UserCreate)-> UsersModel | None:
        
      userInstance = self.factory.create(role=Input.role) 
      
      userObj = {
         **Input.model_dump(),
         'role':userInstance.role,
         'permissions':userInstance.permission(),
         'email':Input.email,
         'full_name':Input.full_name,
         'password':hashPassword(Input.password) if Input.password is not None else None,
         'is_super':userInstance.super
      }
      
      return await self.db.save(self.model(**userObj))
  
    async def changePassword(self,user:UsersModel,newPassword:str):
        hashed = hashPassword(newPassword)
        
        user.password = hashed
        
        return await self.db.save(user)
    
    async def Authenticate(self,email:EmailStr,password:str) -> bool:
        RESULT = await self.GetUser(self.model.email == email)
        if not RESULT:
            return False
        return verify_password(password,RESULT.password)
        
        
    @staticmethod
    def has_password(user:UsersModel) -> bool:
        return user.password is not None
      
    @staticmethod
    def is_super(user:UsersModel) -> bool: 
        return user.is_super 
  
  
