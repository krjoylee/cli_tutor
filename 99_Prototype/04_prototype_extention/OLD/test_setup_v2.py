#!/usr/bin/env python3
"""
Gemini Tutor CLI v2.0 - 테스트 & Setup 도구
Groq/Perplexity/Gemini 통합 테스트
"""

import sys
import json
import platform
from pathlib import Path

console_buffer = []

def log_info(msg: str):
    """정보 로그"""
    print(f"[INFO] {msg}")
    console_buffer.append(msg)

def log_success(msg: str):
    """성공 로그"""
    print(f"[✅] {msg}")
    console_buffer.append(msg)

def log_warning(msg: str):
    """경고 로그"""
    print(f"[⚠️] {msg}")
    console_buffer.append(msg)

def log_error(msg: str):
    """에러 로그"""
    print(f"[❌] {msg}")
    console_buffer.append(msg)


# ============================================================================
# 1. 환경 정보 출력
# ============================================================================

def show_environment_info():
    """시스템 환경 정보 출력"""
    print("\n" + "="*60)
    print("📊 시스템 환경 정보")
    print("="*60 + "\n")
    
    # OS 정보
    system = platform.system()
    release = platform.release()
    arch = platform.machine()
    processor = platform.processor()
    python_version = platform.python_version()
    python_impl = platform.python_implementation()
    
    log_info(f"OS: {system} {release}")
    log_info(f"아키텍처: {arch}")
    log_info(f"프로세서: {processor if processor else '(감지 실패)'}")
    log_info(f"Python: {python_impl} {python_version}")
    
    # WSL 확인
    if system == "Linux":
        try:
            with open("/proc/version", "r") as f:
                content = f.read()
                if "WSL" in content or "Microsoft" in content:
                    log_warning("WSL 환경 감지됨")
        except:
            pass
    
    # Python 실행 경로
    log_info(f"Python 경로: {sys.executable}")
    
    # 설정 디렉토리
    config_dir = Path.home() / ".g-tutor"
    log_info(f"설정 디렉토리: {config_dir}")
    
    print()


# ============================================================================
# 2. 의존성 확인
# ============================================================================

def check_dependencies():
    """필수 라이브러리 확인"""
    print("\n" + "="*60)
    print("📦 의존성 확인")
    print("="*60 + "\n")
    
    dependencies = [
        ("groq", "Groq API 클라이언트"),
        ("google.generativeai", "Google Gemini API"),
        ("rich", "터미널 렌더링"),
        ("textual", "TUI 프레임워크"),
        ("httpx", "HTTP 클라이언트")
    ]
    
    missing = []
    
    for module, description in dependencies:
        try:
            __import__(module)
            log_success(f"{module:20} - {description}")
        except ImportError:
            log_error(f"{module:20} - {description} [NOT INSTALLED]")
            missing.append(module)
    
    if missing:
        print(f"\n[⚠️] 다음 라이브러리를 설치하세요:")
        print(f"    pip install {' '.join(missing)}")
    else:
        log_success("모든 의존성 설치됨!")
    
    print()
    return len(missing) == 0


# ============================================================================
# 3. 설정 확인
# ============================================================================

def check_configuration():
    """저장된 설정 확인"""
    print("\n" + "="*60)
    print("⚙️ 저장된 설정 확인")
    print("="*60 + "\n")
    
    config_file = Path.home() / ".g-tutor" / "config.json"
    
    if not config_file.exists():
        log_warning(f"설정 파일이 없습니다: {config_file}")
        log_info("처음 실행할 때 setup wizard가 자동으로 실행됩니다.")
        return False
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        log_success(f"설정 파일 발견: {config_file}")
        print()
        
        # 설정값 표시
        for key, value in config.items():
            if "api_key" in key.lower():
                # API 키는 마스킹
                masked = value[:10] + "..." if len(str(value)) > 10 else "***"
                log_info(f"{key:20} = {masked}")
            else:
                log_info(f"{key:20} = {value}")
        
        return True
    
    except Exception as e:
        log_error(f"설정 파일 읽기 실패: {e}")
        return False
    
    print()


# ============================================================================
# 4. LLM API 테스트
# ============================================================================

