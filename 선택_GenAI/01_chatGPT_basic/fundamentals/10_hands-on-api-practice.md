# 10. 실전 API 활용 예제와 부트캠프 연계 실습

📁 위치: /GenAI-Learning-Journey/선택과정_생성형AI/01_ChatGPT_basic/10_hands-on-api-practice.md  
📅 정리일: 2025-08-02  
📚 출처: OpenAI API Documentation + 부트캠프 실습 커리큘럼 연계

---

## 🎯 학습 목표

> OpenAI API의 실전 활용법을 단계별 예제를 통해 학습하고,  
> 부트캠프 프로젝트에 직접 적용할 수 있는 구체적인 구현 능력을 습득한다.

---

## 🛠 개발 환경 설정

### 1. 가상환경 및 패키지 설치

```
# 가상환경 생성
python -m venv genai_env

# 활성화
# Windows:
genai_env\Scripts\activate
# macOS/Linux:
source genai_env/bin/activate

# 필수 패키지 설치
pip install openai python-dotenv requests pandas streamlit
```

### 2. API 키 설정

```
# .env 파일 생성
OPENAI_API_KEY=sk-proj-your-api-key-here

# Python에서 사용
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

### 3. 기본 클라이언트 설정

```
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 연결 테스트
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=10
    )
    print("✅ API 연결 성공!")
    print("응답:", response.choices.message.content)
except Exception as e:
    print("❌ API 연결 실패:", str(e))
```

---

## 📚 핵심 활용 패턴

### 1. 기본 대화형 AI

```
def basic_chat(user_input):
    """간단한 채팅 함수"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices.message.content
    
    except Exception as e:
        return f"오류 발생: {str(e)}"

# 사용 예시
user_question = "Python에서 리스트와 튜플의 차이점은?"
answer = basic_chat(user_question)
print(f"질문: {user_question}")
print(f"답변: {answer}")
```

### 2. 텍스트 요약 시스템

```
def summarize_text(text, summary_length="short"):
    """텍스트 요약 함수"""
    
    length_instructions = {
        "short": "3-5줄로 간단히",
        "medium": "한 문단(5-8줄)으로", 
        "long": "2-3문단으로 상세히"
    }
    
    prompt = f"""
다음 텍스트를 {length_instructions.get(summary_length, "간단히")} 요약해주세요:

원문:
{text}

요약 시 다음을 포함해주세요:
- 핵심 주제와 메시지
- 주요 데이터나 수치 (있는 경우)
- 결론 또는 시사점
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.3
        )
        
        return response.choices.message.content
    
    except Exception as e:
        return f"요약 중 오류 발생: {str(e)}"

# 사용 예시
long_article = """
[긴 기사나 문서 텍스트]
"""

summary = summarize_text(long_article, "medium")
print("📄 요약 결과:")
print(summary)
```

### 3. 감정 분석 도구

```
def analyze_sentiment(text):
    """감정 분석 함수"""
    
    prompt = f"""
다음 텍스트의 감정을 분석하고 JSON 형식으로 결과를 제공해주세요:

텍스트: "{text}"

결과 형식:
{{
    "sentiment": "긍정/부정/중립",
    "confidence": 0.85,
    "emotions": ["기쁨", "만족"],
    "keywords": ["좋다", "만족"],
    "explanation": "분석 근거 설명"
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.1
        )
        
        import json
        result = json.loads(response.choices.message.content)
        return result
    
    except Exception as e:
        return {"error": f"분석 중 오류: {str(e)}"}

# 사용 예시
reviews = [
    "이 제품 정말 좋아요! 추천합니다.",
    "배송이 너무 늦었어요. 실망입니다.",
    "그냥 평범한 제품이에요."
]

for review in reviews:
    result = analyze_sentiment(review)
    print(f"리뷰: {review}")
    print(f"감정: {result.get('sentiment', 'N/A')}")
    print(f"신뢰도: {result.get('confidence', 'N/A')}")
    print("---")
```

### 4. 코드 생성 및 설명

```
def generate_code(description, language="python"):
    """코드 생성 함수"""
    
    prompt = f"""
다음 요구사항에 맞는 {language} 코드를 작성해주세요:

요구사항: {description}

제공해야 할 내용:
1. 완전히 작동하는 코드
2. 코드 설명 (주석 포함)
3. 사용 예시
4. 주의사항 (있는 경우)

코드는 실행 가능하고 오류가 없어야 합니다.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.2
        )
        
        return response.choices.message.content
    
    except Exception as e:
        return f"코드 생성 중 오류: {str(e)}"

