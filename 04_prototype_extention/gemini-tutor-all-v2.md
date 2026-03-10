# Gemini Tutor CLI 통합 설계서 (Concept + LLM/환경 설정) - v2.0

> 이 문서는 `Gemini CLI 튜터형 터미널 에이전트`를 실제로 구현하기 위한 **완전체 스펙 1본**이다.
> 
> - 1부: 철학 · 취지 · UX · 기능 · 화면 레이아웃 · 시나리오 (개념/기능 스펙)
> - 2부: LLM(API) 선택 · 무료 키 세팅 · OS/환경 자동 감지 · Setup 마법사 (구현 지향 스펙)
>
> 이 한 파일만 LLM에 넣고 "이대로 Python/Go/Rust/Node로 구현해줘"라고 요청하면 된다.

---

## 📌 v2.0 변경사항

### 새로운 LLM 지원 (3가지 선택 가능)

1. **Groq** (기본값, 추천) ⭐
   - 모델: `openai/gpt-oss-120b` (또는 최신 OSS 모델)
   - 무료 티어: RPM 30, 일 14,400 요청
   - 스트리밍 지원 O

2. **Perplexity** (검색 기반 답변)
   - 검색 결과 기반의 최신 정보 제공
   - 웹 검색 통합
   - 스트리밍 지원 O

3. **Google Gemini** (선택 사항)
   - 모델: `gemini-2.0-flash`
   - 무료 티어: 일 250 요청
   - 스트리밍 지원 O

### API 키 관리 개선

- Setup 마법사에서 사용할 LLM 선택
- 각 LLM별 독립적인 API 키 입력/저장
- 환경 변수로도 설정 가능
- 여러 LLM을 동시에 설정 가능 (장애 시 대체)

---

## 1부. Gemini CLI 튜터형 터미널 에이전트 기획서 (개념/기능 스펙)

### 1. 철학과 취지

#### 1.1 사용자의 페인 포인트

1. **복붙 개발**
   - 인터넷/AI가 준 명령어를 터미널에 그대로 붙여넣어서 실행만 한다.
   - 명령이 **무엇을 의미하는지**, 옵션이 무슨 역할인지 모른다.
   - 에러가 나면 왜 났는지, 무엇을 바꿔야 하는지 스스로 판단하기 어렵다.

2. **안티그래비티/에이전트의 과도한 \"accept\" UX**
   - 명령을 실행할 때마다 \"accept?\"를 누르라고 나오는데, 
     사용자 입장에서는 **무엇을 허용하는지** 정확히 알지 못한다.
   - 결국 생각 없이 계속 `accept`를 누르게 되어, 보안/학습 두 측면 모두 나쁘다.

3. **환경 의존 에러 (예: 인텔 맥에서 Node 설치 문제)**
   - Node 공식 설치 스크립트가 더 이상 인텔 맥을 제대로 지원하지 않는 경우처럼, 
     OS/아키텍처 때문에 생기는 에러는 초보자가 직관적으로 이해하기 어렵다.
   - \"내가 뭘 잘못한 건지\" vs \"환경/버전 문제인지\"를 구분해 줄 도구가 필요하다.

4. **컨텍스트 전환 비용**
   - 브라우저, IDE, 웹 기반 AI 에이전트 등으로 왔다갔다 하면서 작업하면 흐름이 끊긴다.
   - 사용자는 **\"터미널 하나만 열어두고 그 안에서 질문, 실행, 학습까지 다\"** 하고 싶어 한다.

#### 1.2 이 도구가 지향하는 것

1. **터미널 안의 튜터(Tutor)**
   - 단순히 명령어를 \"대신 쳐주는 에이전트\"가 아니라, 
     사용자가 치는 명령 하나하나의 의미를 **설명**해주고, 
     출력과 에러를 **해석**해 주는 \"튜터\" 역할.

