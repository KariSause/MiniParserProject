import sqlite3

DB_PATH = "database.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()



def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()

async def add_user(user_id: int):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()


async def add_keyword(user_id: int, keyword: str):
    cursor.execute("INSERT INTO keywords (keyword) VALUES (?)", (keyword.lower()))
    conn.commit()

async def get_keywords(user_id: int):
    cursor.execute("SELECT keyword FROM keywords WHERE user_id = ?", (user_id,))
    result = [row[0] for row in cursor.fetchall()]
    return result

async def delete_keyword(user_id: int, keyword: str):
    cursor.execute("DELETE FROM keywords WHERE user_id = ? AND keyword = ?", (user_id, keyword))
    conn.commit()

async def get_all_user_keywords():
    cursor.execute("SELECT user_id, keyword FROM keywords")
    data = cursor.fetchall()
    users_keywords = {}
    for user_id, kw in data:
        users_keywords.setdefault(user_id, []).append(kw)
    return users_keywords

async def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    return users