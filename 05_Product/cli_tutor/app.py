"""CLI Tutor — 메인 TUI 애플리케이션 (App)

모든 기반 모듈과 UI 패널을 조립하여 
사용자에게 통합된 CLI 튜터링 경험을 제공합니다.
"""

import sys
import asyncio
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Static
from textual import on, work

from .env_info import EnvInfo
from .config_manager import ConfigManager
from .llm_client import LLMClient
from .scenario_parser import ScenarioParser
from .panels.session_panel import SessionPanel
from .panels.terminal_panel import TerminalPanel
from .panels.explanation_panel import ExplanationPanel
from .panels.agent_panel import AgentPanel


class CLITutorApp(App):
    """CLI Tutor v1.0 메인 TUI 애플리케이션."""

    # 스타일시트 연결
    CSS_PATH = "app.tcss"

    # 키 바인딩
    BINDINGS = [
        ("q", "quit", "종료"),
        ("ctrl+q", "quit", "강제 종료"),
        ("ctrl+l", "clear_terminal", "터미널 지우기"),
        ("ctrl+g", "focus_input", "입력창 포커스"),
        ("ctrl+t", "focus_next", "다음 위젯 (Tab 대용)"),
    ]

    def __init__(self, config: ConfigManager, env_info: EnvInfo):
        super().__init__()
        self.config = config
        self.env_info = env_info
        
        # LLM 클라이언트 초기화 (설정값이 있는 경우)
        self.llm: Optional[LLMClient] = None
        self._init_llm_client()
        
        # 유틸리티 초기화
        self.parser = ScenarioParser()

    def _init_llm_client(self):
        """설정에 따라 LLM 클라이언트를 인스턴스화합니다."""
        if not self.config.is_configured():
            return
            
        provider = self.config.get("llm_provider")
        api_key = self.config.get_api_key()
        model = self.config.get_model()
        
        if provider and api_key:
            self.llm = LLMClient(provider, api_key, model)

    def compose(self) -> ComposeResult:
        """UI 컴포넌트 전체 조립."""
        yield Header(show_clock=True)
        
        # 메인 가로 분할: [세션] | [터미널 | 우측 패널들]
        with Horizontal(id="main-layout"):
            yield SessionPanel(id="sessions")
            
            # 중앙/우측 분할: [터미널] | [우측 수직 패널들]
            yield TerminalPanel(id="terminal")
            
            with Vertical(id="right-pane"):
                yield ExplanationPanel(id="explanation")
                yield AgentPanel(id="agent")
        
        # 하단 입력 바 (고정)
        yield Input(
            placeholder="명령어 입력 (목표는 /goal 또는 /g 로 시작)", 
            id="input-bar"
        )
        
        yield Footer()

    # ------------------------------------------------------------------
    # 액션 핸들러
    # ------------------------------------------------------------------
    
    def action_quit(self) -> None:
        """프로그램 종료."""
        self.exit()

    def action_clear_terminal(self) -> None:
        """터미널 화면 지우기."""
        self.query_one("#terminal", TerminalPanel).clear_history()

    def action_focus_input(self) -> None:
        """입력창에 포커스 주기."""
        self.query_one("#input-bar", Input).focus()
        self.notify("⌨️ 입력창으로 포커스 이동", timeout=2)

    def action_focus_next(self) -> None:
        """Tab 대신 포커스 순환."""
        self.screen.focus_next()
        self.notify("🔄 위젯 전환", timeout=1)

    # ------------------------------------------------------------------
    # 이벤트 핸들러
    # ------------------------------------------------------------------

    @on(Input.Submitted, "#input-bar")
    async def handle_input(self, event: Input.Submitted) -> None:
        """사용자 입력 제출 시 모드 분석 후 적절한 모듈로 전달."""
        # \n 문자가 수동으로 삽입된 경우 제거 (일부 터미널 버그 대응)
        value = event.value.replace("\\n", "").replace("\n", "").strip()
        if not value:
            event.input.value = ""
            return

        # 입력창 비우기
        event.input.value = ""

        # 1. 목표 모드 (/goal 또는 /g 로 시작)
        if value.lower().startswith(("/goal ", "/g ")):
            goal = value.split(" ", 1)[1].strip()
            self.notify(f"🎯 목표 분석 중: {goal[:20]}...", title="Agent")
            self._handle_goal_mode(goal)
        
        # 2. 설명 모드 (/explain 또는 /e 로 시작)
        elif value.lower().startswith(("/explain ", "/e ")):
            query = value.split(" ", 1)[1].strip()
            self.notify(f"❓ 설명 요청 중: {query[:20]}...", title="Explain")
            self._handle_explain_mode(query)

        # 3. 일반 명령어 모드
        else:
            self.notify(f"🚀 명령어 실행: {value[:20]}...", title="Terminal")
            # 새로운 명령어가 시작되면 기존 해설 패널을 즉시 로딩 상태로 변경 (안바뀌는 느낌 방지)
            self.query_one("#explanation", ExplanationPanel).set_loading()
            self._handle_command_mode(value)

    # ------------------------------------------------------------------
    # 모드별 로직 (비동기 처리)
    # ------------------------------------------------------------------

    @work(exclusive=True)
    async def _handle_command_mode(self, command: str) -> None:
        """명령어를 실행하고 그 결과를 분석합니다."""
        terminal = self.query_one("#terminal", TerminalPanel)
        explanation = self.query_one("#explanation", ExplanationPanel)
        
        try:
            # 터미널에서 명령어 실행
            print(f"[DEBUG] [STEP 1] 명령어 실행 시도: {command}")
            exit_code, stdout, stderr = await terminal.execute_command(command)
            print(f"[DEBUG] [STEP 2] 실행 완료 (ExitCode: {exit_code})")
            
            # LLM 해설 요청 (로그 수집)
            if self.llm:
                explanation.set_loading()
                print("[DEBUG] [STEP 3] LLM 해설 생성 시작...")
                
                result = await asyncio.to_thread(
                    self.llm.explain_command, 
                    command, 
                    stdout + stderr, 
                    exit_code
                )
                
                is_error = exit_code != 0
                if result:
                    print(f"[DEBUG] [STEP 4] 해설 생성 성공 (길이: {len(result)})")
                    explanation.set_explanation(result, is_error=is_error)
                    self.notify(f"✅ 해설 완료: {command[:15]}", severity="information")
                else:
                    print("[DEBUG] [STEP 4] 해설 생성 결과 없음")
                    explanation.set_explanation("분석 결과가 없습니다.", is_error=is_error)
                    self.notify("⚠️ 해설 결과가 없습니다.", severity="warning")
            else:
                self.notify("ℹ️ LLM 미설정: 실행만 수행됨", severity="information")
                
        except asyncio.CancelledError:
            print(f"[DEBUG] [CANCEL] 이전 명령어 '{command}' 작업이 새 작업에 의해 취소되었습니다.")
            # 취소 시에는 별도 처리를 하지 않고 종료 (Textual이 새 워커를 시작함)
            raise
        except Exception as e:
            print(f"[DEBUG] [ERROR] 명령어 처리 중 예외: {e}")
            self.notify(f"❌ 에러 발생: {str(e)}", severity="error")

    @work(exclusive=True)
    async def _handle_goal_mode(self, goal: str) -> None:
        """사용자의 목표를 받아 단계별 시나리오를 생성합니다."""
        agent = self.query_one("#agent", AgentPanel)
        
        if not self.llm:
            agent.set_scenario("⚠️ LLM 설정이 완료되지 않았습니다.")
            return

        agent.set_loading()
        print(f"[DEBUG] 시나리오 생성 요청: {goal}")
        
        # LLM에게 시나리오 요청
        try:
            raw_response = await asyncio.to_thread(
                self.llm.generate_scenario,
                goal,
                self.env_info
            )
        except Exception as e:
            print(f"[DEBUG] LLM 호출 중 원인 모를 예외: {e}")
            agent.set_scenario(f"❌ LLM 호출 중 예외: {e}")
            return
        
        if not raw_response:
            print("[DEBUG] 시나리오 응답 데이터 비었음")
            agent.set_scenario("❌ 시나리오 생성에 실패했습니다 (응답 없음).")
            return

        print(f"[DEBUG] 시나리오 원본 수신 (길이: {len(raw_response)})")
        # JSON 파싱 및 포매팅
        scenario = self.parser.parse(raw_response)
        if scenario:
            print(f"[DEBUG] [SUCCESS] 시나리오 가이드 분석/로드 완료 (단계수: {len(scenario.get('steps', []))})")
            formatted = self.parser.format_steps(scenario)
            agent.set_scenario(formatted)
            self.notify(f"✅ 가이드 생성 완료 (목표: {goal[:10]}...)", title="Agent")
        else:
            # 파싱 실패 시 폴백
            print("[DEBUG] [WARNING] JSON 파싱 실패, 텍스트 폴백 모드로 렌더링")
            fallback = self.parser.format_raw_fallback(raw_response)
            agent.set_scenario(fallback)
            self.notify("⚠️ 시나리오 일부 파싱 실패 (텍스트로 표시)", severity="warning")

    @work(exclusive=True)
    async def _handle_explain_mode(self, query: str) -> None:
        """자유 질문에 대해 해설을 제공합니다."""
        explanation = self.query_one("#explanation", ExplanationPanel)
        
        if not self.llm:
            explanation.set_explanation("⚠️ LLM 설정이 필요합니다.")
            return

        explanation.set_loading()
        
        result = await asyncio.to_thread(
            self.llm.ask,
            query,
            self.env_info
        )
        
        explanation.set_explanation(result or "답변을 생성하지 못했습니다.")