2. **반자동(Assistive), 완전자동(Auto) 아님**
   - 핵심 철학: 도구가 시스템을 마음대로 바꾸지 않는다.
   - 항상 사람이 **\"이 명령이 뭘 하는지 이해한 뒤에\"** Enter를 칠 수 있도록 설계한다.
   - 자동 실행은 읽기 전용/안전한 범위에서만 제한적으로 허용한다.

3. **학습 중심 워크플로**
   - \"지금 단계에서 잘 되고 있는지\"를 명확히 알려주고,
   - \"다음에는 보통 어떤 명령을 치는지\"를 제안해 준다.
   - 세션이 끝나면 오늘 한 작업과 배운 점을 요약해 준다.

4. **CLI/TUI Only (No GUI)**
   - 전부 터미널 안에서 작동하는 **텍스트 UI**만 사용한다.
   - 나중에 웹/GUI로 확장 가능하지만, 이 명세의 1차 목표는 CLI/TUI이다.

---

### 2. 전체 개념 요약

#### 2.1 한 줄 설명

> \"터미널 안에 상주하는 Groq/Perplexity/Gemini 기반 튜터 에이전트.
> 좌측에서 세션 관리, 가운데에서 실제 셸 명령 실행,
> 우측에서 '방금 명령 해설'과 '다음 단계 가이드'를 동시에 보여준다.\"

#### 2.2 핵심 역할

1. **CLI 코파일럿**: 자연어 → 셸 명령 세트 추천 및 위험도 안내.
2. **실행 모니터**: 명령 실행 후 성공/실패/경고를 판정하고 요약.
3. **튜터**: 각 명령/에러/로그에 대해 의미를 설명해 주는 교사.
4. **가이드**: 사용자의 목표를 단계별 시나리오(1,2,3번)로 쪼개서 안내.
5. **세션 기록자**: 오늘 한 작업 흐름을 나중에 복습할 수 있게 정리.

---

### 3. 화면 레이아웃 설계 (CLI/TUI)

#### 3.1 3-컬럼 + 우측 2단 구조

터미널 전체를 아래와 같이 나눈다.

- **좌측**: 세션/TAB 목록
- **가운데**: 실제 셸 입력/출력 (메인 터미널)
- **우측 상부**: 방금 실행한 명령의 설명/결과 해석 패널
- **우측 하부**: 다음에 할 작업/명령을 제안하는 에이전트 패널

#### 3.2 ASCII 와이어프레임

```text
┌────────────────┬──────────────────────────────┬──────────────────────────────┐
│  세션/TAB 목록 │          메인 터미널        │     에이전트 패널 (우측)     │
│                │  (실제 셸 입력/출력)       │                              │
│ [1] app-back   │                              │ ┌──────────────────────────┐ │
│ [2] infra-dev  │  user@host:~/proj $ _       │ │ 우측 상부: 해설 패널     │ │
│ [3] node-exp   │                              │ │ - 방금 실행한 명령어    │ │
│ [4] db-test    │  (여기가 진짜 bash/zsh)    │ │ - 출력 요약/의미        │ │
│ [+ 새 세션]    │                              │ │ - 성공/실패 판단        │ │
└────────────────┴──────────────────────────────┤ └──────────────────────────┘ │
                                               │ ┌──────────────────────────┐ │
                                               │ │ 우측 하부: 에이전트/가이드││
                                               │ │ - 하고 싶은 일 질의      ││
                                               │ │ - 1,2,3 단계 제안        ││
                                               │ │ - 각 단계 명령 설명      ││
                                               │ └──────────────────────────┘ │
                                               └──────────────────────────────┘
```

#### 3.3 각 영역 역할 요약

1. **좌측 세션 패널**
   - 여러 작업(프로젝트/실험)을 세션 단위로 관리.
   - 예: `[1] node-env-intel`, `[2] docker-lab`, `[3] infra-tools`, `[+ 새 세션]`.
   - 단축키/명령으로 세션 생성, 이름 변경, 종료.

