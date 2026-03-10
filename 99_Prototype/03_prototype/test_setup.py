#!/usr/bin/env python3
"""
Gemini Tutor CLI - 미니 버전 (테스트용)
Setup 마법사 없이 바로 실행 가능
"""

import os
import platform
from pathlib import Path

# 간단한 환경 감지
def detect_environment():
    """환경 정보 출력"""
    system = platform.system()
    arch = platform.machine()
    
    if system == "Windows":
        os_type = "windows"
    elif system == "Darwin":
        os_type = "macos"
    elif system == "Linux":
        os_type = "linux"
    else:
        os_type = "unknown"
    
    print("=" * 60)
    print("🎯 Gemini Tutor CLI - 환경 감지")
    print("=" * 60)
    print(f"✅ OS: {system} ({os_type})")
    print(f"✅ 아키텍처: {arch}")
    print(f"✅ Python 버전: {platform.python_version()}")
    print("=" * 60)
    print()


def check_dependencies():
    """필수 라이브러리 확인"""
    print("📦 필수 라이브러리 확인 중...\n")
    
    deps = {
        'google.generativeai': 'google-generativeai',
        'rich': 'rich',
        'textual': 'textual'
    }
    
    missing = []
    
    for module, package in deps.items():
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} (필요: pip install {package})")
            missing.append(package)
    
    print()
    
    if missing:
        print("=" * 60)
        print("⚠️  설치가 필요합니다. 아래 명령을 실행하세요:")
        print("=" * 60)
        print(f"pip install {' '.join(missing)}")
        print("=" * 60)
        return False
    else:
        print("✅ 모든 라이브러리가 설치되어 있습니다!\n")
        return True


def show_quick_setup():
    """빠른 Setup 가이드"""
    print("🔑 Gemini API 키 발급 안내\n")
    print("1. 브라우저에서 https://aistudio.google.com 접속")
    print("2. Google 계정으로 로그인")
    print("3. 좌측 '🔑 Get API key' 버튼 클릭")
    print("4. 'Create API key in new project' 선택")
    print("5. 생성된 키 복사\n")
    
    api_key = input("API 키를 입력하세요 (또는 Enter 건너뛰기) > ").strip()
    
    if api_key:
        # 설정 저장
        config_dir = Path.home() / ".g-tutor"
        config_dir.mkdir(exist_ok=True)
        
        import json
        config = {
            "llm_provider": "gemini",
            "llm_model": "gemini-2.0-flash",
            "gemini_api_key": api_key
        }
        
        with open(config_dir / "config.json", "w") as f:
            json.dump(config, f)
        
        print(f"✅ 설정이 저장되었습니다: {config_dir / 'config.json'}\n")
        return True
    else:
        print("⏭️  건너뛰었습니다.\n")
        return False


def test_gemini_api():
    """Gemini API 테스트"""
    print("🧪 Gemini API 테스트\n")
    
    try:
        import json
        import google.generativeai as genai
        
        # 설정 파일에서 API 키 로드
        config_file = Path.home() / ".g-tutor" / "config.json"
        
        if not config_file.exists():
            print("❌ 설정 파일이 없습니다.")
            print(f"📝 {config_file} 생성 필요\n")
            return False
        
        with open(config_file) as f:
            config = json.load(f)
        
        api_key = config.get("gemini_api_key")
        if not api_key:
            print("❌ API 키가 설정되지 않았습니다.\n")
            return False
        
        # API 호출 테스트
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        print("⏳ Gemini API 호출 중...")
        response = model.generate_content("안녕하세요! 이것은 테스트입니다. 한 줄로 답해주세요.")
        
        print(f"✅ API 응답 성공!")
        print(f"📝 응답: {response.text[:100]}...\n")
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}\n")
        return False


def generate_scenario_test():
    """시나리오 생성 테스트"""
    print("🎯 시나리오 생성 테스트\n")
    
    try:
        import json
        import google.generativeai as genai
        
        config_file = Path.home() / ".g-tutor" / "config.json"
        with open(config_file) as f:
            config = json.load(f)
        
        api_key = config.get("gemini_api_key")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # 간단한 시나리오 요청
        prompt = """
다음 형식으로 단계별 시나리오를 JSON으로 생성하세요:

{
    "goal": "Python 개발 환경 세팅",
    "steps": [
        {"index": 1, "title": "Python 버전 확인", "command": "python --version", "explanation": "설명"},
        {"index": 2, "title": "pip 업그레이드", "command": "pip install --upgrade pip", "explanation": "설명"}
    ]
}

위 형식대로만 JSON을 반환하세요. 추가 설명은 없이 JSON만.
"""
        
        print("⏳ 시나리오 생성 중...")
        response = model.generate_content(prompt)
        print(f"✅ 시나리오 생성 성공!\n")
        print(f"📄 응답 (처음 500자):\n{response.text[:500]}...\n")
        
    except Exception as e:
        print(f"❌ 오류: {e}\n")


def main():
    """메인 함수"""
    print("\n")
    
    # 1. 환경 감지
    detect_environment()
    
    # 2. 의존성 확인
    if not check_dependencies():
        print("💡 팁: pip install google-generativeai rich textual 을 먼저 실행하세요.\n")
        return
    
    # 3. 설정 확인/생성
    config_file = Path.home() / ".g-tutor" / "config.json"
    if not config_file.exists():
        print("⚙️  초기 설정이 필요합니다.\n")
        if not show_quick_setup():
            print("💡 나중에 이 프로그램을 다시 실행하면 설정할 수 있습니다.\n")
            return
    else:
        print(f"✅ 기존 설정을 사용합니다: {config_file}\n")
    
    # 4. API 테스트
    if test_gemini_api():
        # 5. 시나리오 생성 테스트
        response = input("시나리오 생성 테스트를 수행하시겠습니까? (y/n, 기본 y) > ").strip().lower()
        if response != 'n':
            generate_scenario_test()
    
    print("=" * 60)
    print("✅ 모든 테스트가 완료되었습니다!")
    print("=" * 60)
    print("\n다음 명령으로 전체 프로그램을 실행하세요:")
    print("python gemini_tutor_app.py\n")


if __name__ == "__main__":
    main()
