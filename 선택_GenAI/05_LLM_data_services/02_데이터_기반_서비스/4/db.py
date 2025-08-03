import os
import sqlite3
from dotenv import load_dotenv

# .env 파일에서 환경변수 불러오기
load_dotenv()

# 환경변수에서 DB 파일 경로 불러오기 (기본값은 "test.db")
DB_PATH = os.getenv("DB_PATH", "test.db")

# 환경변수로 지정한 SQLite DB 파일로 연결
conn = sqlite3.connect(DB_PATH)

def query_db(query: str) -> list:
    """데이터베이스에 쿼리를 실행하고 결과를 반환합니다.

    Args:
        query (str): 실행할 SQL 쿼리

    Returns:
        list: 결과 행 목록 (레코드 형태)
    """

    print("데이터 조회중...", end="")

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            result = [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"\n[ERROR] 쿼리 실행 실패: {e}")
        result = []

    print("완료", end="\n")
    return result