2. **가운데 메인 터미널**
   - 실제로 사용자가 명령을 치는 곳.
   - 평소와 동일한 bash/zsh 환경.
   - 명령이 끝날 때마다 마지막 명령/exit code/출력을 후킹해서 우측 패널에 전달.

3. **우측 상부 해설 패널**
   - \"방금 실행한 명령\"과 그 출력이 뭔지 설명.
   - 성공 여부, 경고 여부, 다음으로 보통 하는 명령을 제안.

4. **우측 하부 에이전트 패널**
   - 사용자가 하고 싶은 일을 자연어로 입력.
   - 에이전트가 1,2,3… 단계 시나리오와 각 단계 명령, 설명을 제안.
   - 사용자는 번호를 선택해 가운데 터미널에서 실행.

---

### 4. 사용자 시나리오 예시

#### 4.1 시나리오 1: 인텔 맥에서 Node LTS 환경 세팅

1. 사용자가 우측 하부 패널에 입력

   ```text
   > 하고 싶은 일: 인텔 맥에서 Node LTS 개발 환경 세팅
   ```

2. 에이전트가 우측 하부에 시나리오 제안

   ```text
   [목표]
   인텔 맥에서 Node LTS 버전 개발 환경 세팅

   [추천 시나리오]
   1. Homebrew 설치/상태 확인
      - 명령: brew --version
      - 의미: Homebrew가 설치되어 있고 정상 동작하는지 확인합니다.

   2. nvm 설치
      - 명령: brew install nvm
      - 의미: 여러 Node 버전을 쉽게 관리할 수 있는 nvm을 설치합니다.

   3. Node LTS 설치
      - 명령: nvm install --lts
      - 의미: 장기 지원(LTS) 버전의 Node를 설치합니다.

   [사용법]
   - 가운데 터미널에서 1번 명령을 먼저 실행하세요.
   - 실행이 끝나면, 우측 상부 패널에서 결과/의미를 확인할 수 있습니다.
   ```

3. 사용자는 가운데 터미널에서 1번 명령 실행

   ```bash
   brew --version
   ```

4. 명령이 끝나면 우측 상부 해설 패널 갱신

   ```text
   [명령어]
   brew --version

   [이 명령이 하는 일]
   - 설치된 Homebrew 버전 정보를 확인합니다.
   - Homebrew가 아예 설치되지 않은 경우 에러가 발생할 수 있습니다.

   [실행 결과 요약]
   - exit code: 0 (성공)
   - 출력: Homebrew 4.3.0

   [판단]
   ✓ Homebrew가 정상 설치되어 있습니다.
   → 다음 단계: 우측 하단 패널의 2번(nvm 설치)으로 진행하세요.
   ```

5. 이런 식으로 2번, 3번… 단계까지 반복.
   - 중간에 에러가 나면 상부 패널에서 에러 해설 + 수정 제안.
   - 하부 패널에서는 \"에러 브랜치\"에 맞는 새로운 시나리오를 제안.

---

### 5. 기능 요구사항 (Functional Requirements)

#### 5.1 코어 기능

1. **자연어 → 명령어 생성**
   - 입력: \"내가 하고 싶은 일\" (한글/영문 자유).
   - 출력: 단계별 시나리오 (1,2,3 …) + 각 단계의 셸 명령 + 짧은 설명.
   - 요구사항:
     - OS(맥/리눅스/윈도WSL 등)와 아키텍처(인텔/ARM 등)를 고려.
     - 위험도가 있는 명령(`rm -rf`, `sudo`, 시스템 설정 변경 등)에 경고 표시.

2. **명령 실행 후 결과 분석**
   - 입력: 마지막으로 실행된 명령 문자열, exit code, stdout/stderr 일부.
   - 출력: 
     - 명령의 역할 설명.
     - 출력 요약 (성공/실패/경고 요약).
     - 성공 시: 다음에 이어서 할 만한 명령 제안.
     - 실패 시: 에러 해석, 흔한 원인, 추천 해결 순서.