def test_groq_api():
    """Groq API 테스트"""
    print("\n" + "="*60)
    print("🧪 Groq API 테스트")
    print("="*60 + "\n")
    
    config_file = Path.home() / ".g-tutor" / "config.json"
    if not config_file.exists():
        log_warning("설정 파일 없음. setup wizard를 먼저 실행하세요.")
        return False
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        api_key = config.get("groq_api_key")
        if not api_key:
            log_warning("Groq API 키가 설정되지 않음.")
            return False
        
        from groq import Groq
        
        log_info("Groq 클라이언트 초기화 중...")
        client = Groq(api_key=api_key)
        
        log_info("테스트 요청 전송 중... (간단한 한글 질문)")
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": "간단히 '안녕하세요'라고 인사해주세요."}
            ],
            max_completion_tokens=100
        )
        
        response = completion.choices[0].message.content
        log_success(f"응답 받음: {response}")
        
        return True
    
    except Exception as e:
        log_error(f"Groq API 테스트 실패: {e}")
        return False
    
    print()


def test_gemini_api():
    """Google Gemini API 테스트"""
    print("\n" + "="*60)
    print("🧪 Google Gemini API 테스트")
    print("="*60 + "\n")
    
    config_file = Path.home() / ".g-tutor" / "config.json"
    if not config_file.exists():
        log_warning("설정 파일 없음. setup wizard를 먼저 실행하세요.")
        return False
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        api_key = config.get("gemini_api_key")
        if not api_key:
            log_warning("Gemini API 키가 설정되지 않음.")
            return False
        
        import google.generativeai as genai
        
        log_info("Gemini 클라이언트 초기화 중...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        log_info("테스트 요청 전송 중... (간단한 한글 질문)")
        response = model.generate_content("간단히 '안녕하세요'라고 인사해주세요.")
        
        log_success(f"응답 받음: {response.text}")
        
        return True
    
    except Exception as e:
        log_error(f"Gemini API 테스트 실패: {e}")
        return False
    
    print()


def test_perplexity_api():
    """Perplexity API 테스트"""
    print("\n" + "="*60)
    print("🧪 Perplexity API 테스트")
    print("="*60 + "\n")
    
    config_file = Path.home() / ".g-tutor" / "config.json"
    if not config_file.exists():
        log_warning("설정 파일 없음. setup wizard를 먼저 실행하세요.")
        return False
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        api_key = config.get("perplexity_api_key")
        if not api_key:
            log_warning("Perplexity API 키가 설정되지 않음.")
            return False
        
        import httpx
        
        log_info("Perplexity 클라이언트 초기화 중...")
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "pplx-7b-online",
            "messages": [
                {"role": "user", "content": "간단히 '안녕하세요'라고 인사해주세요."}
            ],
            "max_tokens": 100
        }
        
        log_info("테스트 요청 전송 중...")
        response = httpx.post(
            "https://api.perplexity.ai/chat/completions",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            log_success(f"응답 받음: {content}")
            return True
        else:
            log_error(f"API 오류: {response.status_code}")
            return False
    
    except Exception as e:
        log_error(f"Perplexity API 테스트 실패: {e}")
        return False
    
    print()


# ============================================================================
# 5. Setup 마법사
# ============================================================================

def quick_setup_wizard():
    """빠른 setup 마법사"""
    print("\n" + "="*60)
    print("🎯 빠른 Setup 마법사 (Multi-LLM)")
    print("="*60 + "\n")
    
    config_file = Path.home() / ".g-tutor" / "config.json"
    config_dir = config_file.parent
    config_dir.mkdir(exist_ok=True)
    
    print("사용할 LLM을 선택하세요:\n")
    print("1) [✅ 추천] Groq - 빠르고 무료, RPM 30")
    print("2) Perplexity - 검색 기반, 최신 정보")
    print("3) Google Gemini - 한국어 우수, 일 250 요청\n")
    
    choice = input("선택 (기본: 1) > ").strip() or "1"
    
    config = {}
    
    if choice == "2":
        log_info("Perplexity 선택")
        api_key = input("Perplexity API 키를 입력하세요 > ").strip()
        if api_key:
            config["llm_provider"] = "perplexity"
            config["perplexity_api_key"] = api_key
            log_success("Perplexity 설정 저장됨")
    elif choice == "3":
        log_info("Google Gemini 선택")
        api_key = input("Gemini API 키를 입력하세요 > ").strip()
        if api_key:
            config["llm_provider"] = "gemini"
            config["llm_model"] = "gemini-2.0-flash"
            config["gemini_api_key"] = api_key
            log_success("Gemini 설정 저장됨")
    else:
        log_info("Groq 선택 (기본)")
        api_key = input("Groq API 키를 입력하세요 > ").strip()
        if api_key:
            config["llm_provider"] = "groq"
            config["llm_model"] = "openai/gpt-oss-120b"
            config["groq_api_key"] = api_key
            log_success("Groq 설정 저장됨")
    
    if config:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        log_success(f"설정 저장: {config_file}")
        return True
    else:
        log_warning("설정이 저장되지 않음")
        return False
    
    print()


# ============================================================================
# 6. 시나리오 생성 테스트
# ============================================================================

def test_scenario_generation():
    """명령어 시나리오 생성 테스트"""
    print("\n" + "="*60)
    print("🧪 명령어 시나리오 생성 테스트")
    print("="*60 + "\n")
    
    config_file = Path.home() / ".g-tutor" / "config.json"
    if not config_file.exists():
        log_warning("설정 파일 없음.")
        return False
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        provider = config.get("llm_provider")
        
        if provider == "groq":
            from groq import Groq
            api_key = config.get("groq_api_key")
            client = Groq(api_key=api_key)
            
            log_info("목표: '현재 디렉터리의 파일 목록 보기'")
            
            completion = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "user", "content": "현재 디렉터리의 파일 목록을 보고 싶어. 무엇을 해야 해?"}
                ],
                max_completion_tokens=500
            )
            
            response = completion.choices[0].message.content
            log_success("응답 받음:")
            print(response)
            return True
        
        else:
            log_warning(f"{provider} 테스트는 구현 예정")
            return False
    
    except Exception as e:
        log_error(f"시나리오 생성 실패: {e}")
        return False
    
    print()


