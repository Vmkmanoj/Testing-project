
from app.services.employee_service import EmployeeService



class EmployeeTool:

    @staticmethod
    async def get_employee_detail(name : str):

        service = EmployeeService.get_user_name(name)


        