3. **에러 자동 감지 옵션**
   - 명령 종료 시 exit code != 0이면:
     - 자동으로 해설 패널을 갱신하거나,
     - \"에러 감지됨, 설명을 볼까요? (y/n)\" 같은 간단한 프롬프트 제공.

4. **목표 기반 워크플로 (가이드 모드)**
   - 사용자가 큰 목표를 적으면, 내부적으로 체크리스트/단계를 계획.
   - 각 단계마다:
     - 필요한 명령 제안
     - 명령 설명
     - 검증 방법(`--version`, `ls`, `curl` 등)을 함께 제안

#### 5.2 튜터/학습 기능

1. **레벨별 설명 모드**
   - `beginner`:
     - 개념 위주 설명, 비유, 긴 문장 허용.
   - `intermediate`:
     - 옵션/플래그 설명과 같은 기술적 내용 중심.
   - `advanced`:
     - 최소한의 설명 + 공식 문서 링크 요약 정도.

2. **명령어 해설 자동 출력**
   - beginner 모드에서는, 해설 패널에 항상
     - \"무엇을 하는 명령인지\" 
     - \"언제/왜 쓰는지\"
     를 3~5줄로 추가.

3. **세션 요약 기능**
   - `:summarize` 명령으로 현재 세션 전체를 요약:
     - 어떤 목표로 시작했는지.
     - 어떤 명령들을 순서대로 실행했는지.
     - 어디서 막혔고 어떻게 해결했는지.
   - 결과를 마크다운 파일로 저장 (예: `~/.g-tutor/sessions/YYYYMMDD-HHMM.md`).

#### 5.3 세션/메모리 기능

1. **세션별 상태 저장**
   - 세션 이름, 현재 목표, 진행 단계, 마지막 에러 상태 등을 로컬에 저장.
   - 다음에 같은 세션을 열면, 이전 작업 맥락을 불러온다.

2. **민감 정보 마스킹**
   - 홈 디렉터리 전체 경로, 토큰, 비밀번호, 쿠키 등은 LLM에 보내기 전에 마스킹.
   - 이벤트/로그 저장 시에도 민감 정보는 기록하지 않도록 규칙 적용.

#### 5.4 안전/승인 UX

1. **모드: 자동/수동**
   - `manual` (기본): 
     - 에이전트는 명령만 제안하고, 실제 실행은 사용자가 가운데 터미널에서 직접 한다.
   - `semi-auto`:
     - 읽기 전용/안전 명령(`ls`, `cat`, `grep`, `git status` 등)은 자동 실행 허용.
   - `auto` (옵션):
     - 신뢰도 높은 환경에서만, 일부 작업을 완전자동으로 수행.

2. **위험 명령 경고**
   - 파일 삭제, 시스템 패키지 제거, 네트워크/방화벽 설정 변경 등은 항상:
     - 자연어 설명 + 확인 질의 후에만 실행.
     - 예: \"이 명령은 ~/logs 디렉터리 아래의 *.log 파일을 모두 삭제합니다. 진행할까요? (y/N)\".

3. **롤백 힌트**
   - Git 작업인 경우:
     - \"방금 작업을 되돌리고 싶다면: `git reset --hard HEAD~1`\" 같이 롤백 명령을 함께 제시.

---

### 6. 기술 설계 (언어/프레임워크 무관 공통 아키텍처)

#### 6.1 고레벨 구조

1. **Main TUI/CLI 프로세스**
   - 화면 레이아웃 관리 (좌/중/우 패널).
   - 키보드 입력/포커스 관리.

2. **Shell Hook/Wrapper 레이어**
   - 가운데 패널에 실제 셸(bash/zsh)을 붙이거나, 
     셸 프로세스를 child process로 띄운 뒤 입출력을 중계.
   - 명령 종료 이벤트를 감지하여:
     - 마지막 명령 문자열
     - exit code
     - stdout/stderr 일부
     를 에이전트에게 넘김.

