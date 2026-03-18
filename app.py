from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

app = FastAPI()

# Set up templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE = 'identity_management.db'

# Ensure database and tables are created
if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        did TEXT,
                        credentials TEXT
                    )''')
    cursor.execute('''CREATE TABLE credentials (
                        id TEXT PRIMARY KEY,
                        type TEXT,
                        issuer TEXT,
                        issued_date TEXT
                    )''')
    cursor.execute('''CREATE TABLE verifications (
                        id TEXT PRIMARY KEY,
                        identity_id TEXT,
                        status TEXT,
                        timestamp TEXT
                    )''')
    # Insert seed data
    cursor.execute("INSERT INTO users (id, name, did, credentials) VALUES (?, ?, ?, ?)",
                   ('1', 'Alice', 'did:example:123', '[]'))
    cursor.execute("INSERT INTO credentials (id, type, issuer, issued_date) VALUES (?, ?, ?, ?)",
                   ('1', 'email', 'example.com', '2023-01-01'))
    cursor.execute("INSERT INTO verifications (id, identity_id, status, timestamp) VALUES (?, ?, ?, ?)",
                   ('1', '1', 'verified', '2023-01-02T10:00:00Z'))
    conn.commit()
    conn.close()

# Models
class User(BaseModel):
    id: str
    name: str
    did: str
    credentials: List[str]

class Credential(BaseModel):
    id: str
    type: str
    issuer: str
    issued_date: str

class Verification(BaseModel):
    id: str
    identity_id: str
    status: str
    timestamp: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/create-identity", response_class=HTMLResponse)
async def create_identity_page():
    return templates.TemplateResponse("create_identity.html", {"request": {}})

@app.get("/manage-identities", response_class=HTMLResponse)
async def manage_identities_page():
    return templates.TemplateResponse("manage_identities.html", {"request": {}})

@app.get("/verify-identity", response_class=HTMLResponse)
async def verify_identity_page():
    return templates.TemplateResponse("verify_identity.html", {"request": {}})

@app.get("/api-docs", response_class=HTMLResponse)
async def api_docs_page():
    return templates.TemplateResponse("api_docs.html", {"request": {}})

@app.post("/api/identities")
async def create_identity(user: User):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, name, did, credentials) VALUES (?, ?, ?, ?)",
                   (user.id, user.name, user.did, str(user.credentials)))
    conn.commit()
    conn.close()
    return {"message": "Identity created successfully"}

@app.get("/api/identities/{id}")
async def get_identity(id: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "name": user[1], "did": user[2], "credentials": user[3]}
    raise HTTPException(status_code=404, detail="Identity not found")

@app.put("/api/identities/{id}")
async def update_identity(id: str, user: User):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, did = ?, credentials = ? WHERE id = ?",
                   (user.name, user.did, str(user.credentials), id))
    conn.commit()
    conn.close()
    return {"message": "Identity updated successfully"}

@app.delete("/api/identities/{id}")
async def delete_identity(id: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Identity deleted successfully"}

@app.post("/api/verify")
async def verify_identity(verification: Verification):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO verifications (id, identity_id, status, timestamp) VALUES (?, ?, ?, ?)",
                   (verification.id, verification.identity_id, verification.status, verification.timestamp))
    conn.commit()
    conn.close()
    return {"message": "Identity verified successfully"}

