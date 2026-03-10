"""CLI Tutor — 초기 설정 마법사 (SetupWizard)

최초 실행 시 Rich Console 기반의 대화형 인터페이스로
LLM Provider 선택 및 API Key 입력을 안내합니다.
"""

import sys

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .env_info import EnvInfo
from .config_manager import ConfigManager


class SetupWizard:
    """대화형 초기 설정 마법사."""

    def __init__(self, console: Console, env_info: EnvInfo, config: ConfigManager):
        self.console = console
        self.env = env_info
        self.config = config

    # ------------------------------------------------------------------
    # 메인 실행
    # ------------------------------------------------------------------

    def run(self) -> bool:
        """Setup 마법사 실행. 성공하면 True 반환."""
        self.console.clear()
        self._show_banner()
        self._show_env_info()
        self._select_provider()
        self._show_summary()
        return True

    # ------------------------------------------------------------------
    # 1. 배너
    # ------------------------------------------------------------------

    def _show_banner(self):
        banner = Text()
        banner.append("🎯 CLI Tutor v1.0 — 초기 설정\n", style="bold cyan")
        banner.append("내 터미널 속의 마스터를 깨워봅시다!\n", style="dim")
        self.console.print(Panel(banner, border_style="cyan", padding=(1, 2)))
        self.console.print()

    # ------------------------------------------------------------------
    # 2. 환경 정보 표시
    # ------------------------------------------------------------------

    def _show_env_info(self):
        table = Table(title="🖥️  시스템 환경 감지 결과", border_style="blue")
        table.add_column("항목", style="cyan", width=14)
        table.add_column("값", style="green")

        table.add_row("운영체제", self.env.os_type.upper())
        table.add_row("아키텍처", self.env.arch)
        table.add_row("상세 정보", self.env.detail)
        if self.env.is_wsl:
            table.add_row("WSL", "✅ Windows Subsystem for Linux")

        self.console.print(table)
        self.console.print()

    # ------------------------------------------------------------------
    # 3. LLM Provider 선택
    # ------------------------------------------------------------------

    def _select_provider(self):
        self.console.print("[bold yellow]📡 사용할 LLM 제공자를 선택하세요[/bold yellow]\n")
        self.console.print("  1) [bold cyan]Groq[/bold cyan]       ⭐ 기본 추천 — 빠르고 무료")
        self.console.print("     모델: openai/gpt-oss-120b | RPM 30 | 일 14,400 요청")
        self.console.print("  2) [bold cyan]Perplexity[/bold cyan] — 웹 검색 기반 최신 정보")
        self.console.print("     검색 통합 | 스트리밍 지원")
        self.console.print("  3) [bold cyan]Gemini[/bold cyan]     — 한국어 특화, 높은 품질")
        self.console.print("     모델: gemini-2.0-flash | 일 250 요청\n")

        choice = input("  선택 (기본: 1) > ").strip() or "1"

        if choice == "2":
            self._setup_perplexity()
        elif choice == "3":
            self._setup_gemini()
        else:
            self._setup_groq()

    # ------------------------------------------------------------------
    # Provider별 설정
    # ------------------------------------------------------------------

    def _setup_groq(self):
        self.console.print("\n[bold cyan]🔑 Groq API 키 설정[/bold cyan]\n")
        self.console.print("  1. https://console.groq.com 에 접속")
        self.console.print("  2. 로그인/가입 → 'API Keys' 메뉴")
        self.console.print("  3. 'Create New API Key' 클릭")
        self.console.print("  4. 생성된 키를 복사 → 아래에 붙여넣기\n")

        api_key = input("  Groq API Key > ").strip()
        if not api_key:
            self.console.print("[red]  ❌ API 키가 입력되지 않았습니다. 종료합니다.[/red]")
            sys.exit(1)

        self.config.set("llm_provider", "groq")
        self.config.set("llm_model", "openai/gpt-oss-120b")
        self.config.set("groq_api_key", api_key)
        self.console.print("[green]  ✅ Groq API 키 저장 완료![/green]")

    def _setup_perplexity(self):
        self.console.print("\n[bold cyan]🔑 Perplexity API 키 설정[/bold cyan]\n")
        self.console.print("  1. https://www.perplexity.ai 에 접속")
        self.console.print("  2. 계정 생성/로그인")
        self.console.print("  3. Settings → API 섹션에서 API 키 생성")
        self.console.print("  4. 생성된 키를 복사 → 아래에 붙여넣기\n")

        api_key = input("  Perplexity API Key > ").strip()
        if not api_key:
            self.console.print("[red]  ❌ API 키가 입력되지 않았습니다. 종료합니다.[/red]")
            sys.exit(1)

        self.config.set("llm_provider", "perplexity")
        self.config.set("llm_model", "sonar-small-online")
        self.config.set("perplexity_api_key", api_key)
        self.console.print("[green]  ✅ Perplexity API 키 저장 완료![/green]")

    def _setup_gemini(self):
        self.console.print("\n[bold cyan]🔑 Google Gemini API 키 설정[/bold cyan]\n")
        self.console.print("  1. https://aistudio.google.com 에 접속")
        self.console.print("  2. Google 계정으로 로그인")
        self.console.print("  3. 'Get API key' → 'Create API key in new project'")
        self.console.print("  4. 생성된 키를 복사 → 아래에 붙여넣기\n")

        api_key = input("  Gemini API Key > ").strip()
        if not api_key:
            self.console.print("[red]  ❌ API 키가 입력되지 않았습니다. 종료합니다.[/red]")
            sys.exit(1)

        self.config.set("llm_provider", "gemini")
        self.config.set("llm_model", "gemini-2.0-flash")
        self.config.set("gemini_api_key", api_key)
        self.console.print("[green]  ✅ Gemini API 키 저장 완료![/green]")

    # ------------------------------------------------------------------
    # 4. 요약
    # ------------------------------------------------------------------

    def _show_summary(self):
        self.console.print()
        table = Table(title="✅ 설정 완료 요약", border_style="green")
        table.add_column("항목", style="cyan", width=14)
        table.add_column("값", style="green")

        table.add_row("시스템", self.env.detail)
        table.add_row("LLM 제공자", self.config.get("llm_provider", "N/A").upper())
        table.add_row("모델", self.config.get_model())
        table.add_row("설정 파일", str(self.config.CONFIG_FILE))

        self.console.print(table)
        self.console.print("\n[bold cyan]  설정이 완료되었습니다! 프로그램을 다시 실행해 주세요.[/bold cyan]\n")
