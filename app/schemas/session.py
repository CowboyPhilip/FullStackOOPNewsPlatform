from pydantic import BaseModel,Field
from typing import Annotated,Any
from odmantic import ObjectId
from datetime import datetime





class SessionCreate(BaseModel):
    userId: ObjectId 
    is_valid:bool = True
    
    

class SessionUpdate(SessionCreate):
    is_valid:bool = False

