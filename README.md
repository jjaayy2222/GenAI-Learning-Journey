# 🌱 GenAI Learning Journey

> 🚀 **생성형 AI 학습 및 실습 프로젝트**  
> OpenAI API 기반 프롬프트 엔지니어링, 데이터베이스 연동, 실습 코드, 자동화 스크립트가 포함된 체계적인 GenAI 학습 저장소입니다.

> **생성형 AI 전문가로 성장하는 개인 학습 기록**  
> 기초부터 실전까지, 나만의 체계적 학습 여정

📚 **주요 구성**: ChatGPT 기초 실습, 데이터베이스 연동 시스템, Git 자동화 도구, 문서화 체계  
⚡ **자동 커밋**: `python3 scripts/gen_genai_commit.py`로 Jay 스타일 커밋 메시지 자동 생성

---

## 🎯 현재 학습 상황

- ✅ **ChatGPT 기초 (#1.x)** - OpenAI API 완전 정복 및 Git 자동화 시스템 구축
- ✅ **데이터베이스 연동 (#2.x)** - MySQL, SQLite, Python 연동, AI-DB 융합 시스템 완성
- 🔄 **웹 크롤링 (#3.x)** - 실시간 정보 검색 시스템 (준비 중)
- 📋 **04~08 과정** - LangChain, RAG 등 고급 과정 순차 진행 예정

---

## 🛠️ 기술 스택

### AI & 데이터베이스 (#2.x)  
- **OpenAI GPT-4**: 프롬프트 엔지니어링, 자연어 처리, Tool Call 활용
- **MySQL**: 관계형 데이터베이스 관리 시스템  
- **SQLite**: 경량형 파일 기반 데이터베이스
- **pymysql**: Python MySQL 연동 라이브러리
- **python-dotenv**: 환경변수 보안 관리
- **tabulate**: 데이터 테이블 포맷팅
- **AI-DB 융합**: ChatGPT와 SQL 연동 자연어 질의응답 시스템 구축 🔥

### 개발 도구 & 자동화
- **Git 자동화**: 커밋 메시지 자동 생성 시스템 (10개 타입 지원)
- **모듈화 설계**: 관심사 분리 및 재사용 가능한 구조
- **환경변수 보안**: .env 기반 민감 정보 관리

---

## 🚀 지금 바로 시작하기

```
# 저장소 복제
git clone https://github.com/jjaayy2222/GenAI-Learning-Journey.git
cd GenAI-Learning-Journey

# 환경 설정 (pyenv 사용자)
pyenv virtualenv 3.11 gen_env
pyenv activate gen_env
pip install -r requirements.txt

# API 키 설정
echo "OPENAI_API_KEY=sk-your-key"               >> .env
echo "DB_HOST=localhost"                        >> .env
echo "DB_USER=root"                             >> .env
echo "DB_PASSWORD=your_password"                >> .env
echo "DB_NAME=test_db"                          >> .env

# 첫 번째 모듈 시작!
cd 선택_GenAI/01_ChatGPT_basic
```

---

## 🎯 주요 학습 성과

### 🤖 ChatGPT 기초 마스터 (#1.x)
- **10개 전문 문서** - OpenAI API 기초부터 고급 활용까지 완전 정복
- **프롬프트 엔지니어링** - 6가지 핵심 원칙, CoT, Few-shot 등 실전 기법
- **Git 자동화 시스템** - Jay 스타일 커밋 메시지 자동 생성 (3종 스크립트)

### 🗄️ 데이터베이스 & SQL 마스터 (#2.x)  
- **MySQL 기초**: 관계형 데이터베이스 구조 및 외래키 제약조건 완전 이해
- **SQLite 활용**: 파일 기반 DB 구축 (schema.sql → scripts.sql → test.db)
- **Python-DB 연동**: pymysql 활용한 안전한 데이터베이스 연결 시스템
- **AI-DB 융합**: **ChatGPT와 SQL 연동 자연어 질의응답 시스템 구축** 🔥

#### 💡 구축된 AI-DB 시스템
- **자연어 DB 조회**: "홍길동 고객 주문 내역" → 자동 SQL 생성 → 결과 해석
- **완전 자동화**: 사용자 질문부터 최종 답변까지 무인 처리
- **보안 강화**: .env 환경변수 기반 DB 접속 관리

---

## 📁 프로젝트 구조

### 핵심 디렉터리
```
GenAI-Learning-Journey/
├── docs/
│   ├── concepts/                       # 핵심 개념 정리 (데이터베이스, SQL 등)
│   ├── practice/                       # 실습 결과 및 단계별 학습 기록
|   |   └── /05_LLM_data_services/      # 4단계 DB 실습 완성
│   ├── troubleshooting/                # 문제 해결 과정 및 개선 방안
│   ├── changelog/                      # 주요 마일스톤 및 학습 기록
│   └── papers/                         # 참고 논문 (수집 중)
|
├── scripts/                            # Git 자동화 스크립트 (3종)
|
├── 선택_GenAI/
│   ├── 01_ChatGPT_basic/               # ✅ OpenAI API 완전 마스터
│   ├── 05_LLM_data_services/           # ✅ 데이터베이스 연동 시스템
│   │   ├── 01_ChatGPT와_챗봇/            # ChatGPT 기본 활용
│   │   └── 02_데이터_기반_서비스/           # DB 4단계 실습 완성
│   └── 06_LangChain_LangGraph/         # 📋 다음 목표
|
└── 공통/                      
```

---

## 📚 완성된 학습 자료

### 🎓 01_ChatGPT_basic (100% 완료)
**10개 전문 문서로 OpenAI API 완전 마스터!**
- API 기초부터 고급 최적화까지
- 프롬프트 엔지니어링 실전 기법  
- [📂 바로 시작하기](./선택_GenAI/01_ChatGPT_basic/)

### 🗄️ 05_LLM_data_services (80% 완료)
**MySQL부터 AI-DB 융합까지 체계적 학습!**

#### ✅ 완성된 모듈
- **01_ChatGPT와_챗봇**: ChatGPT 기본 활용 및 API 연동
- **02_데이터_기반_서비스 (/1-4/)**: 4단계 데이터베이스 실습
  - `MySQL` 기초 및 환경 설정
  - `MySQL` 파일 시스템 구축  
  - `Python-MySQL` 연동 시스템
  - **ChatGPT-SQL 자연어 질의응답 시스템** 🚀

#### 📋 다음 목표 
- **02_데이터_기반_서비스 (/5/)**: `웹 크롤링 + ChatGPT` 연동

### 📖 체계적 문서화
```
docs/
├── concepts/
│   └── database_sql_and_env_setup.md       # MySQL 기초 완전 가이드
├── practice/05_LLM_data_services/
│   └── 02_databased_services/
│       ├── 2_sql.md                        # MySQL 기본 개념 실습
│       ├── 3_sql_and_python.md             # Python과 연동 실습
│       └── 4_sql_and_chatgpt.md            # AI-DB 융합 실습
└── troubleshooting/
    └── commit-automation-issues.md         # Git 자동화 개선 방안
```

---

## 🛠️ 자동화 도구

### Git 커밋 자동화 시스템
```
# 커밋 로그 추출
./scripts/extract_genai_commits.sh

# 자동 커밋 (Jay 스타일 메시지 생성)
python3 scripts/gen_genai_commit.py
```

**주요 기능:**
- ✅ **10개 커밋 타입 지원**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`
- ✅ **동적 제목 생성**: 파일명 기반 의미있는 커밋 메시지
- ✅ **사용자 편집 기능**: 검토 및 수정 가능
- ✅ **자동 로그 저장**: `changelog` 자동 생성

---

## 🎯 다음 단계 계획

### 🔄 진행 예정 (#3.x)
1. **웹 크롤링 시스템** - 실시간 정보 검색 + ChatGPT 연동
2. **LangChain & LangGraph** - 고급 AI 워크플로우 구축
3. **RAG 시스템 구현** - 문서 기반 질의응답 시스템

### 🎯 장기 목표
- **완전한 AI 어시스턴트 구축**: DB + 웹 검색 + 문서 RAG 통합 시스템
- **실전 프로젝트 적용**: 학습 내용 기반 실무 프로젝트
- **커뮤니티 기여**: 다른 학습자들과 경험 공유

---

## 🤝 함께 성장하기

- **🔧 개선 제안**: 더 좋은 아이디어 있으면 언제든지
- **📊 학습 공유**: 같이 학습하는 분들과 경험 나누기
- **🤖 실전 적용**: 구축된 시스템의 실무 활용 사례 공유

---

**⚡ 지금 시작하세요!**
- **ChatGPT 기초**: [01_ChatGPT_basic](./선택_GenAI/01_ChatGPT_basic/)
- **데이터베이스 연동**: [05_LLM_data_services](./선택_GenAI/05_LLM_data_services/)  
- **자동화 도구**: [scripts/](./scripts/)

---

- **📅 마지막 업데이트**: 2025-08-03  |  **🌱 개인 학습 프로젝트 - 지속적 성장 중**

---