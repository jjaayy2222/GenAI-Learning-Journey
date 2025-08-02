#!/bin/bash

# =================================================
# GenAI Learning Journey - 커밋 로그 추출 스크립트
# =================================================

# 프로젝트 루트 경로
PROJECT_ROOT="/Users/jay/GenAI-Learning-Journey"
CHANGELOG_DIR="$PROJECT_ROOT/docs/changelog"

# 현재 날짜
TODAY=$(date +"%Y-%m-%d")
LOG_FILE="$CHANGELOG_DIR/genai-commits-$TODAY.md"

echo "🚀 GenAI Learning Journey 커밋 로그 추출 시작..."
echo "📅 날짜: $TODAY"
echo "📁 로그 파일: $LOG_FILE"

# 프로젝트 루트로 이동
cd "$PROJECT_ROOT" || exit 1

# 커밋 로그 추출 (Jay 스타일 유지)
echo "# GenAI Learning Journey 커밋 로그 - $TODAY" > "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 최근 10개 커밋 추출
echo "## 📋 최근 커밋 히스토리" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
git log --oneline -10 --pretty=format:"- %h: %s" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 오늘 커밋만 추출
echo "## 🎯 오늘의 커밋 ($TODAY)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
git log --since="$TODAY 00:00:00" --until="$TODAY 23:59:59" --pretty=format:"- %h: %s" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 변경된 파일 통계
echo "## 📊 변경 파일 통계" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
git log --since="$TODAY 00:00:00" --name-only --pretty=format: | sort | uniq -c | sort -nr >> "$LOG_FILE"

echo "✅ 커밋 로그 추출 완료!"
echo "📄 생성된 파일: $LOG_FILE"
