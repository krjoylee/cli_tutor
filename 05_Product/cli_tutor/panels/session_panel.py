"""CLI Tutor — 좌측 세션 패널 (SessionPanel)

작업 세션 목록을 표시하고, 세션 간 전환을 지원합니다.
"""

from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text


class SessionPanel(Static):
    """좌측 세션 목록 패널."""

    DEFAULT_CSS = """
    SessionPanel {
        width: 18;
        height: 100%;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessions = [
            {"id": 1, "name": "기본 세션", "active": True},
        ]
        self.active_index = 0

    def render(self):
        lines = Text()

        for i, session in enumerate(self.sessions):
            marker = "▶" if session["active"] else " "
            style = "bold cyan" if session["active"] else "dim"
            lines.append(f" {marker} [{session['id']}] ", style=style)
            lines.append(f"{session['name']}\n", style=style)

        lines.append("\n")
        lines.append(" [+ 새 세션]\n", style="dim green")

        return Panel(
            lines,
            title="📋 세션",
            border_style="cyan",
            padding=(1, 0),
        )

    def add_session(self, name: str):
        """새 세션 추가."""
        new_id = len(self.sessions) + 1
        # 기존 세션 비활성화
        for s in self.sessions:
            s["active"] = False
        self.sessions.append({"id": new_id, "name": name, "active": True})
        self.active_index = len(self.sessions) - 1
        self.refresh()

    def get_active_session(self) -> dict:
        """현재 활성 세션 반환."""
        for s in self.sessions:
            if s["active"]:
                return s
        return self.sessions[0] if self.sessions else {}
