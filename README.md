# AI Tool-Calling Assistant with MCP, Flask & LlamaIndex

This project is a **tool-calling AI assistant** built using **Flask**, **LlamaIndex**, and **MCP (Model Context Protocol)**. It connects a Large Language Model (LLM) via **OpenRouter** to a custom **MCP tool server** that provides database operations, stock market data, and utility tools.

The system allows users to interact with an AI agent through a REST API (and optional frontend), while the agent intelligently decides when to call tools such as:

* SQLite database operations
* Indian stock price lookup (via Yahoo Finance)
* Stock news retrieval
* Time and utility functions

---

## 🧠 Architecture Overview

```
User / Frontend
      ↓
   Flask API  ──► LlamaIndex ReAct Agent ──► MCP Server Tools
      ↑                     │                     │
      └──── JSON Response ◄─┴──────── Tool Output ─┘
```

* **Flask App**: Exposes HTTP endpoints and handles user queries
* **ReAct Agent (LlamaIndex)**: Decides when and how to call tools
* **OpenRouter**: Provides access to LLaMA models
* **MCP Server**: Hosts custom tools (DB, stocks, news, time)

---

## ✨ Features

* 🔗 Tool-calling AI agent using ReAct pattern
* 🗄️ SQLite database CRUD via natural language
* 📈 Real-time Indian stock prices using Yahoo Finance
* 📰 Latest stock-related news
* ⏰ Current time/date utility
* 🌐 CORS-enabled Flask API (ready for frontend integration)
* 🚀 Deployable on Render or similar platforms

---

## 📁 Project Structure

```
├── client.py              # Flask app + AI agent
├── server.py              # MCP tool server
├── sample.db              # SQLite database (auto-created)
├── cleaned_dataset.csv    # Company name ↔ Yahoo Finance symbol mapping
├── templates/
│   └── index.html         # Optional frontend UI
├── requirements.txt
└── README.md
```

---

## 🔧 Tools Provided by MCP Server

### 🗄️ Database Tools (SQLite)

* **add_data(query: str) → bool**
  Insert records into the `people` table

* **read_data(query: str = "SELECT * FROM people") → list**
  Read records using custom SQL queries

**Table Schema:**

| Field      | Type           |
| ---------- | -------------- |
| id         | INTEGER (auto) |
| name       | TEXT           |
| age        | INTEGER        |
| profession | TEXT           |

---

### 📈 Stock Market Tools

* **get_stockprice_symbol(symbol: str) → float**
  Get current stock price by Yahoo Finance symbol (e.g. `TCS.NS`)

* **get_stockprice_name(name: str) → float**
  Get stock price using company name

* **get_all_symbol() → list**
  List all available company names

* **get_stock_news(name: str) → list[dict]**
  Fetch latest news for a given company

---

### ⏰ Utility Tools

* **get_current_time() → str**
  Returns the current date and time

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/suryap007/llm_MCP.git
cd llm_MCP
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Required libraries include:

* flask
* flask-cors
* llama-index
* yfinance
* pandas
* nest-asyncio
* mcp

---

### 3️⃣ Set Environment Variables

```bash
export OPENROUTER_API_KEY=your_api_key_here
export PORT=5000
```

> ⚠️ **Important**: Never hard-code API keys in production.

---

### 4️⃣ Start MCP Tool Server

```bash
python server.py --server_type sse
```

This starts the MCP server (default: SSE mode).

---

### 5️⃣ Start Flask App

```bash
python client.py
```

The API will be available at:

```
http://localhost:5000
```

---

## 🔌 API Endpoints

### `POST /ask`

Send a user query to the AI agent.

**Request Body:**

```json
{
  "message": "Get the stock price of Tata Consultancy Services"
}
```

**Response:**

```json
{
  "response": "The current stock price of TCS is ..."
}
```

---

## 🌐 Deployment Notes (Render)

* Set `OPENROUTER_API_KEY` in Render environment variables
* Ensure MCP server is publicly accessible
* Update `MCP_SERVER_URL` to the deployed MCP endpoint

---

## 🛡️ Security Notes

* Do **NOT** commit API keys to GitHub
* Add `.env` and database files to `.gitignore`
* Validate user inputs for SQL queries in production

---

## 📌 Future Improvements

* Authentication & rate limiting
* Better SQL abstraction (avoid raw queries)
* Streaming responses
* UI improvements
* Logging & monitoring

---


## 🙌 Acknowledgements

* [LlamaIndex](https://www.llamaindex.ai/)
* [OpenRouter](https://openrouter.ai/)
* [Yahoo Finance](https://finance.yahoo.com/)
* MCP (Model Context Protocol)

---

**Happy Building 🚀**
