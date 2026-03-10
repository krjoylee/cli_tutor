# ⚡ Gemini Tutor CLI v2.0 - 5분 빠른 시작

**목표:** 5분 안에 AI 튜터 시작하기!

---

## 🚀 5 Steps to Go!

### ✅ Step 1: Python 확인 (30초)

```powershell
python --version
```

**예상 출력:**
```
Python 3.8.0 이상
```

**문제 있으면:** Python 재설치 (python.org)

---

### ✅ Step 2: 라이브러리 설치 (2분)

```powershell
pip install groq google-generativeai rich textual httpx
```

**진행 중:**
```
Collecting groq...
Successfully installed groq
...
```

**완료 신호:**
```
Successfully installed [라이브러리들]
```

---

### ✅ Step 3: Setup 마법사 (1분 30초)

```powershell
python test_setup_v2.py
```

**화면에 표시되는 것:**

1️⃣ **시스템 정보**
```
📊 시스템 환경 정보
OS: Windows 11 Release 22H2
아키텍처: x86_64
Python: CPython 3.10.5
```

2️⃣ **의존성 확인**
```
📦 의존성 확인
groq ✅
google.generativeai ✅
rich ✅
textual ✅
httpx ✅
```

3️⃣ **LLM 선택**
```
사용할 LLM을 선택하세요:

1) [✅ 추천] Groq - 빠르고 무료, RPM 30
2) Perplexity - 검색 기반, 최신 정보
3) Google Gemini - 한국어 우수, 일 250 요청

선택 (기본: 1) > _
```

**선택하세요:** `1` (또는 원하는 LLM)

4️⃣ **API 키 입력**

**Groq 선택 시:**
```
Groq API 키를 입력하세요 > _
```

👉 https://console.groq.com 에서 API 키 복사 후 붙여넣기

**또는 Gemini 선택 시:**
```
Gemini API 키를 입력하세요 > _
```

👉 https://aistudio.google.com 에서 API 키 복사 후 붙여넣기

5️⃣ **API 테스트 (선택사항)**
```
🧪 API 테스트

1) Groq API 테스트
2) Google Gemini API 테스트
3) Perplexity API 테스트
4) 모두 테스트
5) 테스트 건너뛰기

선택 (기본: 5) > 1
```

**성공하면:**
```
✅ Groq API 테스트
✅ Groq 클라이언트 초기화 중...
✅ 테스트 요청 전송 중...
✅ 응답 받음: 안녕하세요! 무엇을 도와드릴까요?
```

---

### ✅ Step 4: 메인 프로그램 실행 (30초)

```powershell
python gemini_tutor_app_v2.py
```

**화면에 나타나는 것:**

```
╔════════════════════════════════════════════════════╗
║     Gemini Tutor CLI v2.0 - AI 터미널 튜터         ║
╚════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────┐
│ 세션목록  │  메인 터미널         │ 방금 실행 명령   │
│ [1]      │  (명령어 입력 대기)  │ 설명 패널        │
│ [+new]   │                     │                 │
├──────────┴─────────────────────┴─────────────────┤
│ 에이전트 가이드 (시나리오 제시)                   │
└─────────────────────────────────────────────────────┘
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

**Groq (추천)**
```
1. https://console.groq.com 접속
2. 로그인/가입
3. "API Keys" 메뉴
4. "+ Create New API Key" 클릭
5. 키 복사
```

**Google Gemini**
```
1. https://aistudio.google.com 접속
2. Google 로그인
3. "Get API Key" 클릭
4. "Create API key in new project" 선택
5. 키 복사
```

---

### Q2: "ModuleNotFoundError" 에러가 나요

**해결:**
```powershell
pip install groq google-generativeai rich textual httpx
```

다시 실행하세요.

---

### Q3: 인터넷이 없어도 되나요?

**아니요.** LLM API 호출이 필요하므로 인터넷 필수입니다.

---

### Q4: 다른 LLM으로 변경하려면?

```powershell
# 설정 삭제
Remove-Item $env:USERPROFILE\.g-tutor\config.json

# Setup 다시 실행
python test_setup_v2.py

# 다른 LLM 선택
```

---

### Q5: 명령어를 실행할 수 있나요?

**현재:** 명령어 제시만 (버전 2.0)
**향후:** 실제 실행 가능 (버전 3.0)

---

## 🆘 문제 해결

### Problem 1: "python 명령을 찾을 수 없음"

```powershell
# Python 재설치
# https://python.org 에서 다운로드
# 설치 시 "Add Python to PATH" 체크
```

---

### Problem 2: "API 키가 유효하지 않습니다"

```powershell
# 1. 설정 파일 삭제
Remove-Item -Recurse -Force $env:USERPROFILE\.g-tutor

# 2. Setup 다시 실행
python test_setup_v2.py

# 3. API 키 다시 입력 (복사/붙여넣기 주의)
```

---

### Problem 3: "권한이 없습니다"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

그 후 다시 실행

---

### Problem 4: "인터넷 연결 오류"

```powershell
# 인터넷 연결 테스트
ping google.com

# 방화벽 확인
# Windows Defender Firewall 설정 확인
```

---

## ✅ 체크리스트

설치 전에 다음을 확인하세요:

- [ ] Python 3.8 이상 설치됨
- [ ] 인터넷 연결됨
- [ ] 관리자 권한 있음 (Windows)
- [ ] 터미널/PowerShell 열 수 있음

---

## 📚 다음 단계

### 설치 후:
1. 📖 README_v2_KR.md 읽기 (자세한 설명)
2. 🧪 다양한 명령어 시도해보기
3. 🔄 다른 LLM과 비교해보기

### 심화 학습:
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
명령: find . -type f -size +100M -exec ls -lh {} \;
설명: 100MB 이상 파일의 상세 정보 표시
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
명령: wc -w < filename.txt
설명: 더 간단한 형식으로 단어 개수 표시
```

---

## 🎯 목표별 LLM 추천

| 목표 | 추천 | 이유 |
|------|------|------|
| **빠른 응답** | Groq | 1-3초 |
| **한국어** | Gemini | 우수한 번역 |
| **최신 정보** | Perplexity | 웹 검색 |
| **비용 최소** | Groq | 일 1,000 무료 |
| **안정성** | Gemini | Google 서비스 |

---

## 🎉 준비 완료!

```powershell
# 이제 시작하세요!
pip install groq google-generativeai rich textual httpx
python test_setup_v2.py
python gemini_tutor_app_v2.py
```

**Happy Learning! 🚀**

---

## 📞 추가 도움

- 📖 완전 설명서: README_v2_KR.md
- 🐛 문제 해결: README_v2_KR.md의 "문제 해결" 섹션
- 🔑 API 정보: 각 LLM 공식 웹사이트

---

**버전:** 2.0  
**작성일:** 2026년 3월 10일  
**한글 지원:** 완벽 ✅
