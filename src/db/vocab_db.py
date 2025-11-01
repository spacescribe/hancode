import sqlite3
from pathlib import Path
from datetime import datetime

db_path = Path(__file__).parent.parent.parent / "data" / "vocab.db"
print(f"[DEBUG] Vocabulary DB path: {db_path}")

def init_db():
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vocab(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE,
                    pinyin TEXT,
                    english TEXT,
                    example TEXT,
                    english_translation TEXT,
                    date_learned TEXT
                )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz_stats(
                word TEXT PRIMARY KEY,  
                attempts INTEGER DEFAULT 0,
                correct INTEGER DEFAULT 0,
                last_tested TEXT
            )
        """)

    return conn

def save_vocab(items):
    with sqlite3.connect(db_path) as conn:
        for it in items:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO vocab (word, pinyin, english, example, english_translation, date_learned)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (it["word"], it["pinyin"], it["english"], it["example"], it["english_translation"], datetime.now().isoformat()))
            except KeyError:
                continue