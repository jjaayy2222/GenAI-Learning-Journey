# 📚 OpenAI API 기초 완전 정복

> **OpenAI API와 프롬프트 엔지니어링의 핵심 원리부터 실전 활용까지**  
> 10개 문서로 체계적으로 학습하는 완전한 가이드

---

## 🎯 학습 목표

이 폴더를 학습하면 다음과 같은 역량을 갖추게 됩니다:
- ✅ OpenAI API 완전 마스터 (기초~고급)
- ✅ 프롬프트 엔지니어링 전문 기법
- ✅ AI 에이전트 시스템 설계 능력  
- ✅ 실전 프로젝트 구현 및 최적화

---

## 📖 문서 구성 (총 10개)

| 순서 | 문서명 | 난이도 | 권장 학습 | 핵심 내용 |
|------|--------|--------|-----------|-----------|
| 01 | [API 기초 개념](./01_openai-api-fundamentals.md) | ⭐ | 천천히 | API 구조, 모델 비교, 첫 호출 |
| 02 | [프롬프트 엔지니어링](./02_prompt-engineering-principles.md) | ⭐⭐ | 실습 중심 | 6가지 핵심 원칙, 실전 패턴 |
| 03 | [메시지 역할과 구조](./03_message-roles-and-structure.md) | ⭐⭐ | 예제 따라하기 | System/User/Assistant 활용 |
| 04 | [GPT-4.1 특성과 최적화](./04_gpt41-model-characteristics.md) | ⭐⭐⭐ | 비교 분석 | 최신 모델 특성, 성능 최적화 |
| 05 | [에이전트 워크플로우](./05_agent-workflow-design.md) | ⭐⭐⭐ | 설계 연습 | 자율 AI 시스템 설계 |
| 06 | [단계별 사고 유도 (CoT)](./06_chain-of-thought-reasoning.md) | ⭐⭐⭐ | 패턴 익히기 | 논리적 추론 과정 설계 |
| 07 | [Few-shot 학습](./07_few-shot-learning-examples.md) | ⭐⭐ | 예시 구성 | 예시 기반 학습 최적화 |
| 08 | [긴 컨텍스트 처리](./08_long-context-strategies.md) | ⭐⭐⭐ | 대용량 실습 | 1M 토큰 활용, 대용량 문서 |
| 09 | [디버깅과 최적화](./09_prompt-debugging-optimization.md) | ⭐⭐⭐⭐ | 문제 해결 | 성능 진단, 체계적 개선 |
| 10 | [실전 API 활용](./10_hands-on-api-practice.md) | ⭐⭐⭐ | 프로젝트 완성 | 코드 예제, 프로젝트 구현 |

**💡 학습 팁: 시간에 쫓기지 말고, 각 개념을 충분히 이해하고 넘어가세요!**  
**🎯 목표: 속도보다는 깊이 있는 이해와 실제 활용 능력 습득하시는 것이 좋아요!**

---

## 🚀 빠른 시작 가이드

### 1단계: 환경 설정

#### 방법 A: 기본 venv 사용
```
python -m venv genai_env
source genai_env/bin/activate  # Windows: genai_env\Scripts\activate
pip install -r requirements.txt
```

#### 방법 B: pyenv 사용자 (권장)
```<python>
# Python 버전 설정 (3.9+ 권장)
pyenv local 3.13.5 

# 가상환경 생성
pyenv virtualenv genai-learning                         # pyenv virturalenv 가상환경이름

# 가상환경 활성화
pyenv activate genai-learning                           # pyenv activate 가상환경이름

# 패키지 설치
pip install -r requirements.txt

# 가상환경 비활성화
source deactivate                                       

# 가상환경 삭제
pip uninstall genai-learning                            # pip uninstall 가상환경이름
```