3. **LLM 에이전트 백엔드**
   - Groq / Perplexity / Gemini 중 선택한 LLM을 호출하는 모듈.
   - 기능:
     - 자연어 목표 → 단계별 시나리오 + 명령어 생성.
     - 명령/출력 → 해설/판정 텍스트 생성.

4. **로컬 스토리지 레이어**
   - 세션 상태, 요약, 설정, 안전 모드 옵션 등을 파일/DB에 저장.

#### 6.2 데이터 구조(개략)

- `CommandExecution` 구조체 예시:

  ```text
  CommandExecution {
    session_id: string,
    timestamp: datetime,
    command: string,
    exit_code: int,
    stdout_tail: string,   # 마지막 N줄 정도
    stderr_tail: string,
  }
  ```

- `StepPlan` 구조체 예시:

  ```text
  StepPlan {
    goal: string,          # 사용자의 자연어 목표
    steps: [
      {
        index: int,        # 1,2,3...
        title: string,     # 단계 이름
        command: string,   # 실제 셸 명령어 (비워둘 수도 있음)
        explanation: string,
        caution: string?,  # 위험/주의 사항 (옵션)
      },
      ...
    ]
  }
  ```

---

### 7. 구현 언어별 가이드 (개략)

> 이 섹션은 실제 코드를 쓰기 위한 것이 아니라, 
> LLM이 언어별 특성을 고려해 최적화된 구현을 설계할 수 있도록 힌트를 주는 용도이다.

#### 7.1 Python 버전 (프로토타입 용)

- 장점
  - 개발 속도가 빠르고, LLM이 코드 생성을 잘 한다.
  - Textual, Rich, urwid 등 강력한 TUI 프레임워크가 존재.
- 단점
  - 인터프리터 언어라 고성능이 필요하면 한계가 있을 수 있음.
  - 하지만 이 툴의 메인 병목은 LLM 호출이므로, 보통은 충분하다.

#### 7.2 Go / Rust 버전 (고성능/배포 용)

- 공통 요구
  - 단일 바이너리로 배포.
  - 외부 의존성 최소화.
  - 비동기 I/O로 셸 입출력과 LLM 스트림을 동시에 처리.

- Go
  - 장점: 빌드/배포 용이, 병행 처리(goroutine) 편리.
  - TUI: tview, bubbletea 등 사용 가능.

- Rust
  - 장점: 성능과 안정성.
  - TUI: ratatui 등 사용 가능.

#### 7.3 Node.js 버전

- 장점
  - 이미 Node 기반 개발 환경인 사용자에게 익숙.
  - 다양한 CLI/TUI 라이브러리(ink, blessed 등).
- 단점
  - Node 설치가 어려운 환경(예: 일부 인텔 맥)에서는 초기 진입 장벽.

> LLM에게 구현을 요청할 때: 
> \"이 명세에 따라, Python(Textual) 기반 프로토타입을 먼저 만들고,
> 후속으로 Go(bubbletea) 기반 고성능 버전을 설계해줘\" 같은 식으로 구체적으로 요구할 수 있다.

---

## 2부. LLM & 환경 설정 상세 설계서 (LLM/API + OS 감지 + Setup)

이 2부는 실제로 프로그램을 만들 때 필요한:

- 어떤 LLM을 어떤 무료 플랜으로 어떻게 붙이는지,
- 어떤 OS/환경인지 자동으로 인지하는 방법,
- 초기 설정 마법사(Setup) 플로우

까지 구체적으로 정의한다.

---

### 1. 지원 LLM 및 기본 전략 (v2.0 업데이트)

#### 1.1 1차 타겟: Groq (기본, 무료 티어, 스트리밍)

- **상태:** 기본값 (추천)
- **무료 키:** https://console.groq.com 에서 무료 발급
- **모델:** `openai/gpt-oss-120b` (또는 최신 OSS 모델)
- **무료 티어:**
  - RPM (분당 요청): 30
  - RPD (일일 요청): 14,400
- **특징:**
  - ✅ 스트리밍 지원 (실시간 응답)
  - ✅ 매우 빠름 (지연 시간 <1초)
  - ✅ 오픈소스 모델 지원
  - ✅ 신용카드 불필요

