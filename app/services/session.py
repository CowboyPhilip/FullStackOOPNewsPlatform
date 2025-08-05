from app.services.base import BaseService
from app.model.session import SessionsModel
from app.schemas.session import SessionCreate,SessionUpdate




class SessionService(BaseService[SessionsModel,SessionCreate,SessionUpdate]):
    async def createSession(self,obj:SessionCreate):
        sessionObj = {
            **obj.model_dump(),
            'userId':obj.userId
        }
        return await self.db.save(SessionsModel(**sessionObj))