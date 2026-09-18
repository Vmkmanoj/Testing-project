from pydantic import BaseModel



class CreateClientRequest(BaseModel):
    name: str
    email:str
    phone:int
    company_name : str

    

