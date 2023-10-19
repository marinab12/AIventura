from langchain.agents import load_tools
from langchain.tools import tool

from tools.reply_user import ReplyUser

nl2reply = ReplyUser(verbose=False)

human_tool = load_tools(["human"])[0]


@tool
def reply_user(nl_query: str) -> any:
    """Use this tool to reply to user queries"""
    extra_info = input('Be more precise:')
    return extra_info

toolkit_registry = {
    'reply': reply_user,
}


def list_available_tools():
    """Lists the available tools."""
    return list(toolkit_registry.keys())


def load_tools(tools = None):
    """Loads the tools."""
    if tools is None:
        return list(toolkit_registry.values())
    else:
        assert all(
            tool in toolkit_registry for tool in tools), f'Invalid tool(s): {tools}'
        return [toolkit_registry[tool] for tool in tools]