# ============================================================================
# 7. 메인 테스트 함수
# ============================================================================

def main():
    """메인 테스트 함수"""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║   Gemini Tutor CLI v2.0 - 테스트 및 Setup 도구        ║")
    print("║   Multi-LLM 통합 (Groq/Perplexity/Gemini)             ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    # 1. 환경 정보
    show_environment_info()
    
    # 2. 의존성 확인
    if not check_dependencies():
        print("\n❌ 의존성 설치 후 다시 실행하세요.")
        sys.exit(1)
    
    # 3. 설정 확인
    config_exists = check_configuration()
    
    if not config_exists:
        print("\n[💡] 첫 실행인 것 같습니다. Setup을 시작합니다.\n")
        if quick_setup_wizard():
            check_configuration()
        else:
            print("❌ Setup 실패. 나중에 다시 시도하세요.")
            sys.exit(1)
    
    # 4. API 테스트 메뉴
    print("\n" + "="*60)
    print("🧪 API 테스트")
    print("="*60 + "\n")
    print("1) Groq API 테스트")
    print("2) Google Gemini API 테스트")
    print("3) Perplexity API 테스트")
    print("4) 모두 테스트")
    print("5) 테스트 건너뛰기\n")
    
    test_choice = input("선택 (기본: 5) > ").strip() or "5"
    
    if test_choice in ["1", "4"]:
        test_groq_api()
    
    if test_choice in ["2", "4"]:
        test_gemini_api()
    
    if test_choice in ["3", "4"]:
        test_perplexity_api()
    
    # 5. 시나리오 생성 테스트
    print("\n" + "="*60)
    print("🧪 추가 기능 테스트")
    print("="*60 + "\n")
    print("1) 시나리오 생성 테스트")
    print("2) 건너뛰기\n")
    
    feature_choice = input("선택 (기본: 2) > ").strip() or "2"
    
    if feature_choice == "1":
        test_scenario_generation()
    
    # 최종 요약
    print("\n" + "="*60)
    print("✅ 테스트 완료")
    print("="*60 + "\n")
    print("다음 단계:")
    print("1. 다음 명령어로 메인 프로그램 실행:")
    print("   python gemini_tutor_app_v2.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 테스트 중단됨.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 예상치 못한 오류: {e}")
        sys.exit(1)
