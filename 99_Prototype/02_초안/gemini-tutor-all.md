# Gemini Tutor CLI 통합 설계서 (Concept + LLM/환경 설정)

> 이 문서는 `Gemini CLI 튜터형 터미널 에이전트`를 실제로 구현하기 위한 **완전체 스펙 1본**이다.
> 
> - 1부: 철학 · 취지 · UX · 기능 · 화면 레이아웃 · 시나리오 (개념/기능 스펙)
> - 2부: LLM(API) 선택 · 무료 키 세팅 · OS/환경 자동 감지 · Setup 마법사 (구현 지향 스펙)
>
> 이 한 파일만 LLM에 넣고 “이대로 Python/Go/Rust/Node로 구현해줘”라고 요청하면 된다.

---

## 1부. Gemini CLI 튜터형 터미널 에이전트 기획서 (개념/기능 스펙)

### 1. 철학과 취지

#### 1.1 사용자의 페인 포인트

1. **복붙 개발**
   - 인터넷/AI가 준 명령어를 터미널에 그대로 붙여넣어서 실행만 한다.
   - 명령이 **무엇을 의미하는지**, 옵션이 무슨 역할인지 모른다.
   - 에러가 나면 왜 났는지, 무엇을 바꿔야 하는지 스스로 판단하기 어렵다.

2. **안티그래비티/에이전트의 과도한 "accept" UX**
   - 명령을 실행할 때마다 "accept?"를 누르라고 나오는데, 
     사용자 입장에서는 **무엇을 허용하는지** 정확히 알지 못한다.
   - 결국 생각 없이 계속 `accept`를 누르게 되어, 보안/학습 두 측면 모두 나쁘다.

3. **환경 의존 에러 (예: 인텔 맥에서 Node 설치 문제)**
   - Node 공식 설치 스크립트가 더 이상 인텔 맥을 제대로 지원하지 않는 경우처럼, 
     OS/아키텍처 때문에 생기는 에러는 초보자가 직관적으로 이해하기 어렵다.
   - "내가 뭘 잘못한 건지" vs "환경/버전 문제인지"를 구분해 줄 도구가 필요하다.

4. **컨텍스트 전환 비용**
   - 브라우저, IDE, 웹 기반 AI 에이전트 등으로 왔다갔다 하면서 작업하면 흐름이 끊긴다.
   - 사용자는 **"터미널 하나만 열어두고 그 안에서 질문, 실행, 학습까지 다"** 하고 싶어 한다.

#### 1.2 이 도구가 지향하는 것

1. **터미널 안의 튜터(Tutor)**
   - 단순히 명령어를 "대신 쳐주는 에이전트"가 아니라, 
     사용자가 치는 명령 하나하나의 의미를 **설명**해주고, 
     출력과 에러를 **해석**해 주는 "튜터" 역할.

2. **반자동(Assistive), 완전자동(Auto) 아님**
   - 핵심 철학: 도구가 시스템을 마음대로 바꾸지 않는다.
   - 항상 사람이 **"이 명령이 뭘 하는지 이해한 뒤에"** Enter를 칠 수 있도록 설계한다.
   - 자동 실행은 읽기 전용/안전한 범위에서만 제한적으로 허용한다.

3. **학습 중심 워크플로**
   - "지금 단계에서 잘 되고 있는지"를 명확히 알려주고,
   - "다음에는 보통 어떤 명령을 치는지"를 제안해 준다.
   - 세션이 끝나면 오늘 한 작업과 배운 점을 요약해 준다.

4. **CLI/TUI Only (No GUI)**
   - 전부 터미널 안에서 작동하는 **텍스트 UI**만 사용한다.
   - 나중에 웹/GUI로 확장 가능하지만, 이 명세의 1차 목표는 CLI/TUI이다.

---

### 2. 전체 개념 요약

#### 2.1 한 줄 설명

