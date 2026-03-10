# 🚀 Gemini Tutor CLI v2.0 - 완전 설명서

## Multi-LLM 통합 버전 (Groq/Perplexity/Gemini)

**버전:** 2.0 (Multi-LLM 프로토타입)  
**작성일:** 2026년 3월 10일  
**호환성:** Windows 11 PowerShell 5.1+, macOS, Linux, WSL  
**라이선스:** MIT (자유 이용)

---

## 📋 개요

Gemini Tutor CLI는 **터미널/CLI 명령어를 배우는 데 도움이 되는 AI 튜터**입니다.

### v2.0의 새로운 기능

✅ **Groq 통합** (기본, 추천) - 빠르고 무료  
✅ **Perplexity 통합** - 최신 웹 정보 검색  
✅ **Google Gemini 통합** - 한국어 우수  
✅ **초기 설정 시 LLM 선택** - 사용자가 원하는 API 선택  
✅ **Setup 마법사** - 자동 설정 및 테스트  
✅ **다중 환경 지원** - Windows/macOS/Linux/WSL

---

## 🎯 사용 시나리오

### 시나리오 1: 초보자 (5분 설치)

```powershell
# 1단계: 필수 라이브러리 설치
pip install groq google-generativeai rich textual httpx

# 2단계: 테스트 및 Setup 실행
python test_setup_v2.py

# 3단계: 메인 프로그램 실행
python gemini_tutor_app_v2.py
```

**처음 실행 시:** Setup 마법사가 자동으로 실행되어 LLM 선택 및 API 키 입력을 안내합니다.

---

### 시나리오 2: 빠른 시작 (Groq 추천)

Groq를 선택하시면:

```powershell
# 1. 라이브러리 설치
pip install groq rich textual httpx

# 2. Setup 도구 실행 → LLM 선택 (1번 선택) → API 키 입력
python test_setup_v2.py

# 3. 메인 프로그램 실행
python gemini_tutor_app_v2.py

# 입력 예시: "현재 폴더의 파일 목록을 보고 싶어"
# AI가 단계별 명령어를 제시합니다!
```

**소요 시간:** 약 5분

---

### 시나리오 3: 개발자 (커스터마이징)

코드를 수정하고 싶으면:

1. `gemini_tutor_app_v2.py` 열기
2. `LLMClient` 클래스 수정 (API 호출 로직)
3. `GeminiTutorApp` 클래스 수정 (UI)
4. 원하는 기능 추가

**참고:** 각 클래스에 상세한 주석이 있습니다.

---

## 📦 필수 요구사항

| 항목 | 요구사항 | 비고 |
|------|---------|------|
| **OS** | Windows 11+ / macOS / Linux | WSL 지원 |
| **Python** | 3.8 이상 | `python --version` 확인 |
| **pip** | 최신 버전 | `pip --version` 확인 |
| **인터넷** | 필수 | LLM API 호출용 |

---

## 🔧 설치 단계별 가이드

### 1단계: Python 설치 확인

```powershell
# Windows PowerShell
python --version
pip --version

# 출력 예:
# Python 3.10.5
# pip 23.0.1
```

**문제 해결:**
- `python 명령을 찾을 수 없음` → Python을 재설치하고 "환경 변수에 추가" 선택

### 2단계: 라이브러리 설치

```powershell
# 모든 라이브러리 한 번에 설치
pip install groq google-generativeai rich textual httpx

# 또는 한 개씩 설치
pip install groq              # Groq API
pip install google-generativeai  # Google Gemini
pip install rich              # 터미널 렌더링
pip install textual           # TUI 프레임워크
pip install httpx             # HTTP 클라이언트 (Perplexity용)
```

**설치 확인:**
```powershell
python -c "import groq; import rich; import textual; print('✅ 모든 라이브러리 설치됨')"
```

### 3단계: API 키 발급

#### 🟢 **Groq (기본, 추천)**

1. https://console.groq.com 에 접속
2. 로그인/가입
3. 좌측 "API Keys" 클릭
4. "Create New API Key" 버튼
5. 생성된 키 복사
6. 제한: **일 1,000 요청** (무료)

**모델:** `openai/gpt-oss-120b` (빠르고 우수한 성능)

#### 🔵 **Google Gemini**

