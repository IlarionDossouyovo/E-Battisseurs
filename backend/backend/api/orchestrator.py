"""M-12 Orchestrateur IA - N8N Agents"""
from fastapi import APIRouter
from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# Models
class Agent(BaseModel):
    id: str
    name: str
    description: str
    status: str  # idle, running, completed, failed
    last_run: Optional[str] = None
    webhook_url: Optional[str] = None

class AgentRun(BaseModel):
    agent_id: str
    input_data: dict
    output_data: Optional[dict] = None
    status: str
    duration_ms: Optional[int] = None

# Define 12 IA Agents (corresponding to 12 modules)
AGENTS = [
    {
        "id": "agent-01",
        "name": "Sourcing Agent",
        "description": "Recherche produits tendances et analyse fournisseurs",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/sourcing",
    },
    {
        "id": "agent-02", 
        "name": "Pricing Agent",
        "description": "Optimisation des prix et marges",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/pricing",
    },
    {
        "id": "agent-03",
        "name": "Order Router",
        "description": "Routage automatique vers meilleur fournisseur",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/order-router",
    },
    {
        "id": "agent-04",
        "name": "Shipping Optimizer",
        "description": "Sélection transporteur optimal",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/shipping",
    },
    {
        "id": "agent-05",
        "name": "Fraud Detector",
        "description": "Détection fraude paiement",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/fraud",
    },
    {
        "id": "agent-06",
        "name": "Content Generator",
        "description": "Génération contenu produit par IA",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/content",
    },
    {
        "id": "agent-07",
        "name": "Chatbot Agent",
        "description": "Support client IA multilingue",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/chatbot",
    },
    {
        "id": "agent-08",
        "name": "Supplier Negotiator",
        "description": "Négociation automatique fournisseurs",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/negotiator",
    },
    {
        "id": "agent-09",
        "name": "Analytics Agent",
        "description": "Analyse données et prédictions",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/analytics",
    },
    {
        "id": "agent-10",
        "name": "Compliance Agent",
        "description": "Vérification conformité douanière",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/compliance",
    },
    {
        "id": "agent-11",
        "name": "Affiliate Manager",
        "description": "Gestion programme affiliation",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/affiliate",
    },
    {
        "id": "agent-12",
        "name": "Orchestrator",
        "description": "Coordination et décision globale",
        "status": "idle",
        "webhook_url": "http://n8n:5678/webhook/orchestrator",
    },
]

# Agent run history
RUN_HISTORY = []

@router.get("/agents", response_model=List[dict])
async def list_agents(status: Optional[str] = None):
    """List all IA agents"""
    if status:
        return [a for a in AGENTS if a["status"] == status]
    return AGENTS

@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    agent = next((a for a in AGENTS if a["id"] == agent_id), None)
    if not agent:
        return {"error": "Agent not found"}
    return agent

@router.post("/agents/{agent_id}/run")
async def run_agent(agent_id: str, input_data: dict):
    """Run an agent"""
    agent = next((a for a in AGENTS if a["id"] == agent_id), None)
    if not agent:
        return {"error": "Agent not found"}
    
    # Mock execution
    agent["status"] = "running"
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    
    # Simulate result
    result = {
        "run_id": run_id,
        "agent_id": agent_id,
        "status": "completed",
        "result": f"Processed: {input_data}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    
    agent["status"] = "completed"
    agent["last_run"] = result["timestamp"]
    
    RUN_HISTORY.append(result)
    
    return {"success": True, "run": result}

@router.post("/agents/run-all")
async def run_all_agents(input_data: dict):
    """Run all agents in sequence (orchestration)"""
    results = []
    start_time = datetime.utcnow()
    
    for agent in AGENTS:
        agent["status"] = "running"
        result = {
            "agent_id": agent["id"],
            "agent_name": agent["name"],
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        agent["status"] = "completed"
        results.append(result)
    
    duration = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    return {
        "success": True,
        "total_agents": len(AGENTS),
        "completed": len(results),
        "duration_ms": round(duration),
        "results": results,
    }

@router.get("/history", response_model=List[dict])
async def get_history(limit: int = 20):
    """Get agent run history"""
    return RUN_HISTORY[-limit:]

@router.get("/status")
async def get_orchestrator_status():
    """Get overall orchestrator status"""
    running = len([a for a in AGENTS if a["status"] == "running"])
    completed = len([a for a in AGENTS if a["status"] == "completed"])
    idle = len([a for a in AGENTS if a["status"] == "idle"])
    
    return {
        "total_agents": len(AGENTS),
        "running": running,
        "completed": completed,
        "idle": idle,
        "last_update": datetime.utcnow().isoformat() + "Z",
        "n8n_url": "http://n8n:5678",
    }

@router.get("/workflows")
async def get_workflows():
    """Get predefined N8N workflows"""
    return {
        "workflows": [
            {"id": " wf-order", "name": "New Order", "trigger": "order.created", "agents": ["agent-03", "agent-04", "agent-10", "agent-05"]},
            {"id": "wf-sourcing", "name": "Daily Sourcing", "trigger": "cron(0 9 * *)", "agents": ["agent-01", "agent-08", "agent-02"]},
            {"id": "wf-support", "name": "Support Ticket", "trigger": "ticket.created", "agents": ["agent-07"]},
            {"id": "wf-report", "name": "Daily Report", "trigger": "cron(0 18 * *)", "agents": ["agent-09", "agent-12"]},
        ]
    }