import os
import asyncio
import nest_asyncio
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from llama_index.llms.openrouter import OpenRouter
from llama_index.core import Settings
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent import ReActAgent
from llama_index.core.workflow import Context

nest_asyncio.apply()

app = Flask(__name__)
CORS(app) # Enable CORS for public access

# Environment variables (to be set in your Render dashboard)
OPENROUTER_API_KEY = "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"
# The public URL of your server.py instance (e.g., https://your-tools-server.onrender.com/sse)
MCP_SERVER_URL = "http://127.0.0.1:8000/sse"

SYSTEM_PROMPT = """\
You are an AI assistant for Tool Calling.
Before you help a user, you need to work with tools to interact with Our Database or other tools offered in the MCP server.
"""

agent = None
agent_context = None
loop = asyncio.get_event_loop()

async def get_agent(tools: McpToolSpec):
    tool_list = await tools.to_tool_list_async()

    llm = OpenRouter(
        api_key=OPENROUTER_API_KEY,
        model="meta-llama/llama-3.2-3b-instruct:free",
        context_window=4096,
    )

    Settings.llm = llm

    return ReActAgent(
        tools=tool_list,
        llm=llm,
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
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
    if not agent:
        return jsonify({"error": "Agent not initialized"}), 503
        
    try:
        response = loop.run_until_complete(handle_user_message(user_input, agent, agent_context))
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        # Connect to the public MCP URL instead of 127.0.0.1
        mcp_client = BasicMCPClient(MCP_SERVER_URL)
        mcp_tool = McpToolSpec(client=mcp_client)

        agent = loop.run_until_complete(get_agent(mcp_tool))
        agent_context = Context(agent)

        # Use the PORT provided by Render or default to 5000
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    except Exception as startup_error:
        print(f"Startup failed: {startup_error}")