##### 1.1.1 Groq API 키 발급 요약 (사용자 가이드용)

1. 브라우저에서 `https://console.groq.com` 접속
2. 계정 생성 또는 로그인
3. 좌측 메뉴 **\"API Keys\"** 클릭
4. **\"Create New API Key\"** 버튼 클릭
5. 생성된 키를 복사
6. 이 튜터 프로그램의 Setup 마법사에 입력

##### 1.1.2 Groq 코드 예시 (스트리밍)

```python
from groq import Groq

client = Groq(api_key=\"YOUR_GROQ_API_KEY\")

completion = client.chat.completions.create(
    model=\"openai/gpt-oss-120b\",  # 또는 최신 OSS 모델
    messages=[
        {\"role\": \"user\", \"content\": \"Python 개발 환경을 세팅해줘\"}
    ],
    temperature=0.3,
    max_completion_tokens=2048,
    stream=True  # 스트리밍 활성화
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end=\"\", flush=True)
```

---

#### 1.2 2차 타겟: Perplexity (검색 기반, 스트리밍)

- **상태:** 선택 사항
- **무료 키:** https://www.perplexity.ai 에서 발급 (Pro 구독 필요 또는 무료 클레임)
- **특징:**
  - ✅ 웹 검색 기반 최신 정보 제공
  - ✅ 스트리밍 지원
  - ✅ 출처 명시
  - ✅ 높은 응답 품질

##### 1.2.1 Perplexity API 키 발급 요약

1. 브라우저에서 `https://www.perplexity.ai` 접속
2. 계정 생성 또는 로그인
3. 설정에서 **\"API\"** 또는 **\"Developers\"** 섹션 찾기
4. API 키 생성
5. Setup 마법사에 입력

##### 1.2.2 Perplexity 코드 예시

```python
from perplexity import Perplexity

client = Perplexity(api_key=\"YOUR_PERPLEXITY_API_KEY\")

search = client.search.create(
    query=\"최신 Python 개발 환경 세팅 방법\",
    max_results=5,
    max_tokens=2000
)

for result in search.results:
    print(f\"제목: {result.title}\")
    print(f\"URL: {result.url}\")
    print(f\"내용: {result.content}\\n\")
```

---

#### 1.3 3차 타겟: Google Gemini (선택 사항, 무료 티어)

- **상태:** 선택 사항 (백업/대체용)
- **무료 키:** `https://aistudio.google.com` 에서 무료 발급
- **모델:** `gemini-2.0-flash`
- **무료 티어:**
  - 일일 요청: ~250
  - 분당 요청: ~10
- **특징:**
  - ✅ 한국어 지원 우수
  - ✅ 높은 응답 품질
  - ✅ 신용카드 불필요

##### 1.3.1 Gemini API 키 발급 요약

1. 브라우저에서 `https://aistudio.google.com` 접속
2. Google 계정으로 로그인
3. **\"Get API key\"** 버튼 클릭
4. **\"Create API key in new project\"** 선택
5. 생성된 키 복사
6. Setup 마법사에 입력

##### 1.3.2 Gemini 코드 예시

```python
import google.generativeai as genai

genai.configure(api_key=\"YOUR_GEMINI_API_KEY\")

model = genai.GenerativeModel(\"gemini-2.0-flash\")

response = model.generate_content(\"Python 개발 환경을 세팅해줘\")

print(response.text)
```

---

#### 1.4 LLM 선택 정책 (Setup 마법사)

프로그램 초기 설정 단계에서:

1. **기본값:** Groq 선택 (가장 추천)
2. **사용자 선택:** Groq / Perplexity / Gemini 중 자유 선택
3. **멀티 LLM 지원:** 여러 API 키 동시 저장 가능
   - 주 LLM: Groq
   - 보조 LLM: Perplexity
   - 백업 LLM: Gemini

