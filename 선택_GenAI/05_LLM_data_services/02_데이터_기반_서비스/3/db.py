# GenAI-Learning-Journey/선택_GenAI/05_LLM_data_services/02_데이터_기반_서비스/3/db.py

import os
from dotenv import load_dotenv
import pymysql

# .env 파일이 프로젝트 루트에 있으므로 기본 load_dotenv() 사용
load_dotenv()  

# 환경변수에서 DB 접속 정보 읽기
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')                                  # 비밀번호가 없으면 빈 문자열
DB_NAME = os.getenv('DB_NAME', 'test_db')

def get_connection():
    """MySQL DB 연결 생성 및 반환"""
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def query_db(query: str) -> list:
    """DB에 쿼리 실행 후 결과 리스트 반환

    Args:
        query (str): 실행할 SQL 쿼리 문자열

    Returns:
        list: 결과 레코드 리스트 (딕셔너리 형태)
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()                               # 이미 DictCursor라 딕셔너리 리스트로 반환됨
    except Exception as e:
        print(f"DB query error: {e}")
        result = []
    finally:
        conn.close()
    return result