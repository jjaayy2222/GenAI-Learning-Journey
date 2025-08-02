#!/usr/bin/env python3

import os
import subprocess
import json
from datetime import datetime

# =================================================
# GenAI Learning Journey - 자동 커밋 메시지 생성기
# =================================================

class GenAICommitGenerator:
    def __init__(self):
        self.project_root = "/Users/jay/GenAI-Learning-Journey"
        self.changelog_dir = f"{self.project_root}/docs/changelog"
    
    def check_git_add_status(self):
        """Git add 상태 확인 및 사용자 선택"""
        print("🔍 먼저 git add 상태를 확인해주세요!")
        print()
        
        # staged 파일 확인
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        if not result.stdout.strip():
            print("⚠️  아직 git add된 파일이 없습니다!")
            print()
            print("📋 다음 중 하나를 선택하세요:")
            print("   1. 터미널에서 'git add .' 실행 후 다시 스크립트 실행")
            print("   2. 특정 파일만 'git add <파일명>' 후 다시 실행")
            print()
            print("👋 일단 나가서 git add 하고 다시 오시면 됩니다!")
            return False
        
        # staged 파일이 있을 때
        print("✅ Git add된 파일들이 확인되었습니다!")
        staged_files = result.stdout.strip().split('\n')
        print(f"📁 Staged 파일: {len(staged_files)}개")
        for file in staged_files[:5]:
            print(f"   - {file}")
        if len(staged_files) > 5:
            print(f"   ... 외 {len(staged_files) - 5}개")
        print()
        
        print("📋 다음 중 선택해주세요:")
        print("   1. 이 파일들로 커밋 메시지 생성하기")
        print("   2. 더 많은 파일 추가하러 나가기") 
        print("   3. 일단 나가기 (언제든 다시 실행하세요)")
        print()
        
        while True:
            choice = input("🤖 선택하세요 (1/2/3): ").strip()
            
            if choice == '1':
                print("✅ 커밋 메시지 생성을 시작합니다!")
                return True
            elif choice == '2':
                print("📝 더 많은 파일을 add하고 다시 실행해주세요!")
                return False
            elif choice == '3':
                print("👋 스크립트를 나갑니다. 언제든 다시 실행해주세요!")
                return False
            else:
                print("⚠️  1, 2, 3 중 하나를 입력해주세요.")
        
    def get_git_status(self):
        """Git 상태 분석 (staged 파일만)"""
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                              capture_output=True, text=True, cwd=self.project_root)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    def analyze_changes(self, staged_files):
        """변경사항 분석 및 카테고리화 (10개 타입 완전버전)"""
        changes = {
            'feat': [],      # 새로운 기능
            'fix': [],       # 버그 수정
            'docs': [],      # 문서 변경
            'style': [],     # 코드 포맷팅, 스타일
            'refactor': [],  # 코드 리팩토링
            'test': [],      # 테스트 추가/수정
            'chore': [],     # 빌드, 패키지 관리
            'perf': [],      # 성능 개선
            'ci': [],        # CI/CD 설정
            'build': []      # 빌드 시스템, 의존성
        }
        
        for filepath in staged_files:
            if not filepath:
                continue
                
            # Jay의 프로젝트 구조에 맞춰 10개 타입으로 분류
            if 'fundamentals/' in filepath or 'examples/' in filepath:
                if 'test' in filepath.lower() or '_test.py' in filepath:
                    changes['test'].append(filepath)
                else:
                    changes['feat'].append(filepath)
            elif 'docs/' in filepath or 'README.md' in filepath:
                changes['docs'].append(filepath)
            elif '.gitignore' in filepath or 'requirements.txt' in filepath:
                changes['chore'].append(filepath)
            elif 'scripts/' in filepath:
                if 'ci' in filepath or 'github' in filepath:
                    changes['ci'].append(filepath)
                else:
                    changes['build'].append(filepath)
            elif '.github/' in filepath or 'Dockerfile' in filepath:
                changes['ci'].append(filepath)
            elif filepath.endswith('.py') and ('fix' in filepath.lower() or 'bug' in filepath.lower()):
                changes['fix'].append(filepath)
            elif filepath.endswith('.py') and 'refactor' in filepath.lower():
                changes['refactor'].append(filepath)
            elif 'performance' in filepath.lower() or 'perf' in filepath.lower():
                changes['perf'].append(filepath)
            elif filepath.endswith('.css') or filepath.endswith('.scss') or 'style' in filepath:
                changes['style'].append(filepath)
            else:
                changes['feat'].append(filepath)  # 기본값
                
        return changes
    
    def get_next_commit_number(self):
        """다음 커밋 번호 자동 계산"""
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        if result.stdout:
            last_commit = result.stdout.strip()
            # Jay 스타일: feat[#1.5] 패턴에서 숫자 추출
            import re
            match = re.search(r'#(\d+)\.(\d+)', last_commit)
            if match:
                major, minor = int(match.group(1)), int(match.group(2))
                return f"#{major}.{minor + 1}"
        
        return "#1.1"
    
    def generate_smart_title(self, change_type, files):
        """컨텍스트 기반 스마트 제목 생성"""
        if not files:
            return "일반 업데이트"
        
        first_file = files[0]
        
        # GenAI 프로젝트 특화 제목 생성
        if 'examples/' in first_file:
            filename = first_file.split('/')[-1].replace('.py', '')
            if 'basic_chat' in filename:
                return "기본 채팅 기능 구현"
            elif 'summarizer' in filename:
                return "텍스트 요약 기능 개발"
            elif 'hello' in filename:
                return "OpenAI API 연결 테스트"
            else:
                return f"{filename} 실습 완료"
                
        elif 'fundamentals/' in first_file:
            filename = first_file.split('/')[-1].replace('.md', '')
            return f"{filename.replace('-', ' ')} 개념 학습"
            
        elif 'docs/practice/' in first_file:
            return "실습 결과 분석 및 정리"
            
        elif 'scripts/' in first_file:
            return "Git 자동화 시스템 구축"
            
        elif '.gitignore' in first_file:
            return "프로젝트 환경 설정 정비"
            
        else:
            # 기본값: 파일명 기반
            filename = first_file.split('/')[-1]
            return f"{filename} 작업 완료"
    
    def generate_commit_message(self, changes):
        """Jay 스타일 커밋 메시지 생성 (동적 제목)"""
        commit_num = self.get_next_commit_number()
        messages = []
        message_count = 0
        
        for change_type in ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf', 'ci', 'build']:
            if changes[change_type]:
                # 메시지 번호 계산
                if message_count == 0:
                    type_num = commit_num
                else:
                    base_num = int(commit_num.split('.')[0][1:])
                    minor_num = int(commit_num.split('.')[1]) + message_count
                    type_num = f"#{base_num}.{minor_num}"
                
                # 동적 제목 생성 (고정 제목 대신!)
                smart_title = self.generate_smart_title(change_type, changes[change_type])
                
                type_msg = f"- {change_type}[{type_num}]: {smart_title}\n\n"
                for file in changes[change_type][:3]:
                    type_msg += f"- {file}: 작업 완료\n"
                messages.append(type_msg.strip())
                message_count += 1
        
        return "\n\n".join(messages) if messages else f"- update[{commit_num}]: 일반 업데이트"
    
    def review_and_edit_commit_message(self, commit_message):
        """커밋 메시지 검토 및 편집"""
        print(f"📝 생성된 커밋 메시지:")
        print("-" * 40)
        print(commit_message)
        print("-" * 40)
        
        while True:
            print("\n📋 다음 중 선택해주세요:")
            print("   1. 이 메시지로 커밋하기")
            print("   2. 커밋 메시지 수정하기")
            print("   3. 커밋 취소하기")
            print()
            
            choice = input("🤖 선택하세요 (1/2/3): ").strip()
            
            if choice == '1':
                return commit_message  # 원본 그대로 사용
                
            elif choice == '2':
                # 수정 모드
                print("\n✏️  커밋 메시지 수정 모드")
                print("📋 현재 메시지를 복사해서 수정하거나, 새로 작성하세요:")
                print("💡 팁: 여러 줄 입력은 빈 줄로 끝내세요")
                print()
                
                # 사용자 입력 받기
                edited_lines = []
                print("커밋 메시지 입력 (빈 줄로 완료):")
                
                while True:
                    line = input()
                    if line == "":  # 빈 줄이면 입력 완료
                        break
                    edited_lines.append(line)
                
                if edited_lines:
                    edited_message = "\n".join(edited_lines)
                    print("\n📝 수정된 커밋 메시지:")
                    print("-" * 40)
                    print(edited_message)
                    print("-" * 40)
                    
                    confirm = input("\n✅ 이 수정된 메시지를 사용하시겠습니까? (y/n): ")
                    if confirm.lower() in ['y', 'yes']:
                        return edited_message
                    # n이면 다시 선택지로 돌아감
                else:
                    print("⚠️  메시지가 비어있습니다. 다시 선택해주세요.")
                    
            elif choice == '3':
                print("❌ 커밋이 취소되었습니다.")
                return None
                
            else:
                print("⚠️  1, 2, 3 중 하나를 입력해주세요.")
    
    def execute_commit(self):
        """자동 커밋 실행 (편집 기능 포함)"""
        print("🚀 GenAI Learning Journey 자동 커밋 생성기")
        print("=" * 50)
        
        # git add 상태 확인 (개선된 버전)
        if not self.check_git_add_status():
            return  # 사용자가 나가기를 선택하면 종료
        
        # Git 상태 확인 (staged 파일만)
        staged_files = self.get_git_status()
        
        if not staged_files or not staged_files[0]:
            print("✅ 커밋할 staged 파일이 없습니다.")
            return
            
        # 변경사항 분석
        changes = self.analyze_changes(staged_files)
        
        # 커밋 메시지 생성
        commit_message = self.generate_commit_message(changes)
        
        # 검토 및 편집 단계 
        final_message = self.review_and_edit_commit_message(commit_message)
        
        if final_message is None:  # 사용자가 취소한 경우
            return
        
        # Git commit 실행
        result = subprocess.run(['git', 'commit', '-m', final_message], 
                              capture_output=True, text=True, cwd=self.project_root)
        
        if result.returncode == 0:
            print("✅ 커밋이 완료되었습니다!")
            self.save_commit_log(final_message)
        else:
            print("❌ 커밋 중 오류가 발생했습니다:")
            print(result.stderr)
    
    def save_commit_log(self, message):
        """커밋 로그 저장"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = f"{self.changelog_dir}/auto-commit-{today}.md"
        
        os.makedirs(self.changelog_dir, exist_ok=True)
        
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n## {timestamp}\n")
            f.write(f"{message}\n")
            f.write("-" * 50 + "\n")

if __name__ == "__main__":
    generator = GenAICommitGenerator()
    generator.execute_commit()
