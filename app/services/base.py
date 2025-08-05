from pydantic import BaseModel
from odmantic import Model,AIOEngine
from typing import TypeVar,Annotated,Any,Generic
from app.db.mongo import getEngine
from motor.core import AgnosticDatabase
from fastapi.encoders import jsonable_encoder

DBModel = TypeVar('DBModel',bound=Model)
CreateSchemaType = TypeVar('CreateSchemaType',bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType',bound=BaseModel)


class BaseService(Generic[DBModel,CreateSchemaType,UpdateSchemaType]):
    def __init__(self,model: type[DBModel]):
        self.model = model
        self.db: AIOEngine = getEngine()
        
    async def findOne(self,db:AgnosticDatabase,query:Any)-> DBModel | None:
        return await self.db.find_one(self.model,query)   
    async def createOne(self,db:AgnosticDatabase,input:CreateSchemaType)-> DBModel | None:
        jsonParsedData = jsonable_encoder(input)
        return await self.db.save(self.model(**jsonParsedData))    
    async def deleteOne(self,db:AgnosticDatabase,query:Any) -> int:
        return await self.db.remove(self.model,query)