> "터미널 안에 상주하는 Gemini 기반 튜터 에이전트.
> 좌측에서 세션 관리, 가운데에서 실제 셸 명령 실행,
> 우측에서 '방금 명령 해설'과 '다음 단계 가이드'를 동시에 보여준다."

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
   - "방금 실행한 명령"과 그 출력이 뭔지 설명.
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
   - 하부 패널에서는 "에러 브랜치"에 맞는 새로운 시나리오를 제안.

#### 4.2 시나리오 2: 실패 예시 (패키지 설치 에러)

1. 사용자가 `npm install` 실행 → permission 에러 발생
2. 우측 상부 패널 예시

   ```text
   [명령어]
   npm install

   [에러 요약]
   - EACCES: permission denied 에러 발생.
   - 글로벌 디렉터리에 쓰기 권한이 없어서 발생하는 전형적인 문제입니다.

   [원인 후보]
   - 예전에 sudo npm install -g 를 많이 사용하여 권한 꼬임.
   - Node/npm이 root 권한 기준으로 설치됨.

   [추천 조치]
   1) 현재 프로젝트에 국한된 설치인지 확인 (글로벌 설치가 정말 필요한가?).
   2) nvm 또는 Volta 같은 버전 관리 도구로 Node 재설치 고려.
   3) 임시로는 chown/chmod로 npm 캐시/글로벌 디렉터리 권한을 조정할 수 있음.
   ```

---

### 5. 기능 요구사항 (Functional Requirements)

#### 5.1 코어 기능

1. **자연어 → 명령어 생성**
   - 입력: "내가 하고 싶은 일" (한글/영문 자유).
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
     - "에러 감지됨, 설명을 볼까요? (y/n)" 같은 간단한 프롬프트 제공.

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
     - "무엇을 하는 명령인지" 
     - "언제/왜 쓰는지"
     를 3~5줄로 추가.

3. **세션 요약 기능**
   - `:summarize` 명령으로 현재 세션 전체를 요약:
     - 어떤 목표로 시작했는지.
     - 어떤 명령들을 순서대로 실행했는지.
     - 어디서 막혔고 어떻게 해결했는지.
   - 결과를 마크다운 파일로 저장 (예: `~/.g-terminal-tutor/sessions/YYYYMMDD-HHMM.md`).

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
     - 예: "이 명령은 ~/logs 디렉터리 아래의 *.log 파일을 모두 삭제합니다. 진행할까요? (y/N)".

3. **롤백 힌트**
   - Git 작업인 경우:
     - "방금 작업을 되돌리고 싶다면: `git reset --hard HEAD~1`" 같이 롤백 명령을 함께 제시.

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
   - Google Gemini (또는 호환 LLM)를 호출하는 모듈.
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
> "이 명세에 따라, Python(Textual) 기반 프로토타입을 먼저 만들고,
> 후속으로 Go(bubbletea) 기반 고성능 버전을 설계해줘" 같은 식으로 구체적으로 요구할 수 있다.

---

### 8. tmux 스크립트/레이아웃 예시 (선택 사항)

> 여기서 말하는 **tmux 스크립트**는, 
> tmux를 사용해 위에서 정의한 3-컬럼 + 우측 2단 레이아웃을 자동으로 만드는 쉘 스크립트 예시이다.
> 이건 "레이아웃만 tmux에 맡기고, 각 패널에서 별도 프로그램을 띄우는" 방식이다.

#### 8.1 기본 tmux pane 분할 예시

