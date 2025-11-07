# reports/reports.py
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "recipe_db")

def get_ingredient_usage():
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME, port=DB_PORT, charset='utf8mb4')
    try:
        with conn.cursor() as cur:
            cur.callproc('sp_get_ingredient_usage')
            result = cur.fetchall()
            print("Ingredient usage (ingredient_id, name, unit, total_quantity):")
            for row in result:
                print(row)
    finally:
        conn.close()

def top_recipes_by_ingredient_count(limit=5):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME, port=DB_PORT, charset='utf8mb4')
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT r.id, r.title, COUNT(ri.id) AS ingredient_count
                FROM recipes r
                LEFT JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                GROUP BY r.id, r.title
                ORDER BY ingredient_count DESC
                LIMIT %s;
            """, (limit,))
            rows = cur.fetchall()
            print("Top recipes by ingredient count:")
            for r in rows:
                print(r)
    finally:
        conn.close()

if __name__ == "__main__":
    get_ingredient_usage()
    print()
    top_recipes_by_ingredient_count(10)
