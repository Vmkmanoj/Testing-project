LEAVE_EXTRACTION_PROMPT = """Extract ALL leave request details from the user's message.
Return a JSON array of objects. Each object must have the following keys: 
start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), leave_type (one of casual, sick, earned), reason (string).
Remember today's date.
If a field is missing, set it to null.
If there are multiple distinct leave requests, return multiple objects in the array.

User message: {message}
"""

CANCEL_REQUEST = """this is for cancel all pending

User message: {message}
"""

NAME_EXTRACTION_PROMPT = """Extract the employee name the user is asking about in their message.
If they are asking about their own balance or don't specify a name, return `null`.
Otherwise, return only the name as a string, e.g. "manojkumar".

User message: {message}
"""

INTENT_CLASSIFIER_PROMPT = """You are an intent classifier for a leave management assistant.
Classify the user's message into exactly one of these labels:

- apply_leave      -> user wants to request/apply for time off
- check_balance    -> user wants to know how many leave days they have left
- check_status     -> user wants to know the status of an existing request
- cancel_leave     -> user wants to cancel a leave request
- policy           -> user is asking about leave rules/policy
- greeting         -> user greets 
- database_query   -> user asks a general question about employees, managers, departments, or other data not covered above

Respond with only the label, nothing else.

User message: {message}
"""


LEAVE_SUBMISSION_PROMPT = """
Act as a leave assistant for an employee.
Today is {today}.

First, check if leave dates overlap with existing approved leave requests for the user.
Show existing approved leaves:
- Dates: YYYY-MM-DD to YYYY-MM-DD
- Type
- Days

If there is any overlap with already-approved leave, DO NOT proceed with submission.
Instead, respond with a message like:
"You already have overlapping approved leave from [start] to [end].
Do you want me to cancel those or apply this as a new overlapping request?"

If no overlap with approved leave:
1. Calculate total days (inclusive).
2. Calculate total available balance for the leave type for this user.
3. If total days > available balance, respond with:
   "You requested {total_days} days, but only {available} are available.
   Available balance: {available_type}. Available casual: {available_casual}.
   Do you want me to adjust the dates or use casual leave instead?"

If sufficient balance:
4. Create a leave request using start_date, end_date, leave_type, and reason.
5. Confirm:
   "Leave request for {leave_type} from {start} to {end} ({days} days) created."
"""
