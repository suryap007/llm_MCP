from flask import Flask, render_template, request, jsonify
import asyncio
import nest_asyncio
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent, ToolCall, ToolCallResult
from llama_index.core.workflow import Context

nest_asyncio.apply()

app = Flask(__name__)
m = "llama3.2"

SYSTEM_PROMPT = """\
You are an AI assistant for Tool Calling.
Before you help a user, you need to work with tools to interact with Our Database or other tools offered in the MCP server.
"""

agent = None
agent_context = None
loop = asyncio.get_event_loop()

async def get_agent(tools: McpToolSpec):
    tool_list = await tools.to_tool_list_async()
    return FunctionAgent(
        name="Agent",
        description="An agent that can work with Database software or other tools in MCP server",
        tools=tool_list,
        llm=Ollama(model=m),
        system_prompt=SYSTEM_PROMPT,
    )

async def handle_user_message(message_content, agent, agent_context):
    handler = agent.run(message_content, ctx=agent_context)

    response = await handler
    return str(response)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    try:
        response = loop.run_until_complete(handle_user_message(user_input, agent, agent_context))
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        Settings.llm = Ollama(model=m, request_timeout=120.0)
        mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
        mcp_tool = McpToolSpec(client=mcp_client)

        agent = loop.run_until_complete(get_agent(mcp_tool))
        agent_context = Context(agent)

        app.run(debug=True)
    except Exception as startup_error:
        print(f"Startup failed: {startup_error}")