# 사용 예시
code_request = "웹사이트에서 뉴스 제목을 크롤링하는 함수"
generated_code = generate_code(code_request)
print("🔧 생성된 코드:")
print(generated_code)
```

---

## 🚀 부트캠프 연계 프로젝트

### 프로젝트 1: 스마트 문서 요약기

```
import streamlit as st
import os
from openai import OpenAI

def document_summarizer():
    """Streamlit 기반 문서 요약 웹앱"""
    
    st.title("📄 스마트 문서 요약기")
    st.write("긴 문서를 입력하면 핵심 내용을 요약해드립니다.")
    
    # 사용자 입력
    document_text = st.text_area(
        "문서 내용을 입력하세요:",
        height=300,
        placeholder="요약하고 싶은 문서나 기사를 여기에 붙여넣으세요..."
    )
    
    summary_type = st.selectbox(
        "요약 길이 선택:",
        ["짧게 (3-5줄)", "보통 (1문단)", "상세히 (2-3문단)"]
    )
    
    if st.button("📋 요약하기"):
        if document_text.strip():
            with st.spinner("요약 중..."):
                summary = summarize_text(
                    document_text, 
                    "short" if "짧게" in summary_type else
                    "medium" if "보통" in summary_type else "long"
                )
                
                st.subheader("✅ 요약 결과")
                st.write(summary)
                
                # 토큰 사용량 표시 (선택사항)
                st.info(f"원문 길이: {len(document_text)} 문자")
                
        else:
            st.warning("문서 내용을 입력해주세요!")

# 실행: streamlit run app.py
```

### 프로젝트 2: 고객 리뷰 분석 대시보드

```
import pandas as pd
import streamlit as st
import plotly.express as px

def review_analyzer():
    """고객 리뷰 분석 도구"""
    
    st.title("🔍 고객 리뷰 감정 분석")
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "CSV 파일 업로드 (리뷰 데이터)",
        type=['csv']
    )
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("📊 데이터 미리보기:")
        st.dataframe(df.head())
        
        # 리뷰 컬럼 선택
        review_column = st.selectbox(
            "리뷰가 포함된 컬럼을 선택하세요:",
            df.columns.tolist()
        )
        
        if st.button("🚀 감정 분석 시작"):
            results = []
            progress_bar = st.progress(0)
            
            for idx, review in enumerate(df[review_column].dropna()):
                # 감정 분석 수행
                sentiment_result = analyze_sentiment(str(review))
                results.append({
                    'review': review,
                    'sentiment': sentiment_result.get('sentiment', '중립'),
                    'confidence': sentiment_result.get('confidence', 0.5)
                })
                
                # 진행률 업데이트
                progress_bar.progress((idx + 1) / len(df))
            
            # 결과 시각화
            results_df = pd.DataFrame(results)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 감정 분포")
                sentiment_counts = results_df['sentiment'].value_counts()
                fig = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="감정별 리뷰 비율"
                )
                st.plotly_chart(fig)
            
            with col2:
                st.subheader("📈 신뢰도 분포")
                fig2 = px.histogram(
                    results_df,
                    x='confidence',
                    title="분석 신뢰도 분포",
                    nbins=20
                )
                st.plotly_chart(fig2)
            
            # 상세 결과 테이블
            st.subheader("📋 상세 분석 결과")
            st.dataframe(results_df)
            
            # CSV 다운로드
            csv = results_df.to_csv(index=False)
            st.download_button(
                "📥 결과 다운로드",
                csv,
                "sentiment_analysis_results.csv",
                "text/csv"
            )
```

### 프로젝트 3: AI 학습 어시스턴트

```
def ai_tutor():
    """AI 학습 도우미"""
    
    st.title("🎓 AI 학습 어시스턴트")
    
    # 학습 모드 선택
    mode = st.selectbox(
        "학습 모드를 선택하세요:",
        ["질문답변", "개념설명", "문제생성", "코드리뷰"]
    )
    
    if mode == "질문답변":
        question = st.text_input("궁금한 것을 질문하세요:")
        difficulty = st.selectbox("난이도:", ["초급", "중급", "고급"])
        
        if st.button("💡 답변받기"):
            tutor_prompt = f"""
당신은 친절한 AI 튜터입니다. {difficulty} 수준의 학습자에게 
다음 질문에 대해 이해하기 쉽게 설명해주세요:

질문: {question}

답변 가이드라인:
- 단계별로 설명
- 구체적인 예시 포함
- 관련 개념 간단히 언급
- 추가 학습 방향 제시
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": tutor_prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            st.write("📖 **AI 튜터의 설명:**")
            st.write(response.choices.message.content)
    
    elif mode == "개념설명":
        concept = st.text_input("설명받고 싶은 개념:")
        
        if st.button("📚 개념 학습"):
            concept_prompt = f"""
다음 개념을 초보자도 이해할 수 있도록 설명해주세요:

