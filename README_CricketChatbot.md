
# 🏏 Cricket Chatbot – AI-Powered Query Assistant

An intelligent chatbot designed to deliver accurate, real-time, and historical cricket information using **LangGraph**, **LangChain**, and **ReAct agents**.

---

## 🧠 Overview

This project is an **AI-powered chatbot** that helps users retrieve cricket-related information through natural language queries. It supports three core functionalities:

- **Live Matches** – Provides real-time updates on ongoing cricket games.  
- **Past Matches** – Summarizes and fetches completed match data and stats.  
- **General Queries** – Answers questions about players, teams, rankings, and historical events.

Built using modern AI and orchestration tools, the chatbot mimics expert reasoning using **ReAct agents**, **RAG**, and **LangGraph**.

---

## ✨ Features

- **📺 Live Cricket Updates**  
  Fetches real-time match scores and highlights using public cricket APIs.

- **📊 Match Summary & Stats**  
  Retrieves summaries, player performance, and historical game data.

- **🧠 Intelligent Agent-Based Reasoning**  
  Uses **ReAct agents** for iterative thinking and **RAG** for enhanced factual responses.

- **🔎 Web Search Integration**  
  Extends knowledge beyond local databases using real-time web results.

- **🧱 Modular & Scalable Backend**  
  Object-Oriented Python design for easy maintenance and extension.

---

## 🧱 Architecture

The chatbot processes each query in a stepwise, intelligent pipeline:

```text
User Query ➞ Intent Detection ➞ Agent Decision ➞ Data Fetching (API/RAG/Web) ➞ Response Synthesis ➞ Output
```

### 🧑‍💻 Agents & Roles

| Agent Type         | Role & Functionality                                                      |
| ------------------ | ------------------------------------------------------------------------- |
| ReAct Agent        | Breaks down complex queries and iteratively collects relevant facts       |
| RAG Agent          | Retrieves real-time data and enhances response generation                 |
| Web Search Agent   | Fetches live cricket news or stats if not found in APIs or databases      |

---

## 🧰 Technologies Used

| Tool                     | Purpose                                                    |
| ------------------------ | ---------------------------------------------------------- |
| **LangChain**            | Handles agent interactions and language model queries      |
| **LangGraph**            | Controls the flow of multi-agent conversations             |
| **ReAct Agents**         | Iterative reasoning and multi-step thought processes       |
| **Mistral AI**           | Primary LLM for generating natural responses               |
| **Live Cricket APIs**    | For fetching real-time match data                          |
| **Web Search (RAG)**     | Provides up-to-date external knowledge                     |
| **Python (.env, OOP)**   | Core backend logic and secure API configuration            |

---

## ⚙️ Installation & Setup

### 📦 Prerequisites

- Python 3.8 or higher
- API keys for:
  - Live Cricket Data API
  - Web Search (optional)

### 🔧 Setup Steps

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Configure environment variables
# Create a `.env` file with:
# CRICKET_API_KEY=your_key_here

# Step 3: Run the app
python frontend.py
```

---

## 🚀 How It Works

1. User selects a category: **Live**, **Past**, or **General** queries.
2. AI agents analyze the query and decide how to fetch information.
3. Relevant APIs or web tools are triggered to collect data.
4. LLM composes a clear and structured response.
5. Result is displayed in the chatbot interface.

---

## 💬 Sample Queries

- “What’s the score of the current India match?”  
- “Who won the IPL 2023 final?”  
- “Show me Virat Kohli’s batting average in ODIs.”

---

## 📌 Final Thoughts

The Cricket Chatbot combines the power of **AI agents**, **real-time data**, and **conversational intelligence** to deliver an interactive sports assistant. It’s a modular project that can be extended to support additional sports, news domains, or analytics tools.
