import psycopg
import os
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
db_name = os.getenv("DB_NAME")


# 환경변수를 이용한 DB연결정보
DB_CONFIG = {
        "user": os.getenv("DB_USERNAME"),
        "dbname": db_name,
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
}

# DB연결
def get_connection():
    return psycopg.connect(**DB_CONFIG)

# DB삽입
def insert_menu(menu_name, member_name, dt):
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                    "INSERT INTO lunch_menu(menu_name, member_name, dt) VALUES (%s, %s, %s);",
                    (menu_name, member_name, dt)
                    )
            conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Exception{e}")
        return False
    finally:
        conn.close()
# 통계를 위한 데이터 불러오기
def select_table():
    query = """SELECT
    menu_name AS menu,
    name AS ename,
    dt
    FROM lunch_menu as l left join member as m on l.member_name = m.id
    ORDER BY dt DESC"""
    
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
    select_df = pd.DataFrame(rows, columns=['menu','ename','dt'])
    return select_df