```bash
# 새 세션 생성
tmux new-session -d -s tutor_session

# 1) 좌측 패널(세션 목록)을 유지한 상태에서
# 2) 우측에 메인 터미널 패널 생성 (수직 분할)
tmux split-window -h -p 70    # 오른쪽이 70%, 왼쪽이 30%

# 3) 우측 패널을 다시 수직 분할해서 (상·하 구조의 기반)
tmux split-window -v -p 50    # 아래가 50%

# 이제 대략 3개의 패널이 있음:
# - 좌: 세션 패널
# - 우상: 메인 터미널
# - 우하: 에이전트/해설용

# 각 패널에 원하는 프로그램 실행 (예: 우하 패널에 에이전트 CLI 실행)
# pane 인덱스는 환경에 따라 다를 수 있으므로, 실제 구현 시에는 tmux display -p 등을 사용해 식별.

# 마지막으로 세션에 attach
tmux attach -t tutor_session
```

#### 8.2 tmux 기반 레이아웃 vs TUI 내장 레이아웃

- tmux 스크립트 방식
  - 장점: 이미 있는 터미널 멀티플렉서를 활용, 구현 쉽고 안정적.
  - 단점: 레이아웃/단축키가 tmux에 종속, 윈도우/탭 개념이 tmux 중심.

- TUI 프레임워크(예: Python Textual, Go bubbletea 등) 내부 레이아웃
  - 장점: 완전히 커스텀 UI를 만들 수 있고, tmux가 없어도 동작.
  - 단점: 셸 에뮬레이션, 리사이즈, 포커스 등을 직접 관리해야 해서 구현 난이도↑.

> 추천: **1단계에서는 TUI(프레임워크) 기반으로 3-컬럼 레이아웃을 직접 만들고**,
> tmux는 선택적 지원으로 두는 방향이 이해하기 더 쉽고 이식성도 좋다.

---

## 2부. LLM & 환경 설정 상세 설계서 (LLM/API + OS 감지 + Setup)

이 2부는 실제로 프로그램을 만들 때 필요한:

- 어떤 LLM을 어떤 무료 플랜으로 어떻게 붙이는지,
- 어떤 OS/환경인지 자동으로 인지하는 방법,
- 초기 설정 마법사(Setup) 플로우

까지 구체적으로 정의한다.

---

### 1. 지원 LLM 및 기본 전략

#### 1.1 1차 타겟: Gemini API (무료 티어)

- Google AI Studio에서 발급 가능한 **무료 Gemini API 키**를 사용한다.
- 무료 키는 **Flash 계열 모델** 위주로 사용 가능하며, 하루/분당 요청 제한이 있다.
- 이 툴에서는 다음 모델을 기본값으로 가정한다.
  - `gemini-3-flash-preview` (또는 당시 AI Studio에서 무료로 허용하는 Flash 계열)

##### 1.1.1 Gemini API 키 발급 요약 (사용자 가이드용)

1. 브라우저에서 `https://aistudio.google.com` 또는 Gemini API 키 페이지 접속.
2. Google 계정으로 로그인.
3. 좌측 메뉴 또는 홈 화면에서 **“Get API key”** 버튼 클릭.
4. 새 프로젝트를 만들거나 기존 프로젝트를 선택 후 **Create API key**.
5. 생성된 키를 복사하여 안전한 곳에 보관.
6. 이 튜터 프로그램의 설정 파일 또는 환경 변수에 넣는다 (아래 2장 참조).

##### 1.1.2 Gemini 무료 티어 사용 범위 (개략)

- Gemini Developer API 무료 티어는 **일/분 단위 요청/토큰 제한**이 있으나, 개인 개발자 프로토타입에는 충분하다.
- Gemini CLI도 unpaid API key에 대해 **하루 250 요청, 분당 10 요청** 정도의 기본 무료 쿼터를 제공한다고 명시되어 있다.

> 구현 시에는 요청 전/후에 **간단한 rate-limit 보호 로직**을 두어,
> HTTP 429/Quota 초과 시 사용자에게 안내하도록 한다.

---

#### 1.2 2차 타겟: Groq Cloud (무료 티어, 대체 LLM)