개념: {concept}

설명 구조:
1. 간단한 정의
2. 왜 중요한지
3. 실생활 예시
4. 관련 개념들
5. 학습 팁
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": concept_prompt}],
                max_tokens=600,
                temperature=0.6
            )
            
            st.write("🧠 **개념 설명:**")
            st.write(response.choices.message.content)
    
    elif mode == "문제생성":
        topic = st.text_input("문제를 만들 주제:")
        problem_count = st.slider("문제 개수:", 1, 5, 3)
        
        if st.button("📝 문제 생성"):
            problem_prompt = f"""
{topic} 주제에 대한 연습문제 {problem_count}개를 만들어주세요.

각 문제는 다음 형식으로:
**문제 X:**
[문제 내용]

**정답:**
[정답과 간단한 해설]

난이도는 중급 수준으로 만들어주세요.
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": problem_prompt}],
                max_tokens=800,
                temperature=0.8
            )
            
            st.write("🎯 **생성된 연습문제:**")
            st.write(response.choices.message.content)
```

---

## 🔧 고급 활용 기법

### 1. 스트리밍 응답 처리

```
def streaming_chat(user_input):
    """실시간 스트리밍 응답"""
    
    print("AI: ", end="", flush=True)
    
    try:
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}],
            max_tokens=200,
            temperature=0.7,
            stream=True  # 스트리밍 활성화
        )
        
        full_response = ""
        for chunk in stream:
            if chunk.choices.delta.content is not None:
                content = chunk.choices.delta.content
                print(content, end="", flush=True)
                full_response += content
        
        print()  # 줄바꿈
        return full_response
    
    except Exception as e:
        return f"스트리밍 중 오류: {str(e)}"

# 사용 예시
user_question = "인공지능의 미래에 대해 설명해주세요."
streaming_chat(user_question)
```

### 2. 배치 처리

```
def batch_process_texts(texts, task_type="summarize"):
    """여러 텍스트 배치 처리"""
    
    results = []
    
    for i, text in enumerate(texts):
        print(f"처리 중... ({i+1}/{len(texts)})")
        
        if task_type == "summarize":
            result = summarize_text(text, "short")
        elif task_type == "sentiment":
            result = analyze_sentiment(text)
        else:
            result = "지원하지 않는 작업 유형"
        
        results.append({
            'original': text[:100] + "..." if len(text) > 100 else text,
            'result': result,
            'index': i
        })
        
        # API 호출 제한 방지를 위한 대기
        import time
        time.sleep(1)
    
    return results

# 사용 예시
text_list = [
    "첫 번째 분석할 텍스트...",
    "두 번째 분석할 텍스트...",
    "세 번째 분석할 텍스트..."
]

batch_results = batch_process_texts(text_list, "sentiment")
for result in batch_results:
    print(f"원문: {result['original']}")
    print(f"결과: {result['result']}")
    print("---")
```

### 3. 오류 처리 및 재시도

```
import time
import random

def robust_api_call(prompt, max_retries=3):
    """견고한 API 호출 (재시도 로직 포함)"""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return {
                "success": True,
                "content": response.choices.message.content,
                "attempt": attempt + 1
            }
        
        except Exception as e:
            print(f"시도 {attempt + 1} 실패: {str(e)}")
            
            if attempt < max_retries - 1:
                # 지수 백오프 대기
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"{wait_time:.1f}초 후 재시도...")
                time.sleep(wait_time)
            else:
                return {
                    "success": False,
                    "error": str(e),
                    "attempts": max_retries
                }

# 사용 예시
result = robust_api_call("간단한 프로그래밍 팁을 알려주세요.")
if result["success"]:
    print(f"✅ 성공 (시도 {result['attempt']}회)")
    print(result["content"])
else:
    print(f"❌ 실패: {result['error']}")
```

---

## 📊 성능 모니터링

### 1. 토큰 사용량 추적

```
class TokenTracker:
    """토큰 사용량 추적 클래스"""
    
    def __init__(self):
        self.total_tokens = 0
        self.requests = 0
        self.cost_per_token = 0.002 / 1000  # GPT-3.5-turbo 기준
    
    def track_request(self, response):
        """API 응답에서 토큰 사용량 추출"""
        if hasattr(response, 'usage'):
            tokens_used = response.usage.total_tokens
            self.total_tokens += tokens_used
            self.requests += 1
            
            print(f"이번 요청 토큰: {tokens_used}")
            print(f"누적 토큰: {self.total_tokens}")
            print(f"예상 비용: ${self.total_tokens * self.cost_per_token:.4f}")
    
    def get_stats(self):
        """사용 통계 반환"""
        return {
            "total_requests": self.requests,
            "total_tokens": self.total_tokens,
            "average_tokens": self.total_tokens / max(self.requests, 1),
            "estimated_cost": self.total_tokens * self.cost_per_token
        }

# 사용 예시
tracker = TokenTracker()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=50
)

tracker.track_request(response)
print("현재 통계:", tracker.get_stats())
```

---

## 🎯 부트캠프 최종 프로젝트 아이디어

### 1. 통합 AI 업무 도우미
- 문서 요약, 감정 분석, 코드 생성을 하나의 앱에 통합
- Streamlit 대시보드로 구현
- CSV/PDF 파일 업로드 지원

### 2. 스마트 고객 서비스 봇
- FAQ 자동 응답
- 감정 분석 기반 우선순위 분류
- 관리자 대시보드 포함

### 3. 교육용 AI 플랫폼
- 개인화된 학습 경로 추천
- 자동 문제 생성 및 채점
- 학습 진도 추적

### 4. 콘텐츠 자동 생성 도구
- 블로그 포스트 생성
- 소셜미디어 카피 작성
- SEO 키워드 분석 연동

---

## 💡 실전 팁 및 주의사항

### Do's (권장사항)
```
✅ API 키를 환경 변수로 안전하게 관리
✅ 적절한 오류 처리 및 사용자 피드백
✅ 토큰 사용량 모니터링으로 비용 관리
✅ 프롬프트 버전 관리 및 A/B 테스트
✅ 사용자 입력 검증 및 보안 고려
```

### Don'ts (주의사항)
```
❌ API 키를 코드에 하드코딩하지 말 것
❌ 과도한 API 호출로 비용 폭발 방지
❌ 사용자 데이터를 무분별하게 API에 전송 금지
❌ 응답 결과를 검증 없이 그대로 사용 금지
❌ 에러 처리 없이 프로덕션 배포 금지
```

### 비용 절약 팁
```
💰 비용 최적화 전략:
- GPT-3.5-turbo를 기본으로, 필요시에만 GPT-4 사용
- max_tokens 설정으로 불필요한 토큰 사용 방지
- 배치 처리로 API 호출 횟수 최소화
- 캐싱으로 중복 요청 방지
- 프롬프트 최적화로 토큰 효율성 향상
```

---

## 📋 실습 체크리스트

### 기본 설정 확인
- [ ] 가상환경 생성 및 활성화
- [ ] 필수 패키지 설치 완료
- [ ] API 키 설정 및 연결 테스트
- [ ] .env 파일 .gitignore에 추가

### 핵심 기능 구현
- [ ] 기본 채팅 기능 구현
- [ ] 텍스트 요약 기능 구현
- [ ] 감정 분석 기능 구현
- [ ] 오류 처리 로직 추가

### 고급 기능 도전
- [ ] 스트리밍 응답 구현
- [ ] 배치 처리 시스템 구축
- [ ] 토큰 사용량 모니터링
- [ ] Streamlit 웹앱 배포

### 프로젝트 완성
- [ ] 사용자 인터페이스 개선
- [ ] 성능 최적화 적용
- [ ] 문서화 및 README 작성
- [ ] 테스트 케이스 작성

---

## 🔗 관련 문서

- [01_openai-api-fundamentals.md](./01_openai-api-fundamentals.md) — API 기초 개념
- [02_prompt-engineering-principles.md](./02_prompt-engineering-principles.md) — 프롬프트 설계
- [05_agent-workflow-design.md](./05_agent-workflow-design.md) — 에이전트 워크플로우
- [09_prompt-debugging-optimization.md](./09_prompt-debugging-optimization.md) — 성능 최적화

---

## 📝 학습 노트

```
💡 오늘의 핵심 포인트:
1. 실전 프로젝트는 기본 API 호출부터 시작해서 점진적 확장
2. 오류 처리와 사용자 경험을 고려한 견고한 시스템 구축
3. 토큰 사용량 모니터링으로 비용 효율성 확보
4. Streamlit 등 도구 활용으로 빠른 프로토타입 개발

🛠 실전 적용 팁:
- 작은 기능부터 완성하고 단계적으로 확장
- 사용자 피드백을 반영한 지속적 개선
- 코드 재사용성을 고려한 모듈화 설계
- 보안과 성능을 모두 고려한 배포

🚀 다음 단계 발전 방향:
- LangChain/LangGraph와의 연동
- 벡터 데이터베이스를 활용한 RAG 시스템
- 멀티모달 AI 활용 (텍스트+이미지)
- 클라우드 배포 및 스케일링 전략
```

✅ **01_ChatGPT_basic 폴더 문서 시리즈 완성! 🎉**  
**총 10개 문서로 OpenAI API 활용의 A부터 Z까지 체계적으로 완주했습니다!**

