#!/usr/bin/env python3
"""
Gemini Tutor CLI - Windows 11 PowerShell 5.1 호환 프로토타입
터미널 안에 상주하는 Gemini 기반 튜터 에이전트
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import re

# 외부 라이브러리 (필요시 설치: pip install google-generativeai rich textual)
try:
    import google.generativeai as genai
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from textual.app import ComposeResult, on
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Header, Footer, Static, Input, TextArea
    from textual.app import App
except ImportError as e:
    print(f"❌ 필수 라이브러리 누락: {e}")
    print("설치 명령: pip install google-generativeai rich textual")
    sys.exit(1)


# ============================================================================
# 1. 환경 감지 및 설정 관리
# ============================================================================

class EnvInfo:
    """운영체제/플랫폼 정보"""
    def __init__(self):
        self.os_type = self._detect_os()
        self.arch = self._detect_arch()
        self.detail = f"{self.os_type}-{self.arch}"
        self.is_wsl = self._check_wsl()
    
    def _detect_os(self) -> str:
        """OS 타입 감지"""
        system = platform.system()
        if system == "Windows":
            return "windows"
        elif system == "Darwin":
            return "macos"
        elif system == "Linux":
            if self._check_wsl():
                return "wsl"
            return "linux"
        return "unknown"
    
    def _detect_arch(self) -> str:
        """아키텍처 감지"""
        arch = platform.machine().lower()
        if arch in ["x86_64", "amd64"]:
            return "x86_64"
        elif arch in ["arm64", "aarch64"]:
            return "arm64"
        return arch
    
    def _check_wsl(self) -> bool:
        """WSL 환경 여부"""
        if platform.system() != "Linux":
            return False
        try:
            with open("/proc/version", "r") as f:
                return "WSL" in f.read() or "Microsoft" in f.read()
        except:
            return False
    
    def __str__(self):
        return f"OS: {self.os_type} | Arch: {self.arch} | Detail: {self.detail}"


class ConfigManager:
    """설정 파일 관리"""
    
    CONFIG_DIR = Path.home() / ".g-tutor"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    SESSIONS_DIR = CONFIG_DIR / "sessions"
    
    def __init__(self):
        self.CONFIG_DIR.mkdir(exist_ok=True)
        self.SESSIONS_DIR.mkdir(exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        if self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """설정 파일 저장"""
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get(self, key: str, default=None):
        """설정값 조회"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """설정값 저장"""
        self.config[key] = value
        self.save_config()


# ============================================================================
# 2. Setup 마법사 (CLI 기반)
# ============================================================================

class SetupWizard:
    """초기 설정 마법사"""
    
    def __init__(self, console: Console, env_info: EnvInfo):
        self.console = console
        self.env = env_info
        self.config_manager = ConfigManager()
    
    def run(self):
        """Setup 마법사 실행"""
        self.console.clear()
        self.console.print("[bold cyan]🎯 Gemini Tutor CLI - 초기 설정[/bold cyan]\n")
        
        # 환경 정보 표시
        self._show_env_info()
        
        # LLM 선택
        self._setup_llm()
        
        # 설정 완료
        self._show_summary()
    
    def _show_env_info(self):
        """환경 정보 표시"""
        info_table = Table(title="시스템 정보")
        info_table.add_column("항목", style="cyan")
        info_table.add_column("값", style="green")
        
        info_table.add_row("OS", self.env.os_type.upper())
        info_table.add_row("아키텍처", self.env.arch)
        info_table.add_row("상세정보", self.env.detail)
        if self.env.is_wsl:
            info_table.add_row("WSL", "예 (Windows Subsystem for Linux)")
        
        self.console.print(info_table)
        self.console.print()
    
    def _setup_llm(self):
        """LLM 설정"""
        self.console.print("[bold yellow]📡 LLM 선택[/bold yellow]")
        self.console.print("사용할 LLM 제공자를 선택하세요:\n")
        self.console.print("1) [cyan]Gemini[/cyan] (Google, 무료 티어 지원)")
        self.console.print("2) [cyan]Groq[/cyan] (Llama 등, 무료 티어 지원)\n")
        
        choice = input("선택 (기본: 1) > ").strip() or "1"
        
        if choice == "2":
            self._setup_groq()
        else:
            self._setup_gemini()
    
    def _setup_gemini(self):
        """Gemini API 설정"""
        self.console.print("\n[bold cyan]🔑 Gemini API 키 설정[/bold cyan]\n")
        self.console.print("[yellow]아래 단계를 따르세요:[/yellow]")
        self.console.print("1. 브라우저에서 https://aistudio.google.com 에 접속")
        self.console.print("2. Google 계정으로 로그인")
        self.console.print("3. \"Get API key\" 버튼 클릭해 새 API 키 생성")
        self.console.print("4. 생성된 키를 복사해 아래에 붙여넣기\n")
        
        api_key = input("Gemini API 키를 입력하세요 > ").strip()
        
        if not api_key:
            self.console.print("[red]❌ API 키가 입력되지 않았습니다.[/red]")
            sys.exit(1)
        
        self.config_manager.set("llm_provider", "gemini")
        self.config_manager.set("llm_model", "gemini-2.0-flash")
        self.config_manager.set("gemini_api_key", api_key)
        
        self.console.print("[green]✅ Gemini API 키가 저장되었습니다.[/green]")
    
    def _setup_groq(self):
        """Groq API 설정"""
        self.console.print("\n[bold cyan]🔑 Groq API 키 설정[/bold cyan]\n")
        self.console.print("[yellow]아래 단계를 따르세요:[/yellow]")
        self.console.print("1. 브라우저에서 https://console.groq.com 에 접속")
        self.console.print("2. 계정 생성/로그인")
        self.console.print("3. API Keys 메뉴에서 새 키 생성")
        self.console.print("4. 생성된 키를 복사해 아래에 붙여넣기\n")
        
        api_key = input("Groq API 키를 입력하세요 > ").strip()
        
        if not api_key:
            self.console.print("[red]❌ API 키가 입력되지 않았습니다.[/red]")
            sys.exit(1)
        
        self.config_manager.set("llm_provider", "groq")
        self.config_manager.set("llm_model", "llama-3.1-8b-instant")
        self.config_manager.set("groq_api_key", api_key)
        
        self.console.print("[green]✅ Groq API 키가 저장되었습니다.[/green]")
    
    def _show_summary(self):
        """설정 완료 요약"""
        self.console.print("\n[bold green]✅ 설정이 완료되었습니다![/bold green]\n")
        
        summary_table = Table(title="설정 요약")
        summary_table.add_column("항목", style="cyan")
        summary_table.add_column("값", style="green")
        
        summary_table.add_row("시스템", self.env.detail)
        summary_table.add_row("LLM 제공자", self.config_manager.get("llm_provider", "N/A"))
        summary_table.add_row("모델", self.config_manager.get("llm_model", "N/A"))
        summary_table.add_row("설정 파일", str(ConfigManager.CONFIG_FILE))
        
        self.console.print(summary_table)
        self.console.print("\n[bold cyan]이제 프로그램을 재시작하세요![/bold cyan]")


# ============================================================================
# 3. Gemini API 클라이언트
# ============================================================================

class GeminiClient:
    """Gemini API 호출 클라이언트"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=api_key)
    
    def generate_scenario(self, goal: str, env_info: EnvInfo) -> Optional[str]:
        """목표에 따른 단계별 시나리오 생성"""
        try:
            system_prompt = f"""
당신은 터미널/CLI 명령어를 가르치는 훌륭한 튜터입니다.

사용자의 환경:
- OS: {env_info.os_type}
- 아키텍처: {env_info.arch}
- 상세: {env_info.detail}

사용자가 달성하고 싶은 목표를 받으면, 다음 형식의 JSON으로 단계별 시나리오를 생성하세요:

{{
    "goal": "사용자의 목표",
    "steps": [
        {{
            "index": 1,
            "title": "1단계 제목",
            "command": "실행할 셸 명령어",
            "explanation": "이 명령어가 무엇을 하는지 간단한 설명",
            "caution": "주의사항 (옵션)"
        }},
        {{
            "index": 2,
            "title": "2단계 제목",
            "command": "실행할 셸 명령어",
            "explanation": "이 명령어가 무엇을 하는지 간단한 설명",
            "caution": null
        }}
    ]
}}

- 최소 2단계, 최대 5단계로 구성하세요.
- 명령어는 {env_info.os_type} 환경에서 실행 가능해야 합니다.
- 한글 설명을 사용하세요.
"""
            
            model = genai.GenerativeModel(
                self.model,
                system_instruction=system_prompt
            )
            
            response = model.generate_content(goal)
            
            # JSON 추출 시도
            response_text = response.text
            
            # ```json ... ``` 형식 처리
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 직접 JSON 객체 찾기
                try:
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1
                    json_str = response_text[start:end]
                except:
                    json_str = response_text
            
            return json_str
        
        except Exception as e:
            print(f"[red]❌ Gemini API 호출 실패: {e}[/red]")
            return None
    
    def explain_command(self, command: str, output: str, exit_code: int) -> Optional[str]:
        """명령어 실행 결과 설명"""
        try:
            prompt = f"""
명령어: {command}
종료 코드: {exit_code}
출력 (최대 500자): {output[:500]}

위 명령어와 실행 결과에 대해 간단히 설명해주세요.
- 이 명령이 하는 일
- 실행 결과 해석 (성공/실패 여부)
- 만약 실패했다면 가능한 원인
- 다음에 할 수 있는 명령어 제안 (1~2개)

한글로 답변하세요.
"""
            
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            
            return response.text
        
        except Exception as e:
            return f"설명 생성 실패: {e}"