- Groq Cloud는 **무료 Free Tier**로 Llama, Gemma 등 여러 오픈소스 모델을 제공한다.
- Free Tier 주요 특성 (예시, 시점에 따라 달라질 수 있음):
  - 분당 약 30 요청 (RPM)
  - 하루 14,400 요청 (RPD)
  - 분당 6,000 토큰 (TPM)
- 이 튜터 도구에서는 “백업/대체 LLM”으로 Groq을 선택할 수 있게 한다.

##### 1.2.1 Groq API 키 발급 요약

1. `https://console.groq.com` 접속 후 계정 생성.
2. 로그인 후 **API Keys** 메뉴에서 새 키 생성.
3. 생성된 키를 복사하여, 이 프로그램 설정에 넣는다.
4. Free Tier는 **크레딧 카드 없이** 일정 수준 무료 사용이 가능하다.

---

#### 1.3 LLM 선택 정책

프로그램 초기설정(Setup) 단계 또는 설정 파일에서:

- `llm.provider` : `gemini` / `groq` 중 선택 (기본값: `gemini`)
- `llm.model` : 각 provider별 기본값
  - `gemini` → `gemini-3-flash-preview` (또는 최신 무료 Flash)
  - `groq` → `llama-3.1-8b-instant` 또는 비슷한 “instant/cheap” 모델

사용자 변경 가능:

```yaml
# ~/.g-tutor/config.yaml (예시)

llm:
  provider: gemini        # gemini | groq
  model: gemini-3-flash-preview
  api_key_env: GEMINI_API_KEY
```

---

### 2. LLM API 연결 상세 (실제 호출 관점)

#### 2.1 공통 인터페이스

코드 레벨에서 LLM 호출은 다음과 같은 공통 인터페이스를 가진다.

```text
interface LLMClient {
  GenerateChat(
    system_prompt: string,
    messages: [ { role: "user" | "assistant" | "system", content: string } ],
    temperature: float,
    max_tokens: int
  ) -> string  # 모델이 생성한 텍스트
}
```

`GeminiClient`, `GroqClient` 두 구현체를 두고, 설정에 따라 주입한다.

---

#### 2.2 Gemini API 호출 개념

- 엔드포인트/라이브러리는 공식 문서/SDK 사용.
- 예를 들어 JavaScript SDK는 아래와 같은 형태:

```js
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const result = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Explain how AI works in a few words",
});
console.log(result.text);
```

프로토타입 설계에서는 다음만 고정적으로 사용:

- `model` : 설정값 (`gemini-3-flash-preview`)
- `temperature` : 0.2 ~ 0.4 사이  
- `max_tokens` : 1024 정도로 제한해 초기 비용 억제  

---

#### 2.3 Groq API 호출 개념

- Groq는 OpenAI 스타일의 API를 제공하며, Free Tier에서 Llama 3.x, Gemma 2 등 사용 가능.
- 기본 개념:
  - `https://api.groq.com/openai/v1/chat/completions`
  - Authorization: `Bearer YOUR_GROQ_API_KEY`
  - `model`: 예) `llama-3.1-8b-instant`  

프로토타입에서는:

