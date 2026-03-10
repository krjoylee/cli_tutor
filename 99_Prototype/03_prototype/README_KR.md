# Gemini Tutor CLI - Windows 11 PowerShell 5.1 설치 및 실행 가이드

## 📋 시스템 요구사항

- **Windows 11** (PowerShell 5.1 이상)
- **Python 3.8+** (설치 확인: `python --version`)
- **pip** (Python 패키지 매니저)

---

## 🚀 설치 단계

### 1단계: 필수 라이브러리 설치

PowerShell에서 다음 명령을 실행하세요:

```powershell
pip install google-generativeai rich textual
```

**각 라이브러리의 역할:**
- `google-generativeai`: Gemini API 호출
- `rich`: 터미널 텍스트 포맷팅 (테이블, 패널 등)
- `textual`: TUI (Text User Interface) 프레임워크

### 2단계: Python 파일 저장

아래 파일을 원하는 위치에 저장하세요:

- 파일명: `gemini_tutor_app.py`
- 위치: 예) `C:\Users\USER\Documents\gemini-tutor\` 또는 `C:\Users\USER\`

### 3단계: Gemini API 키 준비 (무료)

1. 브라우저에서 [Google AI Studio](https://aistudio.google.com) 에 접속
2. Google 계정으로 로그인
3. 좌측 메뉴에서 **"Get API key"** 클릭
4. **"Create API key in new project"** 선택
5. 생성된 API 키를 복사 (프로그램 첫 실행 시 입력)

**주의:** 이 API 키는 비밀이므로 절대 공개하지 마세요!

---

## ▶️ 실행 방법

### 첫 실행 (Setup 마법사)

PowerShell에서:

```powershell
cd C:\Users\USER\Documents\gemini-tutor  # 파일 위치로 이동
python gemini_tutor_app.py
```

또는 파일 경로를 직접 지정:

```powershell
python C:\Users\USER\gemini_tutor_app.py
```

### 첫 실행 시 진행 사항

1. **시스템 정보 표시**
   - OS: `windows`
   - 아키텍처: `x86_64` (또는 ARM64)
   - 상세정보: `windows-x86_64`

2. **LLM 선택**
   ```
   1) Gemini (Google, 무료 티어 지원)
   2) Groq (Llama 등, 무료 티어 지원)
   선택 (기본: 1) > 
   ```
   - 기본값은 **1 (Gemini)** 추천

3. **Gemini API 키 입력**
   ```
   Gemini API 키를 입력하세요 > 
   ```
   - 앞서 복사한 Google AI Studio 키 붙여넣기
   - `Ctrl+V` 로 붙여넣기 (PowerShell에서 마우스 우클릭도 가능)

4. **설정 완료**
   - 설정이 `C:\Users\USER\.g-tutor\config.json` 에 저장됨
   - 다음 실행부터는 Setup 마법사 없이 바로 시작

### 이후 실행 (매번)

```powershell
python gemini_tutor_app.py
```

---

## 🎮 TUI 애플리케이션 사용법

### 레이아웃

```
┌─────────────┬──────────────────────────────┬──────────────────┐
│   세션      │                              │  설명 패널       │
│   목록      │   메인 터미널                │  (우측 상)       │
│             │   (명령 입력 및 출력)        │                  │
│             │                              ├──────────────────┤
│             │                              │  에이전트 가이드 │
│             │                              │  (우측 하)       │
└─────────────┴──────────────────────────────┴──────────────────┘
```

### 주요 기능 (예정)

1. **좌측 세션 패널**
   - 진행 중인 여러 작업/세션 표시
   - 세션 전환

2. **가운데 메인 터미널**
   - 사용자가 실행할 명령어 입력
   - 실행 결과 출력

3. **우측 상부 설명 패널**
   - 방금 실행한 명령어 설명
   - 실행 결과 해석
   - 성공/실패 판정

4. **우측 하부 에이전트 패널**
   - "하고 싶은 일" 입력
   - Gemini가 단계별 시나리오 제안
   - 각 단계의 명령어와 설명

### 키보드 단축키

| 단축키 | 기능 |
|--------|------|
| `q`    | 프로그램 종료 |
| `c`    | 화면 지우기 |

---

## 🔧 설정 파일 위치 및 구조

### 설정 파일

- **위치:** `C:\Users\USER\.g-tutor\config.json`
- **내용 예시:**

```json
{
  "llm_provider": "gemini",
  "llm_model": "gemini-2.0-flash",
  "gemini_api_key": "YOUR_API_KEY_HERE"
}
```

### 세션 저장 디렉터리

- **위치:** `C:\Users\USER\.g-tutor\sessions\`
- 각 세션의 기록이 마크다운 파일로 저장됨

---

## 🐛 문제 해결

### 1. "ModuleNotFoundError: No module named 'google'"

**해결:**
```powershell
pip install google-generativeai
```

### 2. "ModuleNotFoundError: No module named 'rich'"

**해결:**
```powershell
pip install rich
```

### 3. "ModuleNotFoundError: No module named 'textual'"

**해결:**
```powershell
pip install textual
```

### 4. API 키 관련 오류

**확인 사항:**
1. Google AI Studio에서 정말 API 키를 생성했는가?
2. API 키를 정확하게 복사/붙여넣었는가?
3. API 키에 공백이나 줄바꿈이 없는가?

### 5. 무한 로딩 / 응답 없음

**원인:**
- Gemini API가 느릴 수 있음 (보통 3~10초 소요)
- 인터넷 연결 확인

**해결:**
- `Ctrl+C` 로 중단 후 재실행

### 6. 한글 입력이 깨짐

**해결:**
- PowerShell의 인코딩 설정:
  ```powershell
  chcp 65001  # UTF-8 활성화
  ```

---

## 📚 Gemini API 무료 티어 한계

- **일일 요청 한계:** 약 250 요청/일
- **분당 요청 한계:** 약 10 요청/분
- **무료 모델:** `gemini-2.0-flash` (또는 최신 Flash)

장시간 사용하거나 많은 요청이 필요하면 [Google Cloud](https://cloud.google.com) 에서 유료 플랜 검토.

---

## 💡 팁 및 활용법

### 팁 1: 여러 PowerShell 창에서 동시 실행

각각 다른 세션으로 여러 작업을 병렬 진행 가능:

```powershell
# PowerShell 창 1
python gemini_tutor_app.py  # 세션: node-env

# PowerShell 창 2 (새로 열기)
python gemini_tutor_app.py  # 세션: docker-test
```

### 팁 2: 설정 수동 변경

config.json을 텍스트 에디터(메모장, VS Code 등)로 직접 편집 가능.

### 팁 3: 세션 기록 확인

`C:\Users\USER\.g-tutor\sessions\` 에서 이전 세션 기록 조회.

---

## 📞 추가 지원

이 도구는 **Gemini Tutor CLI 통합 설계서**를 기반으로 만들어졌습니다.

- 더 많은 기능 추가 요청
- 버그 리포트
- 개선 사항 제안

등은 개발자에게 문의하세요.

---

**버전:** 1.0 (프로토타입)  
**마지막 업데이트:** 2026년 3월 10일  
**호환성:** Windows 11 PowerShell 5.1+, Python 3.8+