1. https://aistudio.google.com 에 접속
2. Google 계정으로 로그인
3. "Get API key" 버튼
4. "Create API key in new project" 선택
5. 생성된 키 복사
6. 제한: **일 250 요청** (무료)

**모델:** `gemini-2.0-flash` (빠르고 한국어 우수)

#### 🟣 **Perplexity**

1. https://www.perplexity.ai 에 접속
2. 계정 생성/로그인
3. 설정(⚙️) > API 섹션
4. "Create New API Key" 버튼
5. 생성된 키 복사
6. 제한: **월별 요청 한계** (요금제에 따라)

**특징:** 웹 검색 통합, 최신 정보 제공

### 4단계: Setup 실행

```powershell
# Setup 도구 실행
python test_setup_v2.py

# 화면에 다음이 표시됩니다:
# 1) 시스템 환경 정보
# 2) 의존성 확인
# 3) 설정 확인
# 4) LLM 선택 메뉴
```

**LLM 선택:**
```
사용할 LLM을 선택하세요:

1) [✅ 추천] Groq - 빠르고 무료, RPM 30
2) Perplexity - 검색 기반, 최신 정보
3) Google Gemini - 한국어 우수, 일 250 요청

선택 (기본: 1) > _
```

선택한 LLM의 API 키를 입력하면 설정 완료!

### 5단계: API 테스트

```powershell
# Setup 도구에서 "API 테스트" 선택
# 또는 직접 테스트:

# Groq 테스트
python test_setup_v2.py  # → 1번 선택

# Gemini 테스트
python test_setup_v2.py  # → 2번 선택

# Perplexity 테스트
python test_setup_v2.py  # → 3번 선택
```

### 6단계: 메인 프로그램 실행

```powershell
python gemini_tutor_app_v2.py
```

---

## 📖 TUI 사용법

### 레이아웃

```
┌─────────────────────────────────────────────────────┐
│              🎯 Gemini Tutor CLI v2.0               │
├──────────┬─────────────────────┬───────────────────┤
│ 세션목록 │  메인 터미널        │ 방금 실행 명령    │
│          │  (입력 창)          │ 설명 패널         │
│ [1] ..   │                     │                   │
│ [2] ..   │                     ├───────────────────┤
│ [+ new]  │                     │ 에이전트 가이드   │
│          │                     │ (시나리오 제시)   │
└──────────┴─────────────────────┴───────────────────┘
```

### 사용 예시

```
1. "현재 폴더의 파일 목록을 보고 싶어" 입력

2. AI가 다음을 제시:
   ✅ Step 1: 폴더 내 모든 파일 보기
      명령: ls
      설명: 현재 디렉터리의 파일과 폴더 목록 표시

   ✅ Step 2: 더 자세한 정보 보기
      명령: ls -la
      설명: 파일의 크기, 권한, 수정 날짜 등 상세 정보 표시

3. 명령어 설명 패널에 상세 설명이 나타남

4. 다음 명령어를 입력하거나 이전 명령어를 다시 선택 가능
```

### 단축키

| 단축키 | 기능 |
|--------|------|
| `Q` | 프로그램 종료 |
| `C` | 화면 지우기 |
| `↑/↓` | 이전/다음 명령어 |
| `Tab` | 패널 전환 |

---

## ⚙️ 설정 파일 구조

### 저장 위치

모든 설정과 세션은 **`~/.g-tutor/`** 디렉터리에 저장됩니다.

```
~/.g-tutor/
├── config.json          # 설정 파일 (LLM, API 키)
├── sessions/            # 세션 기록
│   ├── default/
│   ├── project-a/
│   └── ...
└── logs/                # 로그 (향후)
```

### config.json 예시

#### Groq 설정
```json
{
  "llm_provider": "groq",
  "llm_model": "openai/gpt-oss-120b",
  "groq_api_key": "gsk_123456789..."
}
```

#### Gemini 설정
```json
{
  "llm_provider": "gemini",
  "llm_model": "gemini-2.0-flash",
  "gemini_api_key": "AIzaSyD_123456789..."
}
```

#### Perplexity 설정
```json
{
  "llm_provider": "perplexity",
  "perplexity_api_key": "ppl_123456789..."
}
```

---

## 🐛 문제 해결

### 1. "ModuleNotFoundError: No module named 'groq'"

**원인:** 라이브러리가 설치되지 않음

