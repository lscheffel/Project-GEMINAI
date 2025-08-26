import psycopg2.pool
from utils.config import DB_CONFIG

DB_POOL = psycopg2.pool.SimpleConnectionPool(1, 20, **DB_CONFIG)

def init_db():
    conn = DB_POOL.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id SERIAL PRIMARY KEY,
                    prompt TEXT,
                    response TEXT,
                    output_type VARCHAR(10),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
    finally:
        DB_POOL.putconn(conn)

def save_response(prompt, response, output_type):
    conn = DB_POOL.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO history (prompt, response, output_type) VALUES (%s, %s, %s)",
                (prompt, response, output_type)
            )
            conn.commit()
    finally:
        DB_POOL.putconn(conn)