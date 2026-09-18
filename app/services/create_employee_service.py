


from app.schema.client_schema import CreateClientRequest
from app.repositories.create_employee_repository import CreateEmployeeRepository


from app.models.client_model import Client

class CreateEmployeeService:
    def __init__(self,db):
        self.db = db
        self.repo = CreateEmployeeRepository(db)

    async def create_client(self,request : CreateClientRequest):
        client = Client(
            name=request.name,
            email=request.email,
            phone=str(request.phone),
            company_name=request.company_name,
            is_active=True
        )
        client = await self.repo.create_client(client)
        await self.db.commit()
        return client

    
        