**해결:**
```powershell
pip install groq google-generativeai rich textual httpx

# 또는 requirements.txt 생성:
pip install -r requirements.txt

# 설치 확인:
python test_setup_v2.py
```

### 2. "API 키가 유효하지 않습니다"

**원인:** API 키 오입력 또는 만료됨

**해결:**
1. API 키 다시 확인 (복사/붙여넣기)
2. 설정 파일 삭제: `~/.g-tutor/config.json`
3. `python test_setup_v2.py` 실행하여 다시 설정

### 3. "인터넷 연결 실패"

**원인:** 방화벽 또는 네트워크 문제

**확인:**
```powershell
# 인터넷 연결 테스트
ping google.com

# 특정 API 서버 테스트
# Groq: console.groq.com
# Gemini: aistudio.google.com
# Perplexity: api.perplexity.ai
```

### 4. "PowerShell: 이 파일을 실행할 수 없습니다"

**원인:** 실행 정책 제한

**해결:**
```powershell
# 현재 정책 확인
Get-ExecutionPolicy

# 정책 변경
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 다시 실행
python test_setup_v2.py
```

### 5. "WSL 환경에서 오류 발생"

**WSL 환경 확인:**
```bash
# WSL 버전 확인
wsl --version

# Python 재설치
sudo apt update
sudo apt install python3 python3-pip

# 라이브러리 설치
pip3 install groq google-generativeai rich textual httpx
```

---

## 📊 LLM 비교

| 항목 | Groq | Perplexity | Gemini |
|------|------|-----------|--------|
| **속도** | ⭐⭐⭐⭐⭐ 매우 빠름 | ⭐⭐⭐⭐ 빠름 | ⭐⭐⭐⭐ 빠름 |
| **한국어** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ 우수 |
| **웹 검색** | ❌ 미지원 | ✅ 지원 | ❌ 미지원 |
| **일 제한** | 1,000 요청 | 요금제 | 250 요청 |
| **추천** | ⭐⭐⭐⭐⭐ 첫 선택 | ⭐⭐⭐ 최신 정보 | ⭐⭐⭐⭐ 한국어 |

**추천:** 처음 사용자 → **Groq**, 웹 검색 필요 → **Perplexity**, 한국어 우수 → **Gemini**

---

## 🎓 학습 경로

### 레벨 1: 기본 사용 (30분)

```
1. Setup 실행 (10분)
   - python test_setup_v2.py
   - LLM 선택 및 API 키 입력

2. 메인 프로그램 실행 (5분)
   - python gemini_tutor_app_v2.py

3. 간단한 명령어 시도 (15분)
   - "파일 목록 보기"
   - "텍스트 파일 내용 보기"
   - "폴더 생성하기"
```

### 레벨 2: 심화 활용 (1시간+)

```
1. 다양한 명령어 시도
   - 파일 검색
   - 텍스트 처리
   - 시스템 정보 조회

2. 세션 관리
   - 여러 세션 생성
   - 이전 기록 확인

3. 각 LLM 비교
   - Groq vs Gemini vs Perplexity
   - 응답 시간 비교
   - 품질 비교
```

### 레벨 3: 개발자 커스터마이징 (2시간+)

```
1. 코드 구조 분석
   - EnvInfo 클래스
   - ConfigManager 클래스
   - LLMClient 클래스
   - GeminiTutorApp 클래스

2. 기능 추가
   - 실제 셸 명령 실행
   - 에러 자동 감지
   - 명령 결과 자동 설명

3. UI 커스터마이징
   - 새로운 패널 추가
   - 색상 변경
   - 레이아웃 수정
```

---

## 🔄 프로그램 업데이트 LLM 변경

### LLM 변경 방법

```powershell
# 1. 설정 파일 삭제
# Windows:
del $env:USERPROFILE\.g-tutor\config.json

# macOS/Linux:
rm ~/.g-tutor/config.json

# 2. Setup 다시 실행
python test_setup_v2.py

# 3. 다른 LLM 선택
```

---

## 💡 팁과 트릭

### 팁 1: 한국 서버 최적화

Groq는 서울 리전이 없으므로, Perplexity나 Gemini가 더 빠를 수 있습니다.

```powershell
# 각 LLM의 응답 시간 테스트:
python test_setup_v2.py  # 모두 테스트

# 가장 빠른 것 선택
```