#### API 키 설정
```<python>
# .env 파일 생성
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# 환경 변수로 관리
pip install python-dotenv

# 깃 추적 방지
touch .gitignore                                        # .gitignore 파일 생성 후 파일 열기

# .gitignore 파일에 .env 파일 추가
# - 루트 디렉토리에 생성되었는지 확인
# - 보통 포함되는 내용
.env
__pycache__/
*.pyc                                                   # 이후 깃 추적에 피할 내용들 포함 → `git add .gitignore`
```

### 2단계: 첫 번째 API 호출 테스트
```<python>
# hello_openai.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, OpenAI!"}],
    max_tokens=50
)

print("🎉 성공!", response.choices[0].message.content)
```

### 3단계: 학습 순서 따라가기

> 1. **01~03번 문서**: 기초 개념 확립 (필수)
> 2. **04~06번 문서**: 고급 기법 학습 (핵심)  
> 3. **07~09번 문서**: 최적화 및 실전 적용
> 4. **10번 문서**: 프로젝트 구현 및 완주!


## 🏆 학습 후 얻는 것

### 💼 실무 활용 역량
- 비즈니스 문제를 AI로 해결하는 설계 능력
- 프롬프트 최적화를 통한 비용/성능 효율화
- 대용량 데이터 처리 및 자동화 시스템 구축

### 🧠 기술적 깊이  
- GPT 모델별 특성 이해 및 최적 활용법
- Chain-of-Thought, Few-shot 등 고급 기법 마스터
- AI 에이전트 및 워크플로우 시스템 설계 역량

**⚡ 천천히, 하지만 꾸준히!** 01번 문서부터 차근차근 시작해보세요.  
**🎯 완주보다 중요한 것:** 각 단계를 **충분히 이해**하고 실제로 써먹을 수 있게 되는 것!

---

## 📊 나의 학습 진도

- [ ] 01. API 기초 개념 
- [ ] 02. 프롬프트 엔지니어링
- [ ] 03. 메시지 역할과 구조
- [ ] 04. GPT-4.1 특성과 최적화
- [ ] 05. 에이전트 워크플로우
- [ ] 06. 단계별 사고 유도 (CoT)
- [ ] 07. Few-shot 학습
- [ ] 08. 긴 컨텍스트 처리
- [ ] 09. 디버깅과 최적화  
- [ ] 10. 실전 API 활용

🏆 **모든 문서를 학습하셨습니다! 축하드립니다!** 🎉

---

## 📁 추천 프로젝트 구조

(에시) 학습 과정에서 코드를 정리할 때 다음 구조를 참고하세요: 

```
ROOT                                 # 이 경우 `GenAI-Learning-Journey`
│
├── README.md                        # 프로젝트 전체 소개 파일
│
├──  01_ChatGPT_basic/
│    │
│    ├── README.md                    # 이 파일
│    │
│    ├── fundamentals/
│    │   │
│    │   ├── 01_openai-api-fundamentals.md
│    │   │
│    │   ├── 02_prompt-engineering-principles.md
│    │   │
│    │   └── ... (나머지 8개)
│    │
│    ├── ... (나머지 문서들)
│    │
│    ├── examples/                    # 학습 중 작성한 예제 코드
│    │   ├── basic_chat.py
│    │   ├── text_summarizer.py  
│    │   ├── sentiment_analyzer.py
│    │   └── prompt_experiments.py
│    │
│    ├── projects/                    # 완성된 프로젝트
│    │   ├── document_summarizer/
│    │   ├── review_analyzer/
│    │   └── ai_tutor/
│    │
│    └── utils/                       # 재사용 가능한 유틸리티
│        ├── api_helpers.py
│        ├── token_tracker.py
│        └── prompt_templates.py
│    
├── 02_...
│
├── ...
│
├── .gitignore                   # .gitignore 
│
└── requirements.txt             # 패키지 목록

```

* **💡 TIP:** 각 문서 학습 후 관련 코드를 `examples/`에 저장해두면 나중에 참고하기 좋아요!

---

* **마지막 업데이트: 2025-08-02** | **제작: GenAI Learning Journey**
