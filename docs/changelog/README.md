# 📋 Changelog & Commit Log Directory

이 폴더는 **GenAI Learning Journey** 프로젝트의 커밋 히스토리와 변경 로그를 체계적으로 관리합니다.

## 📁 파일 구조

### 🤖 자동 생성 파일들
- `genai-commits-YYYY-MM-DD.md` - 일별 커밋 로그 추출 파일
- `auto-commit-YYYY-MM-DD.md` - 자동 커밋 시스템 실행 기록

### 📝 수동 관리 파일들  
- `differences.md` - 임시 작업 메모 (삭제 예정)
- 향후 milestone 기반 changelog 추가 예정

## 🛠 생성 방법

```
# 커밋 로그 추출
./scripts/extract_genai_commits.sh

# 자동 커밋 (로그 자동 저장)
python3 scripts/gen_genai_commit.py
```

## 📊 업데이트 주기
- **자동**: 커밋 시마다 자동 기록
- **수동**: 주요 milestone 달성 시 정리
- **내용 업데이트**: 2025-08-03 예정

---

* *Last updated: 2025-08-02*