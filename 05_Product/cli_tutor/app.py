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
        ("ctrl+l", "clear_terminal", "터미널 지우기"),
        ("ctrl+g", "focus_input", "입력창 포커스"),
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

    # ------------------------------------------------------------------
    # 이벤트 핸들러
    # ------------------------------------------------------------------

    @on(Input.Submitted, "#input-bar")
    async def handle_input(self, event: Input.Submitted) -> None:
        """사용자 입력 제출 시 모드 분석 후 적절한 모듈로 전달."""
        value = event.value.strip()
        if not value:
            return

        # 입력창 비우기
        event.input.value = ""

        # 1. 목표 모드 (/goal 또는 /g 로 시작)
        if value.lower().startswith(("/goal ", "/g ")):
            goal = value.split(" ", 1)[1].strip()
            self._handle_goal_mode(goal)
        
        # 2. 설명 모드 (/explain 또는 /e 로 시작)
        elif value.lower().startswith(("/explain ", "/e ")):
            query = value.split(" ", 1)[1].strip()
            self._handle_explain_mode(query)

        # 3. 일반 명령어 모드
        else:
            self._handle_command_mode(value)

    # ------------------------------------------------------------------
    # 모드별 로직 (비동기 처리)
    # ------------------------------------------------------------------

    @work(exclusive=True)
    async def _handle_command_mode(self, command: str) -> None:
        """명령어를 실행하고 그 결과를 분석합니다."""
        terminal = self.query_one("#terminal", TerminalPanel)
        explanation = self.query_one("#explanation", ExplanationPanel)
        
        # 터미널에서 명령어 실행
        exit_code, stdout, stderr = await terminal.execute_command(command)
        
        # LLM 해설 요청 (로그 수집)
        if self.llm:
            explanation.set_loading()
            
            # 해설 결과 대기 (스트리밍은 v2.0 개선 과제)
            # 여기서는 블로킹 없이 별도 워커로 실행됨
            result = await asyncio.to_thread(
                self.llm.explain_command, 
                command, 
                stdout + stderr, 
                exit_code
            )
            
            is_error = exit_code != 0
            explanation.set_explanation(result or "분석 결과가 없습니다.", is_error=is_error)

    @work(exclusive=True)
    async def _handle_goal_mode(self, goal: str) -> None:
        """사용자의 목표를 받아 단계별 시나리오를 생성합니다."""
        agent = self.query_one("#agent", AgentPanel)
        
        if not self.llm:
            agent.set_scenario("⚠️ LLM 설정이 완료되지 않았습니다.")
            return

        agent.set_loading()
        
        # LLM에게 시나리오 요청
        raw_response = await asyncio.to_thread(
            self.llm.generate_scenario,
            goal,
            self.env_info
        )
        
        if not raw_response:
            agent.set_scenario("❌ 시나리오 생성에 실패했습니다.")
            return

        # JSON 파싱 및 포매팅
        scenario = self.parser.parse(raw_response)
        if scenario:
            formatted = self.parser.format_steps(scenario)
            agent.set_scenario(formatted)
        else:
            # 파싱 실패 시 폴백
            fallback = self.parser.format_raw_fallback(raw_response)
            agent.set_scenario(fallback)

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
