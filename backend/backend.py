from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query, HTTPException
import random
import uuid
import sqlite3
import json
from dotenv import load_dotenv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("conspiracies.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS conspiracies (
    id TEXT PRIMARY KEY,
    conspiracy TEXT,
    sources TEXT
)
""")
conn.commit()

TEMPLATES = [
    "{group} secretly controls {event} to {motive}.",
    "{event} was staged by {group} to distract from {coverup}.",
    "{person} is actually a {creature} working for {group}.",
    "{technology} was invented not by {official_story}, but by {group} to {motive}.",
    "{group} has been hiding the truth about {event} since {year}."
]

GROUPS = ["the Illuminati", "the Freemasons", "a secret government agency", "lizard people"]
EVENTS = ["the moon landing", "9/11", "COVID-19", "AI advancements"]
MOTIVES = ["control the masses", "hide the existence of aliens", "manipulate the economy"]
COVERUPS = ["a secret space program", "mind-control experiments", "the real cure for cancer"]
PEOPLE = ["Elon Musk", "Mark Zuckerberg", "Taylor Swift", "The Pope"]
CREATURES = ["reptilian", "cyborg", "ancient alien", "time traveler"]
TECHNOLOGIES = ["the internet", "5G", "quantum computing", "cryptocurrency"]
OFFICIAL_STORIES = ["scientists", "government agencies", "tech companies", "aliens"]
YEARS = ["1947", "1969", "2001", "2020"]

SOURCE_TEMPLATES = [
    "https://{site}/news/{keyword}",
    "https://{site}/leaks/{keyword}",
    "https://{site}/exposed/{keyword}",
    "https://{site}/classified/{keyword}",
    "https://{site}/truth/{keyword}"
]

SITES = [
    "truthwatchers.com", "hiddenhistory.net", "deepstatefiles.org",
    "exposesecrets.info", "whistleblower.news"
]

KEYWORDS = [
    "government-coverup", "alien-technology", "secret-societies",
    "fake-moon-landing", "mind-control", "forbidden-knowledge"
]

def generate_sources():
    sources = [
        random.choice(SOURCE_TEMPLATES).format(
            site=random.choice(SITES),
            keyword=random.choice(KEYWORDS)
        )
        for _ in range(3)
    ]
    return sources

def generate_conspiracy():
    template = random.choice(TEMPLATES)
    conspiracy = template.format(
        group=random.choice(GROUPS),
        event=random.choice(EVENTS),
        motive=random.choice(MOTIVES),
        coverup=random.choice(COVERUPS),
        person=random.choice(PEOPLE),
        creature=random.choice(CREATURES),
        technology=random.choice(TECHNOLOGIES),
        official_story=random.choice(OFFICIAL_STORIES),
        year=random.choice(YEARS)
    )
    return conspiracy[0].upper() + conspiracy[1:]


load_dotenv()

PASSWORD = os.getenv("ADMIN_PASSWORD")

def verify_password(password: str):
    if password != PASSWORD:
        raise HTTPException(status_code=403, detail="Unauthorized")

@app.get("/generate")
def get_conspiracy():
    conspiracy = generate_conspiracy()
    sources = generate_sources()
    conspiracy_id = str(uuid.uuid4())
    
    cursor.execute("INSERT INTO conspiracies (id, conspiracy, sources) VALUES (?, ?, ?)",
                   (conspiracy_id, conspiracy, json.dumps(sources)))
    conn.commit()
    
    return {"id": conspiracy_id, "conspiracy": conspiracy, "sources": sources}

@app.get("/conspiracy/all")
def get_all_conspiracies(password: str = Query(...)):
    verify_password(password)

    cursor.execute("SELECT id, conspiracy, sources FROM conspiracies")
    rows = cursor.fetchall()
    
    conspiracies = [
        {"id": row[0], "conspiracy": row[1], "sources": row[2]} for row in rows
    ]
    return {"conspiracies": conspiracies}

@app.get("/conspiracy/count")
def count_conspiracies(password: str = Query(...)):
    verify_password(password)

    cursor.execute("SELECT COUNT(*) FROM conspiracies")
    count = cursor.fetchone()[0]
    return {"count": count}

@app.get("/conspiracy/{conspiracy_id}")
def get_conspiracy_by_id(conspiracy_id: str):
    cursor.execute("SELECT conspiracy, sources FROM conspiracies WHERE id = ?", (conspiracy_id,))
    row = cursor.fetchone()
    if row:
        return {"id": conspiracy_id, "conspiracy": row[0], "sources": json.loads(row[1])}
    return {"error": "Conspiracy not found"}

@app.delete("/conspiracy/empty")
def empty_conspiracies(password: str = Query(...)):
    verify_password(password)
    
    cursor.execute("DELETE FROM conspiracies")
    conn.commit()
    return {"message": "All conspiracies deleted successfully"}
