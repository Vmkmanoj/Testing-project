from app.agent.state import SQLAgentState
from langgraph.graph import StateGraph, END, START
from app.agent.state import AgentState
from app.agent.node.leave_node import (
    apply_leave,
    create_leave_node,
    cancel_leave,
    check_balance_node,
)
from app.agent.router import router_intent, confirmation_router
from langgraph.checkpoint.memory import MemorySaver

from app.agent.node.Employe_node.generate_sql import generate
from app.agent.node.Employe_node.validate_sql import validate_sql
from app.agent.node.Employe_node.execute_sql import execute_sql
from app.agent.node.Employe_node.format_answer import format_answer
from app.database.database import Sql_agent
from app.agent.node.Employe_node.get_node import get_schema
from app.agent.router import check_validation
from app.agent.node.Employe_node.policy import policy
from app.agent.node.Employe_node.greeting_node import greeting
from app.agent.node.Employe_node.conformantion_node import confirmation


checkpointer = MemorySaver()


# def build_graph():
#     workflow = StateGraph(AgentState)

#     workflow.add_node("apply_leave", apply_leave.run)
#     # workflow.add_node("confirmation", confirmation_node.run)
#     workflow.add_node("create_leave", create_leave_node.run)
#     workflow.add_node("cancel_leave", cancel_leave.run)
#     workflow.add_node("check_balance", check_balance_node.run)
#     workflow.add_node("policy", policy)

#     async def not_implemented(state: AgentState):
#         state["final_response"] = "This feature is not yet implemented."
#         return state

#     async def clarify(state: AgentState):
#         state["final_response"] = (
#             "I'm not sure I understand. Could you please rephrase your request? You can ask me to apply for leave, check your balance, or ask about leave policies."
#         )
#         return state

#     for node_name in ["check_status", "policy_qa"]:
#         workflow.add_node(node_name, not_implemented)

#     workflow.add_node("clarify", clarify)
#     workflow.set_conditional_entry_point(
#         router_intent,
#         {
#             "apply_leave": "apply_leave",
#             "check_balance": "check_balance",
#             "check_status": "check_status",
#             "cancel_leave": "cancel_leave",
#             "policy_qa": "policy_qa",
#             "unclear": "clarify",
#             "confirmation": "confirmation",
#         },
#     )

#     workflow.add_edge("apply_leave", END)

#     workflow.add_conditional_edges(
#         "confirmation",
#         confirmation_router,
#         {
#             "create_leave": "create_leave",
#             "clarify": "clarify",
#         },
#     )

#     workflow.add_edge("create_leave", END)

#     for node in [
#         "apply_leave",
#         "check_balance",
#         "check_status",
#         "cancel_leave",
#         "policy_qa",
#         "clarify",
#     ]:
#         workflow.add_edge(node, END)

#     return workflow.compile(checkpointer=checkpointer)


# agent_graph = build_graph()


def build_agent_graph():

    graph = StateGraph(SQLAgentState)

    # =========================
    # Nodes
    # =========================

    graph.add_node("get_schema", get_schema)
    graph.add_node("generate_sql", generate)
    graph.add_node("validate_sql", validate_sql)
    graph.add_node("execute_sql", execute_sql)
    graph.add_node("format_answer", format_answer)
    graph.add_node("greeting", greeting)
    graph.add_node("policy", policy)
    graph.add_node("confirmation", confirmation)

    # =========================
    # ENTRY ROUTER
    # =========================

    graph.set_conditional_entry_point(
        router_intent,
        {
            "greeting": "greeting",
            "get_schema": "get_schema",
            "policy": "policy",
            "confirmation": "confirmation",
        },
    )

    # =========================
    # SQL FLOW
    # =========================

    graph.add_edge("get_schema", "generate_sql")

    graph.add_edge("generate_sql", "validate_sql")

    # =========================
    # SQL VALIDATION ROUTER
    # =========================

    graph.add_conditional_edges(
        "validate_sql",
        check_validation,
        {
            "execute_sql": "execute_sql",
            "generate_sql": "generate_sql",
            "confirmation": "confirmation",
            "format_answer": "format_answer",
            "greeting": "greeting",
            "end": END,
        },
    )

    graph.add_conditional_edges(
        "confirmation",
        confirmation_router,
        {
            "execute_sql": "execute_sql",
            "format_answer": "format_answer",
        },
    )

    graph.add_edge("execute_sql", "format_answer")

    # =========================
    # GREETING
    # =========================

    graph.add_edge("greeting", END)

    # =========================
    # POLICY
    # =========================

    graph.add_edge("policy", END)

    # =========================
    # END
    # =========================

    graph.add_edge("format_answer", END)

    return graph.compile(checkpointer=checkpointer)


sql_agent_graph = build_agent_graph()
