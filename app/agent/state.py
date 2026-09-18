from typing import TypedDict, Optional, Any


class AgentState(TypedDict):

    # Common
    user_message: str
    user_id: str
    role: str

    intent: Optional[str]

    # Leave Domain
    leave_data: Optional[dict]
    awaiting_confirmation: bool
    confirmed: Optional[bool]

    # Employee Domain
    employee_data: Optional[dict]

    # Team Domain
    team_data: Optional[dict]

    # Project Domain
    project_data: Optional[dict]

    # Client Domain
    client_data: Optional[dict]

    # Common Result
    tool_result: Optional[dict]
    final_response: Optional[str]


class SQLAgentState(TypedDict):
    question: str
    schema: Optional[str]
    sql_query: Optional[str]
    validation_result: Optional[str]
    query_result: Optional[str]
    final_answer: Optional[str]
    error: Optional[str]

    leave_data: Optional[dict]
    awaiting_confirmation: bool
    confirmed: Optional[bool]

    greeting_responce : Optional[str]

    retries: int
    user_id: str
    role: str