# ============================================================================
# 4. TUI 애플리케이션 (Textual 기반)
# ============================================================================

class SessionPanel(Static):
    """좌측 세션 패널"""
    
    def render(self):
        sessions = ["[1] default", "[2] project-a", "[+ 새 세션]"]
        return Panel(
            "\n".join(sessions),
            title="세션 목록",
            border_style="cyan"
        )


class TerminalPanel(Static):
    """가운데 터미널 패널"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
    
    def render(self):
        content = "\n".join(self.history[-20:]) if self.history else ""
        return Panel(
            content,
            title="메인 터미널 (입력 창)",
            border_style="green"
        )
    
    def add_output(self, text: str):
        self.history.append(text)
        self.refresh()


class ExplanationPanel(Static):
    """우측 상부 설명 패널"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.explanation_text = ""
    
    def render(self):
        return Panel(
            self.explanation_text or "[grey]대기 중...[/grey]",
            title="방금 실행 명령 설명",
            border_style="yellow"
        )
    
    def set_explanation(self, text: str):
        self.explanation_text = text
        self.refresh()


class AgentPanel(Static):
    """우측 하부 에이전트 패널"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent_text = ""
    
    def render(self):
        return Panel(
            self.agent_text or "[grey]하고 싶은 일을 입력하세요.[/grey]",
            title="에이전트 가이드",
            border_style="magenta"
        )
    
    def set_scenario(self, text: str):
        self.agent_text = text
        self.refresh()


class GeminiTutorApp(App):
    """메인 TUI 애플리케이션"""
    
    BINDINGS = [
        ("q", "quit", "종료"),
        ("c", "clear", "화면 지우기"),
    ]
    
    def __init__(self, config_manager: ConfigManager, env_info: EnvInfo):
        super().__init__()
        self.config_manager = config_manager
        self.env_info = env_info
        self.gemini_client = None
        self._init_llm()
        
        self.terminal_panel = None
        self.explanation_panel = None
        self.agent_panel = None
    
    def _init_llm(self):
        """LLM 클라이언트 초기화"""
        provider = self.config_manager.get("llm_provider", "gemini")
        
        if provider == "gemini":
            api_key = self.config_manager.get("gemini_api_key")
            model = self.config_manager.get("llm_model", "gemini-2.0-flash")
            self.gemini_client = GeminiClient(api_key, model)
    
    def compose(self) -> ComposeResult:
        """UI 구성"""
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(
                Layout(
                    Layout(SessionPanel(), name="left", size=20),
                    Layout(self._create_middle_right(), name="middle_right"),
                    direction="horizontal",
                    name="main"
                ),
                name="body"
            ),
            Layout(name="footer", size=3),
        )
        
        yield layout
    
    def _create_middle_right(self) -> Layout:
        """중앙-우측 레이아웃"""
        layout = Layout()
        layout.split(
            Layout(TerminalPanel(), name="terminal"),
            Layout(
                Layout(ExplanationPanel(), name="explanation"),
                Layout(AgentPanel(), name="agent"),
                direction="vertical"
            ),
            direction="horizontal"
        )
        return layout
    
    def action_quit(self):
        """프로그램 종료"""
        self.exit()
    
    def action_clear(self):
        """화면 지우기"""
        if self.terminal_panel:
            self.terminal_panel.history = []
            self.terminal_panel.refresh()


# ============================================================================
# 5. 메인 프로그램
# ============================================================================

def main():
    """메인 함수"""
    console = Console()
    
    # 환경 정보 수집
    env_info = EnvInfo()
    config_manager = ConfigManager()
    
    # Setup 마법사 확인
    if not config_manager.get("llm_provider"):
        wizard = SetupWizard(console, env_info)
        wizard.run()
        return
    
    # TUI 앱 실행
    try:
        app = GeminiTutorApp(config_manager, env_info)
        app.run()
    except Exception as e:
        console.print(f"[red]❌ 애플리케이션 오류: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
