from pydantic import BaseModel,Field
from typing import Literal,Annotated
from fastapi import UploadFile,File,Form

class FilterParams(BaseModel):
    limit:  int = Field(100,gt=0,le=100)   
    offset: int = Field(0,ge=0)
    orderBy: Literal['created_at','updated_at'] = 'created_at'
    tags: list[str] = []
    
class Blog(BaseModel):
    file:Annotated[UploadFile,File()]
    blogName:Annotated[str,Form()]    
    
class Item(BaseModel):
    name: str 
    description: str 
    price: float
    tax: float = 10.5
    tags: list[str] = []
    