```jsonc
POST /openai/v1/chat/completions
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    { "role": "system", "content": "...튜터용 시스템 프롬프트..." },
    { "role": "user", "content": "..." }
  ],
  "temperature": 0.2,
  "max_tokens": 1024
}
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
  - 언어별 `os.platform() == "win32"` (Node), `os.name == "nt"` (Python), `runtime.GOOS == "windows"` (Go) 등으로 판단.

##### 3.2.2 WSL 감지

- WSL 환경에서는 `/proc/version` 또는 `/proc/sys/kernel/osrelease`에 `WSL`/`Microsoft` 문자열이 포함되어 있음.

##### 3.2.3 macOS 인텔 vs Apple Silicon

- `uname -m` 결과:
  - `x86_64` → 인텔
  - `arm64` → Apple Silicon (M1/M2/M3…)

이를 바탕으로 다음과 같이 내부 구조체 정의:

```text
struct EnvInfo {
  os_type: "windows" | "wsl" | "macos" | "linux",
  arch:    "x86_64" | "arm64" | "other",
  detail:  string  # 예: "macos-intel", "macos-apple-silicon", "ubuntu-wsl"
}
```

초기화 시:

1. OS/arch 감지
2. OS/arch에 맞게 **기본 추천 명령 템플릿**을 선택 (예: Node 설치 방식 등).

---

#### 3.3 환경 감지 예시 로직 (의사 코드)

```text
function detect_environment() -> EnvInfo:
  if windows_native():
    if is_wsl():
      # WSL로 먼저 체크
      return EnvInfo(os_type="wsl", arch=read_uname_m(), detail="wsl-" + read_distro())
    else:
      return EnvInfo(os_type="windows", arch=read_arch_win(), detail="windows-native")
  else:
    # POSIX (Linux/macOS)
    kernel = run("uname -s")
    arch   = run("uname -m")

    if kernel == "Darwin":
      if arch == "x86_64":
        return EnvInfo(os_type="macos", arch="x86_64", detail="macos-intel")
      elif arch == "arm64":
        return EnvInfo(os_type="macos", arch="arm64", detail="macos-apple-silicon")
      else:
        return EnvInfo(os_type="macos", arch="other", detail="macos-unknown")
    elif kernel == "Linux":
      if is_wsl():
        return EnvInfo(os_type="wsl", arch=arch, detail="wsl-" + read_distro())
      else:
        return EnvInfo(os_type="linux", arch=arch, detail="linux-native")
    else:
      return EnvInfo(os_type="unknown", arch=arch, detail="unknown")
```

이 `EnvInfo`를 기반으로:

- Node 설치 관련 가이드에 사용할 명령 템플릿 결정
- 패키지 매니저 (`brew`, `apt`, `dnf`, `choco` 등) 선택
- 경고 문구 (예: “현재 macOS 인텔, Node 공식 패키지 일부 미지원” 등)를 맞춤 출력.

---

### 4. 초기 설정(Setup) 플로우 설계

#### 4.1 CLI/TUI 기반 설정 마법사

> 이 프로젝트의 철학상 **터미널 기반 TUI 설정 마법사**를 전제로 한다.

##### 4.1.1 첫 실행 시 플로우

1. 프로그램 실행 → 설정 파일(~/.g-tutor/config.yaml) 없으면 Setup 모드 진입.
2. 환경 감지: `EnvInfo` 출력 예시:

   ```text
   [환경 감지 결과]
   - OS: macOS
   - Arch: x86_64 (인텔)
   - Detail: macos-intel
   ```

3. LLM 선택 질문:

   ```text
   사용할 LLM 제공자를 선택하세요.
   1) Gemini (Google, 무료 티어 지원)
   2) Groq (Llama 등, 무료 티어 지원)
   선택 (기본: 1) >
   ```

4. 선택에 따라 API 키 입력 가이드:

   - 예: Gemini 선택 시

     ```text
     [Gemini API 키 설정]

     1. 브라우저에서 https://aistudio.google.com 에 접속합니다.
     2. Google 계정으로 로그인 후, "Get API key" 버튼을 눌러 새 API 키를 만듭니다.
     3. 생성된 키를 복사해서 아래에 붙여넣으세요.

     API 키를 지금 터미널에 직접 입력하시겠습니까?
     1) 네, 여기서 입력 (config 파일에 저장)
     2) 아니요, 환경 변수로 나중에 설정하겠습니다 (GEMINI_API_KEY)
     선택 (기본: 1) >
     ```

5. 키 입력/저장 후, 설정 요약을 보여주고 종료:

   ```text
   [설정 요약]

   - OS: macos-intel
   - LLM: Gemini (gemini-3-flash-preview)
   - API 키: config.yaml 에 저장됨

   이제부터 'g-tutor' 명령을 실행하면
   튜터형 터미널 에이전트를 사용할 수 있습니다.
   ```

---

### 5. 개발용 설정 예시 (환경 변수 / config 파일)

#### 5.1 환경 변수 방식 (빠른 테스트용)

```bash
# Gemini
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