```yaml
# ~/.g-tutor/config.yaml (예시)

llm:
  primary: groq           # 기본 LLM
  fallback: perplexity    # 대체 LLM (Groq 장애 시)
  backup: gemini          # 백업 LLM
  
  groq:
    api_key_env: GROQ_API_KEY
    model: openai/gpt-oss-120b
    temperature: 0.3
    max_tokens: 2048
    
  perplexity:
    api_key_env: PERPLEXITY_API_KEY
    max_results: 5
    max_tokens: 2000
    
  gemini:
    api_key_env: GEMINI_API_KEY
    model: gemini-2.0-flash
    temperature: 0.3
    max_tokens: 1024
```

---

### 2. LLM API 연결 상세 (실제 호출 관점)

#### 2.1 공통 인터페이스

```text
interface LLMClient {
  GenerateChat(
    system_prompt: string,
    messages: [ { role: \"user\" | \"assistant\" | \"system\", content: string } ],
    temperature: float,
    max_tokens: int,
    stream: bool = false
  ) -> string or Stream
}
```

`GroqClient`, `PerplexityClient`, `GeminiClient` 세 구현체를 두고, 설정에 따라 주입한다.

#### 2.2 스트리밍 지원

Groq와 Perplexity는 스트리밍 지원:

```python
# 스트리밍 사용 예시
for chunk in llm_client.generate_chat_stream(prompt):
    print(chunk, end=\"\", flush=True)
```

---

### 3. 환경(OS/플랫폼) 자동 감지 설계

#### 3.1 구분하고 싶은 케이스

1. 순수 Windows (PowerShell / cmd)
2. Windows 안에서 WSL (Ubuntu 등)
3. macOS (인텔 / Apple Silicon)
4. Linux (x86_64 / ARM 등)

#### 3.2 감지 전략 개요

##### 3.2.1 운영체제 기본 구분

- POSIX 계열 (macOS, Linux, WSL)에서는 `uname` 기반:
  - `uname -s` → `Linux`, `Darwin` 등
  - `uname -m` → `x86_64`, `arm64`, `aarch64` 등
- Windows 네이티브:
  - 언어별 `os.platform() == \"win32\"` (Node), `os.name == \"nt\"` (Python), `runtime.GOOS == \"windows\"` (Go) 등으로 판단.

##### 3.2.2 WSL 감지

- WSL 환경에서는 `/proc/version` 또는 `/proc/sys/kernel/osrelease`에 `WSL`/`Microsoft` 문자열이 포함되어 있음.

##### 3.2.3 macOS 인텔 vs Apple Silicon

- `uname -m` 결과:
  - `x86_64` → 인텔
  - `arm64` → Apple Silicon (M1/M2/M3…)

#### 3.3 환경 감지 예시 로직 (의사 코드)

```text
function detect_environment() -> EnvInfo:
  if windows_native():
    if is_wsl():
      return EnvInfo(os_type=\"wsl\", arch=read_uname_m(), detail=\"wsl-\" + read_distro())
    else:
      return EnvInfo(os_type=\"windows\", arch=read_arch_win(), detail=\"windows-native\")
  else:
    kernel = run(\"uname -s\")
    arch   = run(\"uname -m\")

    if kernel == \"Darwin\":
      if arch == \"x86_64\":
        return EnvInfo(os_type=\"macos\", arch=\"x86_64\", detail=\"macos-intel\")
      elif arch == \"arm64\":
        return EnvInfo(os_type=\"macos\", arch=\"arm64\", detail=\"macos-apple-silicon\")
      else:
        return EnvInfo(os_type=\"macos\", arch=\"other\", detail=\"macos-unknown\")
    elif kernel == \"Linux\":
      if is_wsl():
        return EnvInfo(os_type=\"wsl\", arch=arch, detail=\"wsl-\" + read_distro())
      else:
        return EnvInfo(os_type=\"linux\", arch=arch, detail=\"linux-native\")
    else:
      return EnvInfo(os_type=\"unknown\", arch=arch, detail=\"unknown\")
```

---

