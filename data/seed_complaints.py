"""
data/seed_complaints.py
------------------------
Seeds 25 sample complaints into the Endee vector database.

Run from the project root:
    python data/seed_complaints.py
"""

from __future__ import annotations

import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from endee import EndeeDB
from sentence_transformers import SentenceTransformer

COMPLAINTS = [
    # delivery (5)
    {"text": "My order was supposed to arrive within 3-5 days but it has been 2 weeks and I still have not received it.", "category": "delivery"},
    {"text": "The package was delivered to the wrong address. My neighbour found it on their doorstep.", "category": "delivery"},
    {"text": "Delivery driver marked the parcel as delivered but I was home all day and nothing arrived.", "category": "delivery"},
    {"text": "My order arrived completely crushed. The box was clearly damaged during transit.", "category": "delivery"},
    {"text": "I paid for express shipping but my order arrived 5 days late. I want a refund on the shipping fee.", "category": "delivery"},
    # billing (5)
    {"text": "I was charged twice for the same order on my credit card. Please refund the duplicate charge immediately.", "category": "billing"},
    {"text": "The discount code I applied was not reflected in my final invoice. I was charged full price.", "category": "billing"},
    {"text": "I cancelled my subscription but I was still charged for the next month.", "category": "billing"},
    {"text": "There are unexplained charges on my bill that were never disclosed at checkout.", "category": "billing"},
    {"text": "I requested a refund 3 weeks ago but the money has not appeared in my account yet.", "category": "billing"},
    # product (5)
    {"text": "The laptop I received has a cracked screen right out of the box. It was clearly not inspected.", "category": "product"},
    {"text": "The headphones stopped working after just one week of normal use. The sound cuts out randomly.", "category": "product"},
    {"text": "I received a completely different product from what I ordered. The colour and size are wrong.", "category": "product"},
    {"text": "The blender blade broke after the second use. Quality is far below what was advertised.", "category": "product"},
    {"text": "The clothing item shrank significantly after the first wash despite following care instructions.", "category": "product"},
    # support (5)
    {"text": "I have been waiting on hold for over an hour to speak to a customer service representative.", "category": "support"},
    {"text": "The chatbot could not resolve my issue and I was never transferred to a human agent.", "category": "support"},
    {"text": "I sent three emails about my problem and have received no response in over a week.", "category": "support"},
    {"text": "The support agent was rude and dismissive when I explained my situation.", "category": "support"},
    {"text": "I was promised a callback within 24 hours but nobody ever called me back.", "category": "support"},
    # account (3)
    {"text": "I cannot log into my account even after resetting my password multiple times.", "category": "account"},
    {"text": "My account was locked without any explanation. I have not violated any terms of service.", "category": "account"},
    {"text": "Someone made unauthorised purchases using my account. I need this investigated immediately.", "category": "account"},
    # returns (2)
    {"text": "I initiated a return 4 weeks ago and the refund has still not been processed.", "category": "returns"},
    {"text": "The return label provided was invalid. The courier refused to accept my parcel.", "category": "returns"},
]


def seed():
    db_path = ROOT / "data" / "complaints.jsonl"
    if db_path.exists() and db_path.stat().st_size > 0:
        print(f"Database already exists at {db_path}. Skipping seed.")
        print("Delete data/complaints.jsonl and re-run to reseed.")
        return

    print("Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    db = EndeeDB(str(db_path))

    print(f"Seeding {len(COMPLAINTS)} complaints into Endee...\n")
    for i, c in enumerate(COMPLAINTS, 1):
        vector = model.encode(c["text"], normalize_embeddings=True).tolist()
        db.insert(
            id=str(uuid.uuid4()),
            vector=vector,
            metadata={
                "text": c["text"],
                "category": c["category"],
                "customer_id": f"cust_{i:03d}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
        print(f"  [{i:02d}/{len(COMPLAINTS)}] [{c['category']:8s}] {c['text'][:65]}...")
        time.sleep(0.02)

    print(f"\n✓ Done — {db.count()} complaints stored in Endee at {db_path}")


if __name__ == "__main__":
    seed()
