# 05. 프로젝트 용어 사전 (Glossary)

본 문서는 `CLI Tutor Project`에서 사용하는 용어를 정의합니다.
본 프로젝트는 독립 배포가 가능하므로, 외부 참조 없이 이 문서만으로 용어를 이해할 수 있어야 합니다.

## 1. 관리 체계 용어 (Governance)

| 용어 | 명칭 | 정의 및 상세 설명 |
| :--- | :--- | :--- |
| **PPSCI** | 시스템 프레임워크 | **P**rogram, **P**roject, **S**ystem, **C**ategory, **I**tem의 약자로, 시스템의 5단계 관리 위계를 의미합니다. |
| **하이라키** | Hierarchy | 문서 간의 상하 종속 관계 및 권위 계층. Level 1(최고)부터 Level 5(최하)까지로 정의됩니다. |
| **순서** | Sequence | 동일 레벨 내에서의 실행 흐름이나 파일의 나열 순서. (`NN_` 또는 `NN_MM_` 접두사 활용) |

## 2. 운영 프로시저 용어 (SOP)

| 프로시저 | 영문 표기 | 정의 및 준수 사항 |
| :--- | :--- | :--- |
| **넘버링** | Numbering (NP) | 순서 제어를 위한 규칙. `NN_MM_Name.md` 형식을 준수합니다. |
| **컨트롤** | Control (CP) | 투명한 변경 관리 절차. 중요 변경은 Git 커밋(한글)으로 기록합니다. |
| **실행 프로시저** | Execution (EP) | [이해] → [단순화] → [시스템화] 과정을 통해 해결합니다. |

## 3. CLI Tutor 프로젝트 특화 용어 (Project Specific Terms)

| 용어 | 영문 명칭 | 정의 및 상세 설명 |
| :--- | :--- | :--- |
| **TUI** | Text User Interface | 그래픽 없이 터미널 상에서 텍스트와 레이아웃으로 구성되는 사용자 인터페이스 |
| **CLI** | Command-Line Interface | 키보드 명령어 입력으로만 제어하는 인터페이스 방식 |
| **PTY** | Pseudo-Terminal | 터미널 에뮬레이터가 프로세스와 통신하기 위해 사용하는 가상 터미널 장치 |
| **WinPTY** | Windows PTY | Windows 환경에서 PTY를 에뮬레이션하기 위한 래퍼 라이브러리 |
| **에이전트 패널** | Agent Panel | 사용자가 목표를 자연어로 입력하면, LLM이 시나리오를 단계별로 제시하는 TUI 구역 |
| **설명 패널** | Explanation Panel | 사용자가 실행한 명령어의 출력과 에러를 즉시 사람의 언어(한국어)로 해설해주는 TUI 구역 |
| **터미널 패널** | Terminal Panel | 사용자가 직접 셸 명령어를 타이핑하고 실행 결과를 확인하는 메인 TUI 구역 |
| **세션 패널** | Session Panel | 이전 작업 이력을 관리하고 세션 간 전환을 지원하는 좌측 TUI 구역 |
| **시나리오** | Scenario | LLM이 사용자의 목표를 분석하여 생성하는 단계별(Step-by-Step) 명령어 가이드 데이터 (JSON 형식) |
| **Setup 마법사** | Setup Wizard | 최초 실행 시 LLM 제공자 선택 및 API Key 입력을 안내하는 대화형 초기 설정 프로세스 |
| **Provider 패턴** | Provider Pattern | 단일 LLM에 종속되지 않도록 추상화 레이어를 두어 Groq, Perplexity, Gemini 등을 교체 가능하게 하는 설계 방식 |
| **EnvInfo** | Environment Info | OS, 아키텍처, WSL 여부 등 사용자 시스템 환경을 자동 감지하는 유닛 클래스 |
| **ConfigManager** | Config Manager | 로컬 JSON 파일(`~/.cli-tutor/config.json`)에 API Key 등 설정을 영속적으로 저장하고 관리하는 유닛 클래스 |

## 4. 기술 용어 (Technical Terms)

| 용어 | 정의 |
| :--- | :--- |
| **Textual** | Python 기반 비동기 TUI 프레임워크. 이벤트 루프와 CSS 유사 스타일링을 지원 |
| **Rich** | Python 기반 터미널 텍스트 스타일링 라이브러리. Panel, Table, Text 등 다양한 위젯을 제공 |
| **Groq** | LPU(Language Processing Unit) 기반의 초고속 LLM 추론 API 서비스. 무료 티어 제공 |
| **httpx** | Python 기반 비동기 지원 HTTP 클라이언트 라이브러리 |

---
> [!NOTE]
> 본 용어 사전은 프로젝트 독립 운영을 위해 필요한 모든 용어를 자체적으로 포함하고 있습니다.
