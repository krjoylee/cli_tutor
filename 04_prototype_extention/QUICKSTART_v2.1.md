# ⚡ Gemini Tutor CLI v2.1 - 5분 빠른 시작

**목표:** 5분 안에 AI 튜터 시작하기!

---

## 🚀 5 Steps to Go!

### ✅ Step 1: Python 확인 (30초)

```bash
python --version
```

**예상 출력:**
```
Python 3.8.0 이상
```

없다면 [python.org](https://python.org)에서 설치하세요.

---

### ✅ Step 2: 라이브러리 설치 (2분)

```bash
pip install groq google-generativeai rich textual httpx
```

**진행 중:**
```
Collecting groq...
Successfully installed groq-0.x.x
...
Successfully installed [모든 라이브러리]
```

---

### ✅ Step 3: Setup 마법사 (1분 30초)

```bash
python test_setup_v2.1.py
```

**화면에 표시되는 것:**

#### 1️⃣ **시스템 정보**
```
📊 시스템 환경 정보
┌────────────────────────────────────────┐
│ OS          │ Windows 11               │
│ 아키텍처    │ x86_64                   │
│ 프로세서    │ Intel(R) Core(TM)...     │
│ Python      │ CPython 3.14.0           │
│ 설정 디렉토 │ C:\Users\USER\.g-tutor   │
└────────────────────────────────────────┘
```

#### 2️⃣ **의존성 확인**
```
📦 의존성 확인
[✅] groq                 - Groq API 클라이언트
[✅] google.generativeai  - Google Gemini API
[✅] rich                 - 터미널 렌더링
[✅] textual              - TUI 프레임워크
[✅] httpx                - HTTP 클라이언트
✅ 모든 의존성 설치됨!
```

#### 3️⃣ **저장된 설정 확인**
```
⚙️ 저장된 설정 확인
✅ 설정 파일 발견: C:\Users\USER\.g-tutor\config.json

[INFO] llm_provider  = groq
[INFO] llm_model     = openai/gpt-oss-120b
[INFO] groq_api_key  = gsk_pcb6ve...
```

#### 4️⃣ **API 테스트**
```
🧪 API 테스트

테스트할 API를 선택하세요:
1) Groq API 테스트
2) Google Gemini API 테스트
3) Perplexity API 테스트
4) 모두 테스트
5) 테스트 건너뛰기

선택 (기본: 5) > _
```

**선택하세요:** `5` (건너뛰기) 또는 `1` (테스트)

---

### ✅ Step 4: 메인 프로그램 실행 (30초)

```bash
python gemini_tutor_app_v2.1.py
```

**화면에 나타나는 것:**

```
╔════════════════════════════════════════════════════╗
║     Gemini Tutor CLI v2.1 - AI 터미널 튜터         ║
║     Multi-LLM (Groq/Perplexity/Gemini)             ║
╚════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────┐
│ 세션목록  │  메인 터미널      │ 명령어 설명      │
│ [1]      │  (입력 대기중)    │ 패널             │
│ [+new]   │                   │                  │
│          │                   ├──────────────────┤
│          │                   │ 에이전트 가이드  │
│          │                   │ (시나리오)       │
└──────────────────────────────────────────────────┘

[Q] 종료  [C] 지우기
```

---

### ✅ Step 5: 명령어 배우기 시작! 🎉

**메인 터미널에 입력:**

```
현재 폴더의 파일 목록을 보고 싶어
```

**AI 응답 (예시):**

```
✅ STEP 1: 파일 목록 보기
명령: ls
설명: 현재 디렉터리의 모든 파일과 폴더를 표시합니다

✅ STEP 2: 더 자세한 정보 보기
명령: ls -la
설명: 숨김 파일 포함, 권한/크기/수정일 등 상세 정보 표시

✅ STEP 3: 폴더 트리 보기 (선택)
명령: tree
설명: 폴더 구조를 시각적 트리 형태로 표시
```

---

## 💡 자주 묻는 질문 (FAQ)

### Q1: API 키는 어디서 얻나요?

#### Groq (권장) ⭐

```
1. https://console.groq.com 접속
2. 로그인/가입
3. "API Keys" 메뉴 클릭
4. "+ Create New API Key" 클릭
5. 생성된 키 복사 → Setup 마법사에 붙여넣기
```

#### Google Gemini

```
1. https://aistudio.google.com 접속
2. Google 계정으로 로그인
3. "Get API Key" 클릭
4. "Create API key in new project" 선택
5. 생성된 키 복사 → Setup 마법사에 붙여넣기
```

#### Perplexity

```
1. https://www.perplexity.ai 접속
2. 가입/로그인
3. 설정 > API 섹션
4. "+ Create API Key" 클릭
5. 생성된 키 복사 → Setup 마법사에 붙여넣기
```

---

### Q2: "ModuleNotFoundError" 에러가 나요

**해결:**

```bash
pip install --upgrade groq google-generativeai rich textual httpx
```

다시 실행하세요.

---

### Q3: 인터넷이 없어도 되나요?

**아니요.** LLM API 호출이 필요하므로 **인터넷 필수**입니다.

---

### Q4: 다른 LLM으로 변경하려면?

```bash
# Windows
Remove-Item -Recurse $env:USERPROFILE\.g-tutor

# macOS/Linux
rm -rf ~/.g-tutor

# Setup 다시 실행
python test_setup_v2.1.py
```

---

### Q5: 설정을 초기화하려면?

```bash
# Windows PowerShell
Remove-Item $env:USERPROFILE\.g-tutor\config.json

# macOS/Linux
rm ~/.g-tutor/config.json

# Setup 도구 다시 실행
python test_setup_v2.1.py
```

---

## 🆘 문제 해결

### Error: "Layout got unexpected argument 'direction'"

**수정됨!** v2.1에서 이 에러는 완전히 수정되었습니다.

만약 여전히 발생하면:

```bash
pip install --upgrade textual
```

---

### Error: "python 명령을 찾을 수 없음"

**Windows:**
1. Python 재설치
2. 설치 시 **"Add Python to PATH"** 반드시 체크!

**macOS/Linux:**
```bash
python3 --version
python3 test_setup_v2.1.py
```

`python3` 명시적으로 사용

---

### Error: "API 키가 유효하지 않습니다"

```bash
# 설정 파일 삭제
# Windows
Remove-Item -Recurse -Force $env:USERPROFILE\.g-tutor

# macOS/Linux
rm -rf ~/.g-tutor

# Setup 마법사 다시 실행
python test_setup_v2.1.py

# API 키 다시 입력 (복사/붙여넣기 주의!)
```

---

### Error: "권한 거부 (Permission denied)"

**macOS/Linux:**
```bash
chmod +x test_setup_v2.1.py
chmod +x gemini_tutor_app_v2.1.py
```

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## ✅ 체크리스트

시작 전 확인:

- [ ] Python 3.8+ 설치됨
- [ ] 인터넷 연결됨
- [ ] 라이브러리 설치됨 (`pip install groq ...`)
- [ ] LLM API 키 준비됨

---

## 📚 다음 단계

### 1. 설치 완료 후
- 📖 README_v2.1_KR.md 읽기 (자세한 설명)
- 🧪 다양한 명령어 시도해보기
- 🔄 다른 LLM과 비교해보기

### 2. 심화 학습
- LLM 체인 구성
- 에러 자동 감지
- 세션 기록 분석

---

## 🎓 학습 예제

### 예제 1: 파일 찾기

```
입력: "용량이 큰 파일을 찾고 싶어"

출력:
✅ STEP 1: 현재 디렉터리에서 큰 파일 찾기
명령: ls -lSh
설명: 파일을 크기 순으로 정렬하여 표시

✅ STEP 2: 모든 하위 폴더에서 찾기
명령: find . -type f -size +100M
설명: 100MB 이상의 모든 파일을 찾아 표시

✅ STEP 3: 상세한 정보 보기
명령: du -sh *
설명: 각 항목의 실제 디스크 사용량 표시
```

### 예제 2: 텍스트 파일 처리

```
입력: "파일의 특정 단어 개수를 세고 싶어"

출력:
✅ STEP 1: 단어 개수 세기
명령: wc -w filename.txt
설명: 파일의 전체 단어 개수 표시

✅ STEP 2: 특정 단어 찾기
명령: grep -c "word" filename.txt
설명: 특정 단어가 몇 번 나왔는지 표시

✅ STEP 3: 각 줄의 단어 개수
명령: awk '{print NF}' filename.txt
설명: 각 줄별 단어 개수 표시
```

---

## 🎯 LLM 선택 가이드

| 상황 | 추천 | 이유 |
|------|------|------|
| **빠르고 무료** | Groq | 1-3초, 무료 |
| **한국어 우수** | Gemini | 공식 번역 |
| **최신 정보** | Perplexity | 웹 검색 |
| **일일 많은 요청** | Groq | 1,000 무료 |
| **안정적** | Gemini | Google 서비스 |

---

## 🎉 준비 완료!

```bash
# 이제 시작하세요!
python test_setup_v2.1.py
python gemini_tutor_app_v2.1.py
```

**Happy Learning! 🚀**

---

## 📞 추가 도움

- 📖 **완전 설명서**: README_v2.1_KR.md
- 📋 **파일 목록**: MANIFEST_v2.1.txt
- 🔗 **Groq**: https://console.groq.com
- 🔗 **Gemini**: https://aistudio.google.com
- 🔗 **Perplexity**: https://www.perplexity.ai

---

**버전:** 2.1  
**업데이트:** 2026년 3월 10일  
**상태:** ✅ 안정화

Made with ❤️ for Terminal Learners