# Groq
export GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

#### 5.2 설정 파일 예시 (YAML)

```yaml
# ~/.g-tutor/config.yaml

env:
  os_type: auto   # auto: 프로그램이 자동 감지, 아니면 강제로 override 가능
  arch: auto

llm:
  provider: gemini           # gemini | groq
  model: gemini-3-flash-preview
  api_key_env: GEMINI_API_KEY
  timeout_sec: 30

safety:
  mode: manual               # manual | semi-auto | auto
  allow_dangerous_commands: false

ui:
  theme: default
  show_beginner_explanations: true
  explanation_level: beginner   # beginner | intermediate | advanced
```

프로그램 로직:

1. `config.yaml` 로드
2. `env.os_type == "auto"` 이면 `detect_environment()` 실행
3. `llm.api_key_env` 에서 환경변수 조회
   - 없으면 `config.llm.api_key` 필드(옵션)를 보고, 둘 다 없으면 Setup 모드로 안내.

---

### 6. 이 설계서를 LLM에 사용할 때 예시 프롬프트

#### 6.1 Python + Textual + Gemini 프로토타입 요청

```text
아래 통합 명세서를 참고해서,
Python + Textual 기반으로 동작하는 최소 기능 프로토타입을 만들어줘.

요구사항:
- 실행 시 config.yaml을 읽거나 없으면 Setup 마법사(TUI)로 진입
- Setup 마법사에서:
  - 환경(OS/arch) 자동 감지
  - LLM provider로 Gemini만 일단 지원
  - 사용자가 Gemini API 키를 입력하면 ~/.g-tutor/config.yaml에 저장
- 메인 화면:
  - 좌/중/우 레이아웃(더미라도 괜찮음)
  - 가운데 패널: 사용자가 명령을 텍스트로 입력하면, 그냥 echo만 해도 됨
  - 우측 하부 패널: 사용자가 목표를 입력하면, Gemini API를 호출해서
    단계별 시나리오(최소 2단계)를 생성
  - 우측 상부 패널: 마지막 명령에 대한 더미 설명 또는 LLM 기반 설명
```

#### 6.2 Go + bubbletea + Groq 설계 요청

```text
아래 통합 명세서를 참고해서,
Go + bubbletea 기반으로 동작하는 설계와 일부 코드 예시를 작성해줘.

요구사항:
- LLM provider는 Groq를 기본값으로 사용
- 환경(OS/arch) 자동 감지 로직을 Go 코드로 구현
- bubbletea 모델 구조:
  - 좌/중/우 + 상/하 패널 구조
  - 가운데 패널은 실제 bash child process를 붙이는 대신,
    일단 '가짜 셸'로서 문자열을 쌓는 형태로 시작
- LLM 호출은 interface로 추상화하고, GroqClient 구현체만 추가
- config.yaml 로딩 및 환경 변수(GROQ_API_KEY) 사용 방법 포함
```

---

### 7. 결론

이 통합 설계서는 "터미널 안에서 돌아가는 Gemini 기반 튜터 에이전트"를 만들기 위한

- 철학/취지/UX/기능/화면 구조
- LLM(API) 선택과 무료 키 세팅 방법
- OS/아키텍처 자동 감지 로직
- 초기 Setup 마법사 플로우

를 한 번에 담고 있다.

이 파일 하나만 LLM에게 제공하고,
"이 스펙대로 Python/Go/Rust/Node로 최대한 빠르고 가벼운 CLI/TUI 프로그램을 만들어줘"라고 요청하면,
여러 언어 버전의 구현을 반복 생성/개선하는 데 활용할 수 있다.