### 팁 2: 배치 작업 자동화

Setup을 자동화하려면:

```powershell
# install.ps1 작성
pip install groq google-generativeai rich textual httpx
python test_setup_v2.py
```

### 팁 3: 여러 환경 관리

```powershell
# 환경별 config.json 분리
# ~/.g-tutor/config.work.json
# ~/.g-tutor/config.study.json

# 스크립트로 전환:
# switch-config.ps1
```

---

## 📚 추가 자료

### 공식 문서

- **Groq API:** https://console.groq.com/docs
- **Google Gemini:** https://ai.google.dev
- **Perplexity API:** https://docs.perplexity.ai

### Python 관련

- **Rich 라이브러리:** https://rich.readthedocs.io
- **Textual 프레임워크:** https://textual.textualize.io

### 셸 명령어 학습

- **Linux 명령어:** https://man7.org/linux/man-pages/
- **PowerShell:** https://learn.microsoft.com/en-us/powershell/

---

## 🎉 시작하기

### 지금 바로 시작하세요!

```powershell
# 1단계: 라이브러리 설치
pip install groq google-generativeai rich textual httpx

# 2단계: Setup
python test_setup_v2.py

# 3단계: 실행
python gemini_tutor_app_v2.py

# 4단계: 명령어 배우기 시작!
```

---

## ❓ FAQ

**Q: 정말 무료인가?**  
A: 네! 모든 LLM이 무료 티어를 제공합니다. (일일/월별 요청 한계 있음)

**Q: 오프라인에서도 되나?**  
A: 아니요. LLM API 호출이 필요하므로 인터넷 필수입니다.

**Q: 데이터는 어디에 저장되나?**  
A: 모두 로컬(`~/.g-tutor/`)에 저장됩니다. 클라우드 저장 없음.

**Q: 초보자도 사용 가능한가?**  
A: 네! Setup 마법사가 모든 과정을 안내합니다.

**Q: 어떤 명령어를 배울 수 있나?**  
A: 모든 터미널/CLI 명령어 가능. 특히 Linux/macOS 명령어에 강합니다.

**Q: API 키가 유출되면?**  
A: 각 API 제공자의 대시보드에서 즉시 키를 삭제하면 됩니다.

**Q: 다른 LLM도 추가 가능한가?**  
A: 네! 코드에서 `LLMClient` 클래스를 확장하면 새로운 LLM 추가 가능합니다.

---

## 🛠️ 기술 지원

### 자주 확인할 것

- 설정 파일: `~/.g-tutor/config.json`
- 로그 위치: 터미널 출력
- 캐시: `~/.g-tutor/sessions/`

### 재설치 (완전 초기화)

```powershell
# Windows
Remove-Item -Recurse -Force $env:USERPROFILE\.g-tutor

# macOS/Linux
rm -rf ~/.g-tutor

# 라이브러리 재설치
pip install --upgrade groq google-generativeai rich textual httpx

# Setup 다시 실행
python test_setup_v2.py
```

---

## 📝 버전 히스토리

### v2.0 (현재)
- ✅ Multi-LLM 지원 (Groq/Perplexity/Gemini)
- ✅ 초기 Setup 마법사
- ✅ 자동 환경 감지
- ✅ 향상된 테스트 도구

### v1.0 (이전)
- ✅ Gemini API만 지원
- ✅ 기본 TUI 레이아웃
- ✅ 세션 관리

---

## 📞 연락처 및 피드백

이 프로젝트는 **완전 오픈소스**이며, 모든 코드가 인라인 주석과 함께 제공됩니다.

**다음 업데이트 예정:**
- [ ] 실제 셸 명령 실행
- [ ] 명령 결과 자동 설명
- [ ] 에러 자동 감지 및 해결책
- [ ] 웹 UI 버전
- [ ] 모바일 앱

---

## 🎉 축하합니다!

이제 모든 준비가 되었습니다. Happy Learning! 🚀

**다음 단계:**
1. 라이브러리 설치
2. Setup 실행
3. 메인 프로그램 실행
4. 명령어 배우기 시작!

---

**최종 버전:** 2.0  
**라이선스:** MIT (자유 이용)  
**작성자:** Gemini Tutor Team  
**마지막 수정:** 2026년 3월 10일
