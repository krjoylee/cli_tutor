"""CLI Tutor — 우측 상단 해설 패널 (ExplanationPanel)

가운데 메뉴에서 실행된 명령어의 출력을 LLM이 분석한
'명령어 설명 및 에러 해설'을 표시합니다.
"""

from rich.panel import Panel
from textual.widgets import Static
from rich.console import RenderableType
from rich.markdown import Markdown


class ExplanationPanel(Static):
    """방금 실행한 명령어의 해설 영역."""

    DEFAULT_CSS = """
    ExplanationPanel {
        height: 1fr;
        border: round yellow;
        padding: 0 1;
        overflow-y: auto;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.explanation_content: RenderableType = "[dim]아직 실행된 명령어가 없습니다.[/dim]"
        self.current_status_style = "yellow"

    def render(self) -> Panel:
        return Panel(
            self.explanation_content,
            title="💡 명령어 해설",
            border_style=self.current_status_style
        )

    def set_explanation(self, text: str, is_error: bool = False):
        """해설 텍스트 갱신 (마크다운 렌더링)."""
        self.current_status_style = "red" if is_error else "yellow"
        
        # Markdown 위젯이 아닌 Rich Markdown 객체로 렌더링
        self.explanation_content = Markdown(text)
        
        self.refresh()
        self.scroll_home(animate=False)

    def set_loading(self):
        """로딩 인디케이터 표시."""
        self.current_status_style = "blue"
        self.explanation_content = "⏳ [dim cyan]결과를 분석 중입니다...[/dim cyan]"
        self.refresh()
