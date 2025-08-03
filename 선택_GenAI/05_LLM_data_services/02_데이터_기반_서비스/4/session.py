# session.py
import os
import pymysql
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경변수에서 MySQL 접속 정보 불러오기
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'test_db')

# MySQL 연결 객체 생성
conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor,                                     # DictCursor도 가능
)