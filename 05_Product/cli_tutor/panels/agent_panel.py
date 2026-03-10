"""CLI Tutor — 우측 하단 에이전트 패널 (AgentPanel)

사용자의 목표를 받아 LLM이 생성한 단계별(Step-by-Step)
시나리오를 렌더링합니다.
"""

from rich.panel import Panel
from textual.widgets import Static
from rich.console import RenderableType
from rich.markdown import Markdown


class AgentPanel(Static):
    """시나리오 가이드 영역."""

    DEFAULT_CSS = """
    AgentPanel {
        height: 1fr;
        border: round magenta;
        padding: 0 1;
        overflow-y: auto;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scenario_content: RenderableType = "[dim]하고 싶은 일을 아래 입력창에서 시작하세요. (목표를 입력)\n예: Git 전역 사용자 이름과 이메일을 설정하고 싶어[/dim]"
        self.current_status_style = "magenta"

    def render(self) -> Panel:
        return Panel(
            self.scenario_content,
            title="🎯 에이전트 가이드",
            border_style=self.current_status_style
        )

    def set_scenario(self, text: str):
        """생성된 시나리오 텍스트(포매팅 완료 상태) 표시."""
        self.current_status_style = "magenta"
        
        # 일반 포매팅 텍스트 그대로 표시
        self.scenario_content = text
        
        self.refresh()
        self.scroll_home(animate=False)

    def set_loading(self):
        """로딩 인디케이터 표시."""
        self.current_status_style = "blue"
        self.scenario_content = "🤖 [dim cyan]최적의 시나리오를 구성 중입니다...[/dim cyan]"
        self.refresh()
