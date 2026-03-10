# 📚 Gemini Tutor CLI v2.1 - 완전 설명서

**버전:** 2.1  
**업데이트:** 2026년 3월 10일  
**상태:** ✅ 프로덕션 준비 (v2.1 안정화)

---

## 📖 목차

1. [개요](#개요)
2. [주요 기능](#주요-기능)
3. [설치](#설치)
4. [빠른 시작](#빠른-시작)
5. [상세 가이드](#상세-가이드)
6. [LLM 설정](#llm-설정)
7. [문제 해결](#문제-해결)
8. [버전 변경사항](#버전-변경사항)

---

## 개요

**Gemini Tutor CLI v2.1**은 다중 LLM 기반의 **터미널 명령어 학습 도구**입니다.

- 🤖 **다중 LLM 지원**: Groq, Perplexity, Google Gemini
- 🖥️ **플랫폼 호환**: Windows (PowerShell), macOS, Linux, WSL
- ⚡ **빠른 설정**: 5분 안에 시작 가능
- 📊 **대화형 TUI**: Textual 기반 터미널 UI
- 🎓 **단계별 가이드**: 각 명령어별 설명 및 시나리오

---

## 주요 기능

### 1. **자동 환경 감지**
- OS 타입 자동 인식 (Windows / macOS / Linux / WSL)
- CPU 아키텍처 감지 (x86_64 / ARM64)
- Python 버전 및 경로 확인

### 2. **Multi-LLM 통합**
- **Groq**: 빠르고 무료 (권장)
- **Perplexity**: 웹 검색 기반, 최신 정보
- **Google Gemini**: 한국어 우수, 공식 API

### 3. **Setup 마법사**
- 처음 실행 시 자동으로 LLM 선택 및 API 키 입력
- 설정 저장: `~/.g-tutor/config.json`

### 4. **대화형 TUI (Terminal User Interface)**
- **세션 관리**: 여러 학습 세션 동시 관리
- **터미널 패널**: 명령어 입력/실행
- **설명 패널**: 방금 실행한 명령어 상세 설명
- **에이전트 패널**: 목표에 맞는 단계별 시나리오

### 5. **상세한 명령어 설명**
- 각 명령어가 하는 일
- 실행 결과 해석
- 다음 단계 제안

---

## 설치

### 요구사항

- **Python**: 3.8 이상
- **OS**: Windows 11 / macOS / Linux / WSL
- **인터넷**: LLM API 호출 필요

### Step 1: Python 확인

```bash
python --version
```

최소 3.8 이상이어야 합니다. 없다면 [python.org](https://python.org)에서 설치하세요.

### Step 2: 라이브러리 설치

```bash
pip install groq google-generativeai rich textual httpx
```

**설치 내용:**
- `groq`: Groq API 클라이언트
- `google-generativeai`: Google Gemini API
- `rich`: 터미널 렌더링
- `textual`: TUI 프레임워크
- `httpx`: HTTP 클라이언트 (Perplexity 호환)

### Step 3: 프로그램 다운로드

모든 파일을 한 폴더에 저장하세요:

```
my-tutor/
├── gemini_tutor_app_v2.1.py    # 메인 프로그램
├── test_setup_v2.1.py           # Setup 도구
├── README_v2.1_KR.md            # 이 파일
├── QUICKSTART_v2.1.md           # 빠른 시작 가이드
└── MANIFEST_v2.1.txt            # 파일 목록
```

---

## 빠른 시작

### 5분 안에 시작하기

```bash
# 1. Setup 도구 실행 (처음 1번만)
python test_setup_v2.1.py

# 2. LLM 선택 & API 키 입력

# 3. 메인 프로그램 실행
python gemini_tutor_app_v2.1.py
```

**상세 절차:** [QUICKSTART_v2.1.md](QUICKSTART_v2.1.md) 참고

---

## 상세 가이드

### 프로그램 구조

```
┌─────────────────────────────────────────────┐
│  사용자 (Windows/macOS/Linux/WSL)           │
└────────────┬────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────────┐  ┌──────────────────┐
│ test_setup  │  │ gemini_tutor_app │
│  v2.1.py    │  │    v2.1.py       │
└─────────────┘  └──────────────────┘
    (1회)            (계속 사용)
    │                │
    ├─ EnvInfo       ├─ EnvInfo
    ├─ ConfigMgr     ├─ ConfigManager
    ├─ LLM 선택      ├─ LLMClient
    └─ API 테스트    └─ Textual TUI
                         (세션/터미널/설명)
```

### 핵심 클래스

#### 1. **EnvInfo** - 환경 정보
```python
env = EnvInfo()
print(env.os_type)  # "windows", "macos", "linux", "wsl"
print(env.arch)     # "x86_64", "arm64"
print(env.is_wsl)   # True/False
```

#### 2. **ConfigManager** - 설정 관리
```python
config = ConfigManager()
config.set("llm_provider", "groq")
config.save_config()
```

저장 위치: `~/.g-tutor/config.json`

#### 3. **LLMClient** - 다중 LLM 클라이언트
```python
llm = LLMClient("groq", api_key, "openai/gpt-oss-120b")
scenario = llm.generate_scenario("파일 찾기", env_info)
```

#### 4. **SetupWizard** - 초기 설정
```python
wizard = SetupWizard(console, env_info)
wizard.run()  # 대화형 설정 진행
```

---

## LLM 설정

### Groq (권장) ⭐

**장점:**
- 무료 (일 1,000개 요청 무료)
- 매우 빠름 (1-3초)
- RPM 30, TPM 1,000 이상

**설정:**
1. https://console.groq.com 접속
2. 로그인/가입
3. "API Keys" 메뉴
4. "+ Create New API Key"
5. 키 복사

**모델:**
- `openai/gpt-oss-120b` (권장)
- `llama-3.1-405b` (더 큼)

---

### Perplexity 🔍

**장점:**
- 웹 검색 기반 (최신 정보)
- 스트리밍 지원
- 일반적인 질문에 우수

**설정:**
1. https://www.perplexity.ai 접속
2. 가입/로그인
3. 설정 > API
4. "+ Create API Key"

**모델:**
- `pplx-7b-online` (기본)

---

### Google Gemini 🔷

**장점:**
- 한국어 번역 우수
- 공식 Google API
- 안정적

**설정:**
1. https://aistudio.google.com 접속
2. Google 로그인
3. "Get API key"
4. "Create API key in new project"

**모델:**
- `gemini-2.0-flash` (권장)
- `gemini-pro` (이전 버전)

---

## 문제 해결

### Problem 1: "ModuleNotFoundError: No module named 'groq'"

**해결:**
```bash
pip install groq google-generativeai rich textual httpx
```

---

### Problem 2: "API 키가 유효하지 않습니다"

**해결:**
```bash
# 1. 설정 파일 삭제
rm -r ~/.g-tutor/config.json  # macOS/Linux
Remove-Item $env:USERPROFILE\.g-tutor\config.json  # Windows

# 2. Setup 다시 실행
python test_setup_v2.1.py

# 3. API 키 다시 입력 (복사/붙여넣기 주의)
```

---

### Problem 3: "Textual Layout 에러"

**해결:**
```bash
pip install --upgrade textual
```

최신 버전 설치 후 재실행하세요.

---

### Problem 4: "python 명령을 찾을 수 없음"

**Windows:**
1. Python 재설치
2. 설치 시 "Add Python to PATH" 체크

**macOS/Linux:**
```bash
which python3
# 또는
python3 --version
```

`python3`를 명시적으로 사용하세요.

---

### Problem 5: "인터넷 연결 오류"

**확인:**
```bash
ping google.com
```

**Windows 방화벽 확인:**
1. Windows Defender Firewall 설정
2. "앱 허용" 섹션에서 Python 확인

---

## 버전 변경사항

### v2.1 (2026년 3월)

✅ **수정 사항:**
- Textual `Layout` 호환성 수정 (`direction` 파라미터 제거)
- TUI 구조 최적화 (`Horizontal/Vertical` 컨테이너 사용)
- LLM 클라이언트 통합 개선

✨ **개선 사항:**
- 다중 LLM 클라이언트 완전 통합
- Setup 마법사 UI 개선
- 에러 메시지 상세화
- 한글 지원 강화

📦 **패키지:**
- `gemini_tutor_app_v2.1.py` (메인, 수정됨)
- `test_setup_v2.1.py` (Setup 도구)
- `README_v2.1_KR.md` (이 파일)
- `QUICKSTART_v2.1.md` (빠른 시작)
- `MANIFEST_v2.1.txt` (파일 목록)

### v2.0 (이전 버전)

- 초기 다중 LLM 통합
- 기본 TUI 구조
- Groq/Gemini 지원

---

## ✅ 체크리스트

설치 전 확인:
- [ ] Python 3.8+ 설치
- [ ] 인터넷 연결
- [ ] pip 명령어 작동
- [ ] 관리자 권한 (Windows)

---

## 📞 추가 도움

- **빠른 시작:** [QUICKSTART_v2.1.md](QUICKSTART_v2.1.md)
- **파일 목록:** [MANIFEST_v2.1.txt](MANIFEST_v2.1.txt)
- **Groq 공식:** https://groq.com
- **Gemini 공식:** https://ai.google.dev
- **Perplexity 공식:** https://www.perplexity.ai

---

**Happy Learning! 🚀**

Made with ❤️ for Terminal Learners