### 4. 초기 설정(Setup) 플로우 설계 (v2.0 업데이트)

#### 4.1 CLI/TUI 기반 설정 마법사

##### 4.1.1 첫 실행 시 플로우

1. 프로그램 실행 → 설정 파일(~/.g-tutor/config.yaml) 없으면 Setup 모드 진입.
2. 환경 감지: `EnvInfo` 출력 예시:

   ```text
   [환경 감지 결과]
   - OS: Windows
   - Arch: x86_64
   - Detail: windows-native
   ```

3. **LLM 선택 질문** (v2.0 변경):

   ```text
   사용할 LLM 제공자를 선택하세요 (추천: Groq).
   1) Groq (빠름, 추천) ⭐
   2) Perplexity (검색 기반)
   3) Google Gemini (한국어 우수)
   선택 (기본: 1) >
   ```

4. 선택에 따라 API 키 입력 가이드:

   - 예: Groq 선택 시

     ```text
     [Groq API 키 설정]

     1. 브라우저에서 https://console.groq.com 에 접속합니다.
     2. 로그인/가입 후, \"API Keys\" 메뉴에서 새 키를 만듭니다.
     3. 생성된 키를 복사해서 아래에 붙여넣으세요.

     API 키를 지금 터미널에 직접 입력하시겠습니까?
     1) 네, 여기서 입력 (config 파일에 저장)
     2) 아니요, 환경 변수로 나중에 설정하겠습니다 (GROQ_API_KEY)
     선택 (기본: 1) >
     ```

5. 키 입력/저장 후, 설정 요약을 보여주고 종료:

   ```text
   [설정 요약]

   - OS: windows
   - LLM: Groq (openai/gpt-oss-120b)
   - API 키: config.yaml 에 저장됨

   이제부터 'g-tutor' 명령을 실행하면
   튜터형 터미널 에이전트를 사용할 수 있습니다.
   ```

---

### 5. 개발용 설정 예시 (환경 변수 / config 파일)

#### 5.1 환경 변수 방식 (빠른 테스트용)

```bash
# Groq
export GROQ_API_KEY=\"YOUR_GROQ_API_KEY\"

# Perplexity
export PERPLEXITY_API_KEY=\"YOUR_PERPLEXITY_API_KEY\"

# Gemini
export GEMINI_API_KEY=\"YOUR_GEMINI_API_KEY\"
```

#### 5.2 설정 파일 예시 (YAML)

```yaml
# ~/.g-tutor/config.yaml

env:
  os_type: auto   # auto: 프로그램이 자동 감지
  arch: auto

llm:
  primary: groq                    # 기본 LLM
  fallback: perplexity             # 백업
  backup: gemini
  
  groq:
    api_key_env: GROQ_API_KEY
    model: openai/gpt-oss-120b
    temperature: 0.3
    max_tokens: 2048
    
  perplexity:
    api_key_env: PERPLEXITY_API_KEY
    max_results: 5
    max_tokens: 2000
    
  gemini:
    api_key_env: GEMINI_API_KEY
    model: gemini-2.0-flash
    temperature: 0.3
    max_tokens: 1024

safety:
  mode: manual               # manual | semi-auto | auto
  allow_dangerous_commands: false

ui:
  theme: default
  show_beginner_explanations: true
  explanation_level: beginner   # beginner | intermediate | advanced
```

---

## 결론

이 v2.0 설계서는:

- ✅ Groq (기본, 권장)
- ✅ Perplexity (검색 기반 대안)
- ✅ Gemini (백업)

**3가지 LLM을 모두 지원**하며, Setup 마법사에서 쉽게 선택할 수 있도록 설계되었다.

각 LLM은 **독립적인 API 키**를 가지고, 스트리밍 지원으로 **실시간 응답**을 제공한다.

---

**버전:** 2.0  
**업데이트:** 2026년 3월 10일  
**호환성:** Windows 11 PS 5.1+, macOS, Linux  
**라이선스:** MIT (자유 이용)
