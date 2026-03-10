# 05. CLI Tutor Project Overview (사업/설계 개요)

본 문서는 **CLI Tutor** 서비스의 전체 프로젝트 설계를 조감하는 최상위 개요서입니다.
철학(`05_00_Philosophy.md`)을 상속받으며, 사전에 구축된 샘플 프로토타입의 구현체 분석을 바탕으로 제너럴 컨셉으로 확장된 아이디어를 정립합니다.

> **상위 거버넌스 참조**: `../../../Program/01_Philosophy.md`

---

## 1. 서비스 정의 (Service Definition)

| 구분 | 내용 |
| :--- | :--- |
| **서비스명** | **CLI Tutor (구 Gemini Tutor)** |
| **슬로건** | "내 터미널 속의 마스터" |
| **핵심 기능** | TUI(Text User Interface) 기반 다중 LLM 연동 CLI 명령어 학습 및 에러 해설 도구 |
| **서비스 유형** | 콘솔/터미널 애플리케이션 (CLI/TUI) |
| **타겟** | 개발 입문자, 서버 관리자, 새로운 CLI 도구 학습자 |

## 2. 해결하는 문제 (Problem Statement)

> 오류가 발생할 때마다 구글을 검색하고, 터미널과 브라우저 사이를 오가는(Context Switching) 피로도가 높습니다.

| 문제 | 현재 상태 | CLI Tutor 솔루션 |
| :--- | :--- | :--- |
| 진입 장벽 | CLI 환경의 시각적 압박과 어려운 명령어 | TUI 분할 화면으로 시각적 안정감 및 가이드 제공 |
| 콘텍스트 스위칭 | 터미널 에러 복사 -> 웹 브라우저 검색 | 터미널 내에서 즉각적으로 에러 원인 분석 (Explanation Panel) |
| 비용 부담 | 고가의 AI 코딩 어시스턴트 도입 필요 | Groq 기반 무료/초고속 추론 제공, 경량화 |
| 파편화된 학습 | 문서를 읽고 따라하는 수동적 학습 | 목표 달성형 시나리오 (Agent Panel) 단계별 직접 실행 |

## 3. 핵심 시스템 아키텍처 (Core Architecture)

샘플 프로토타입 구조를 기반으로 확장 가능한 아키텍처 규격을 정의합니다.

1. **환경 감지 유닛 (EnvInfo)**
   - OS(Windows/Linux/MacOS), 아키텍처(x86_64, ARM), 특정 환경(WSL) 자동 감지하여 OS에 맞는 프롬프트 최적화.
2. **설정 및 환경 유닛 (ConfigManager & SetupWizard)**
   - 초기 진입 시 진입 장벽을 낮추는 콘솔 마법사.
   - 로컬 디렉토리(`~/.cli-tutor/` 등)에 안전한 JSON 포맷 설정 저장 및 상태 관리.
3. **LLM 라우팅 유닛 (LLMClient)**
   - **Groq (기본):** 무료, 초고속, LLaMA 계열 활용 극대화.
   - **Perplexity:** 최신 기술 트렌드나 특정 도구 메뉴얼 검색 필요 시.
   - **Gemini:** 특정 목적 혹은 한국어 특화 답변 필요 시 Fallback용.
4. **TUI 렌더링 유닛 (Textual App)**
   - 좌측: Sessions Panel (작업 이력 관리)
   - 중앙: Terminal Panel (명령어 입력 및 실행기)
   - 우석 상단: Explanation Panel (결과 해설/디버깅)
   - 우측 하단: Agent Panel (시나리오 마스터/미션 제공)

## 4. 작동 흐름 (UX Flow)

```mermaid
graph TD
    A[프로그램 실행] --> B{설정(API) 존재?}
    B -- No --> C[Setup Wizard 실행]
    C --> D[Provider 선택 및 API Key 저장]
    D --> E
    B -- Yes --> E[TUI 메인 인터페이스 로드]
    E --> F[목표/명령어 입력 대기]
    F -->|목표 입력| G[Agent: 시나리오 단계별 생성]
    F -->|명령어 실행| H[OS Shell 통과 후 출력값 확보]
    H --> I[LLM: 출력값 분석 및 Explanation 업데이트]
    G --> F
    I --> F
```

## 5. 진행 로드맵 (Roadmap)

```
[Phase 1] 초기 아이디어 정립 및 프로토타입 분석 (현재)
  ├── 프로토타입 기능 분해 및 역설계
  ├── 프로젝트 철학, 구조, 규칙 정의 문서화
  └── 제너럴 컨셉으로의 명칭 및 확장 방향 확정

[Phase 2] 시스템 정제 및 아키텍처 세분화 (01_Expansion / 02_Refinement)
  ├── UX/UI (Textual Layout) 상세 디자인 및 오류 대안 수립
  ├── Multi-LLM 프롬프트 엔지니어링 템플릿화
  └── 터미널 PTY 세션 연동의 기술적 한계 및 해결방안 모색

[Phase 3] 정규 버전 (v1.0) 개발 및 런칭
  ├── CLI 패키지화 (pip install cli-tutor)
  ├── 오픈소스 커뮤니티 배포 유도
  └── 플러그인 생태계 도입 (Docker tutor, Git tutor 특화 팩 등)
```

---
> [!TIP]
> 본 개요서는 개발 진행 상황에 따라 업데이트됩니다. 세부 기능 확장 아이디어는 `01_Expansion` 폴더 하위 카드에 기록합니다.

## 6. PPSCI 관리 체계 (Hierarchy)

| 레벨 | 구분 | 요소 | 설명 |
| :--- | :--- | :--- | :--- |
| **L1** | Program | `Program/01_Philosophy.md` | 전역 철학 준수 |
| **L2** | Project | `05_CLI_Tutor/` | CLI Tutor 프로젝트 유닛 |
| **L3** | System | `01_Expansion/`, `02_Refinement/` | 아이디어 확장 및 정제 |
| **L4** | Category | 카드별 분류 (철학, 기술, UX, 배포전략) | 모듈 단위 관리 |
| **L5** | Item | `entries/` | 설계 문서, 코드 스니펫, 프로토타입 |

## 7. 실행 프로시저 (Execution Procedure)

본 프로젝트의 EP는 상위 철학의 [이해] → [단순화] → [시스템화] 원칙을 다음과 같이 구체화합니다.

1. **이해**: 샘플 프로토타입 코드를 철저히 분석하여 의도와 구조를 파악한다.
2. **단순화**: 파악한 구조를 철학(Philosophy) 및 확장 카드(Expansion Cards)로 분해하여 문서화한다.
3. **시스템화**: 정제(Refinement) 단계를 거쳐 구현 가능한 기술 명세로 전환하고, 실제 코드를 구축한다.

