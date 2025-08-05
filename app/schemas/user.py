from pydantic import BaseModel,EmailStr,StringConstraints,ConfigDict,Field,field_validator
from typing import Annotated,Literal
from odmantic import ObjectId
from datetime import datetime
from app.config.debs import Role,permissionType
class userLogin(BaseModel):
    email:EmailStr
    password:str
    


class UserBase(BaseModel):
    full_name: str 
    
    
class UserCreate(UserBase):
    role: Role
    email: EmailStr
    password: Annotated[str | None , StringConstraints(min_length=6,max_length=34)]
        
    
    
class UserPasswordUpdate(UserBase):
    original: Annotated[str | None, StringConstraints(min_length=8, max_length=64)] = None # noqa
    password: Annotated[str | None, StringConstraints(min_length=8, max_length=64)] = None  # noqa   
    
    
class UserInDB(UserBase):
    email:EmailStr | None = None
    model_config = ConfigDict(from_attributes=True)
    
class User(UserInDB):
    role:Role
    permissions:permissionType
    is_verified:bool 
    is_super:bool
    hashed_password: bool = Field(default=False, alias="password")
    model_config = ConfigDict(populate_by_name=True)
    created_At: datetime
    updated_At:datetime
    id: ObjectId | None = None
    

    
    @field_validator("hashed_password", mode="before")
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False