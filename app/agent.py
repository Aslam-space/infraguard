import os
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
import chromadb
from app.collector import get_latest
from app.database import get_recent_incidents, get_avg_mttr
from app.detector import detect, get_anomaly_type
from app.healer import heal
from app.config import OPENAI_API_KEY, AI_PROVIDER

# ==============================================================
# ChromaDB vector memory — agent remembers past incidents
# ==============================================================
chroma_client     = chromadb.Client()
incident_memory   = chroma_client.get_or_create_collection("incidents")

def store_incident_memory(anomaly_type, action, outcome):
    """Store incident outcome in vector memory"""
    incident_memory.add(
        documents=[f"{anomaly_type} anomaly: action={action}, outcome={outcome}"],
        ids=[f"incident_{len(incident_memory.get()['ids'])+1}"]
    )

def query_memory(anomaly_type):
    """Find similar past incidents from memory"""
    results = incident_memory.query(
        query_texts=[f"{anomaly_type} anomaly"],
        n_results=min(3, len(incident_memory.get()['ids']))
    )
    if results['documents'] and results['documents'][0]:
        return results['documents'][0]
    return []

# ==============================================================
# Agent Tools — what the agent can DO
# ==============================================================
@tool
def get_current_metrics() -> dict:
    """Get current server metrics including CPU, RAM, disk usage"""
    return get_latest()

@tool
def get_incident_history() -> list:
    """Get recent incidents and their resolution details"""
    return get_recent_incidents(limit=5)

@tool
def check_anomaly() -> dict:
    """Run ML anomaly detection on current metrics"""
    m = get_latest()
    is_anomaly, score = detect(
        m['cpu'], m['ram'], m['disk'],
        m['net_in'], m['net_out']
    )
    atype, severity, value = get_anomaly_type(m['cpu'], m['ram'], m['disk'])
    return {
        "is_anomaly": is_anomaly,
        "score": score,
        "type": atype,
        "severity": severity,
        "value": value
    }

@tool
def execute_healing(anomaly_type: str) -> dict:
    """Execute auto-healing for a specific anomaly type (CPU/MEMORY/DISK/SERVICE)"""
    m       = get_latest()
    _, _, value = get_anomaly_type(m['cpu'], m['ram'], m['disk'])
    success, mttr, output = heal(anomaly_type, value)
    store_incident_memory(anomaly_type, f"heal_{anomaly_type.lower()}", 
                         "success" if success else "failed")
    return {"success": success, "mttr_seconds": mttr, "output": output[:200]}

@tool
def get_avg_recovery_time() -> float:
    """Get average MTTR (Mean Time To Recovery) across all incidents"""
    return get_avg_mttr()

# ==============================================================
# Build AI Agent
# ==============================================================
def build_agent():
    # Choose LLM based on config
    if AI_PROVIDER == "openai" and OPENAI_API_KEY:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=OPENAI_API_KEY
        )
        print("[Agent] Using OpenAI GPT-4o-mini")
    else:
        llm = Ollama(model="llama3", temperature=0)
        print("[Agent] Using Ollama Llama3 (local)")

    tools = [
        get_current_metrics,
        get_incident_history,
        check_anomaly,
        execute_healing,
        get_avg_recovery_time
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are InfraGuard, an autonomous DevOps AI agent.
Your job is to monitor server health, detect anomalies, and heal issues automatically.

Rules:
1. Always check metrics first
2. If anomaly detected, check incident history for similar patterns
3. Execute the most appropriate healing action
4. Explain your decision in plain English
5. Be concise — max 3 sentences per response"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    memory = ConversationBufferWindowMemory(
        k=5, memory_key="chat_history", return_messages=True
    )

    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(
        agent=agent, tools=tools,
        memory=memory, verbose=True,
        handle_parsing_errors=True
    )

# Global agent instance
agent_executor = None

def get_agent():
    global agent_executor
    if agent_executor is None:
        agent_executor = build_agent()
    return agent_executor

def run_agent(prompt="Check server health and fix any issues"):
    """Run the agent with a prompt, return response"""
    try:
        agent  = get_agent()
        result = agent.invoke({"input": prompt})
        return result.get("output", "Agent completed task")
    except Exception as e:
        return f"[Agent Error] {e}"
