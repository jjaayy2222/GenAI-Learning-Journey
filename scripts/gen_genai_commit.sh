#!/bin/bash

# =================================================
# GenAI Learning Journey - 대화형 커밋 메시지 생성
# =================================================

PROJECT_ROOT="/Users/jay/GenAI-Learning-Journey"
CHANGELOG_DIR="$PROJECT_ROOT/docs/changelog"

echo "🚀 GenAI Learning Journey 자동 커밋 시스템"
echo "============================================"

# 프로젝트 루트로 이동
cd "$PROJECT_ROOT" || exit 1

# Git 상태 확인
echo "📊 현재 Git 상태 확인 중..."
git status --porcelain

# 변경 사항이 있는지 확인
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 커밋할 변경사항이 없습니다."
    exit 0
fi

echo ""
echo "🤖 자동 커밋 메시지를 생성할까요? (y/n)"
read -r response

if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
    echo "📝 Python 스크립트로 커밋 메시지 생성 중..."
    python3 "$PROJECT_ROOT/scripts/gen_genai_commit.py"
else
    echo "❌ 커밋 생성을 취소했습니다."
fi