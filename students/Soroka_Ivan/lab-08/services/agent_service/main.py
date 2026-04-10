from fastapi import FastAPI

app = FastAPI()
agents_db = {"A-1": {"name": "Иван Сорока", "status": "ONLINE"}}

@app.get("/{agent_id}")
def get_agent(agent_id: str):
    if agent_id in agents_db:
        return agents_db[agent_id]
    return {"error": "Агент не найден"}

@app.post("/")
def create_agent(name: str):
    agent_id = "A-2"
    agents_db[agent_id] = {"name": name, "status": "ONLINE"}
    return {"agent_id": agent_id, "message": "Агент создан"}