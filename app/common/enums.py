from enum import Enum

class RoleName(str, Enum):
    """
    System roles used throughout the application.
    """

    EMPLOYEE = "EMPLOYEE"

    MANAGER = "MANAGER"

    HR = "HR"


    