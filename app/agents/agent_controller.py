import os
from typing import TypedDict, Annotated, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
import operator

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

from app.agents.tools import (
    search_codebase,
    read_file,
    get_repo_structure,
    search_by_language,
    search_functions_only,
)


# ─── Agent State ──────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    repo_name: str


# ─── System Prompt ────────────────────────────────────────────────────────────
AGENT_SYSTEM_PROMPT = """You are RepoMind, an expert AI agent that helps developers understand GitHub repositories.

You have access to these tools:
- search_codebase: Semantically search for relevant code
- read_file: Read a complete file from the repo
- get_repo_structure: See the folder/file structure
- search_by_language: Search filtered by programming language
- search_functions_only: Find specific function definitions

When answering questions:
1. Always search the codebase first before answering
2. Use multiple tools if needed for a complete answer
3. Reference specific files and line numbers when possible
4. Be concise but thorough

The user is asking about the repository: {repo_name}"""


# ─── Tools List ───────────────────────────────────────────────────────────────
TOOLS = [
    search_codebase,
    read_file,
    get_repo_structure,
    search_by_language,
    search_functions_only,
]


# ─── Build Agent ──────────────────────────────────────────────────────────────
def build_agent(repo_name: str):
    """Build and return a LangGraph agent using Groq."""

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0.1,
    )

    llm_with_tools = llm.bind_tools(TOOLS)

    def agent_node(state: AgentState):
        system_msg = SystemMessage(
            content=AGENT_SYSTEM_PROMPT.format(repo_name=state["repo_name"])
        )
        messages = [system_msg] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(TOOLS)

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()


# ─── Run Agent ────────────────────────────────────────────────────────────────
def run_agent(question: str, repo_name: str) -> str:
    """Run the agent on a question about a repo."""
    agent = build_agent(repo_name)

    initial_state = {
        "messages": [HumanMessage(content=question)],
        "repo_name": repo_name,
    }

    print(f"🤖 Agent starting for repo: {repo_name}")
    print(f"❓ Question: {question}")
    print("-" * 50)

    final_state = agent.invoke(initial_state)

    for msg in reversed(final_state["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content

    return "Agent could not generate a response."