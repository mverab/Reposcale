"""Database access — raw SQL, no connection pooling."""

import psycopg2

# Hardcoded connection — no env vars
DB_HOST = "db.internal.company.com"
DB_NAME = "platform_prod"
DB_USER = "app"
DB_PASS = "s3cret_prod_password"


def get_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )


def query(sql: str, params=None) -> list[dict]:
    conn = get_connection()  # New connection per query — no pooling
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        conn.close()


def execute(sql: str, params=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()
