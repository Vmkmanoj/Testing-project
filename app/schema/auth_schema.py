from pydantic import BaseModel



class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class PermissionResponse(BaseModel):
    id: str
    name: str
    description: str

class RoleResponse(BaseModel):
    id: str
    name: str
    permissions: list[PermissionResponse]

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str = "EMPLOYEE"
    manager_id: str | None = None

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str | None = None
    email: str
    role: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    role: str
    access_token: str
    token_type: str
    user: UserResponse

class RegisterResponse(BaseModel):
    success: bool
    message: str