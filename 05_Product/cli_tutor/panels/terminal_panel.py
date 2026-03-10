"""CLI Tutor — 중앙 터미널 패널 (TerminalPanel)

사용자 명령어를 표시하고, 서브프로세스로 명령을 실행합니다.
OS 셸과 통신하여 출력 및 종료 코드를 캡처합니다.
"""

import subprocess
import shlex
import os
import asyncio
from typing import Tuple

from rich.panel import Panel
from rich.text import Text
from rich.ansi import AnsiDecoder
from textual.widgets import Static
from ..logger import CLILogger


class TerminalPanel(Static):
    """실제 명령어가 실행되고 출력되는 메인 터미널 영역."""

    DEFAULT_CSS = """
    TerminalPanel {
        height: 100%;
        border: round green;
        padding: 0 1;
        overflow-y: scroll;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
        self._decoder = AnsiDecoder()
        self.target_shell = "cmd" if os.name == 'nt' else "sh"

    def render(self):
        """Rich Panel 형태로 히스토리 렌더링."""
        if not self.history:
            return Panel(
                Text(">>> 입력을 기다리는 중...\n(아래 입력창에 명령어를 타이핑하세요)", style="dim"),
                title="💻 메인 터미널",
                border_style="green"
            )

        # ANSI 코드가 들어있을 수 있으므로 Rich Text로 변환
        content = Text()
        # 최근 100줄만 렌더링하도록 잘라냄
        recent_history = self.history[-100:]
        
        for line in recent_history:
            if isinstance(line, str):
                # 단순 문자열
                content.append(line + "\n")
            elif isinstance(line, Text):
                # 이미 Rich 포맷팅된 텍스트
                content.append(line)
                content.append("\n")

        return Panel(
            content,
            title="💻 메인 터미널",
            border_style="green"
        )

    def add_command_echo(self, command: str, pwd: str = ""):
        """입력한 명령어를 터미널 화면에 에코."""
        prompt = f"[{pwd}]$ " if pwd else "$ "
        formatted = Text.assemble((prompt, "bold bright_blue"), (command, "bold white"))
        self.history.append(formatted)
        self.refresh()
        self.scroll_end(animate=False)

    def add_output(self, text: str, is_error: bool = False):
        """명령어 실행 결과(표준출력/에러)를 화면에 추가."""
        if not text.strip():
            return
            
        style = "red" if is_error else "default"
        for line in text.splitlines():
            self.history.append(Text(line, style=style))
            
        self.refresh()
        self.scroll_end(animate=False)

    async def execute_command(self, command: str) -> Tuple[int, str, str]:
        """OS 셸에서 명령어 실행 및 입출력 캡처 (비동기).
        
        Returns:
            Tuple[int, str, str]: (exit_code, stdout, stderr)
        """
        cwd = os.getcwd()
        self.add_command_echo(command, cwd)
        
        # 윈도우 환경과 POSIX 환경에서의 실행 처리 분기
        is_windows = os.name == 'nt'
        
        # 실제 실행될 명령어 구성
        full_command = command
        if is_windows and self.target_shell in ["powershell", "pwsh"]:
            # 파워쉘로 실행 시 Command 인자로 전달
            full_command = f"{self.target_shell} -NoProfile -Command \"{command}\""
        
        # 대화형 셸 진입 방지 로직 (단순 진입 시도 차단)
        interactive_cmds = ["powershell", "pwsh", "cmd", "bash", "zsh", "python", "node", "wsl"]
        if command.strip().lower() in interactive_cmds:
            msg = f"⚠️ '{command}'와 같은 대화형 셸/입력 모드는 현재 미지원입니다.\n원하는 셸을 쓰려면 '/shell {command}'를 입력한 뒤 인자를 포함해 사용하세요 (예: wsl --list)"
            self.add_output(msg, is_error=True)
            return -1, "", msg

        process = None
        try:
            CLILogger.debug(f"Subprocess start: {full_command} (via {self.target_shell})")
            process = await asyncio.create_subprocess_shell(
                full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            CLILogger.debug(f"Process PID: {process.pid}")
            stdout_bytes, stderr_bytes = await process.communicate()
            
            # 종료 대기 (자명한 리소스 해제)
            await process.wait()
            CLILogger.debug(f"Subprocess terminated (ExitCode: {process.returncode})")
            
            # 인코딩 처리 (Windows WSL 출력 등 UTF-16LE 대응)
            def smart_decode(data: bytes) -> str:
                if not data: return ""
                for enc in ["utf-8", "cp949", "utf-16"]:
                    try:
                        # 널 바이트(\x00)가 섞인 경우(UTF-16을 CP949로 읽었을 때 등)를 위해 체크
                        decoded = data.decode(enc)
                        if "\x00" not in decoded or enc == "utf-16":
                            return decoded
                    except:
                        continue
                return data.decode("cp949", errors="replace")

            stdout_str = smart_decode(stdout_bytes)
            stderr_str = smart_decode(stderr_bytes)

            # 화면 출력 추가
            if stdout_str:
                self.add_output(stdout_str)
            if stderr_str:
                self.add_output(stderr_str, is_error=True)
                
            exit_code = process.returncode
            
            # CD 명령 처리
            if command.strip().startswith("cd ") and exit_code == 0:
                self._handle_cd(command)

            return exit_code, stdout_str, stderr_str

        except asyncio.CancelledError:
            print(f"[DEBUG] 명령어 실행 워커가 취소되었습니다.")
            if process and process.returncode is None:
                try:
                    process.kill()
                    print("[DEBUG] 하위 프로세스 강제 종료(kill) 수행")
                except Exception as ex:
                    print(f"[DEBUG] 프로세스 종료 중 오류: {ex}")
            raise  # @work 핸들러를 위해 상위로 전파
        except Exception as e:
            error_msg = f"실행 중 예외 발생: {str(e)}"
            print(f"[DEBUG] {error_msg}")
            self.add_output(error_msg, is_error=True)
            return -1, "", error_msg
        finally:
            # 안전한 자원 해제 확인
            if process and process.returncode is None:
                try:
                    process.terminate()
                except:
                    pass

    def _handle_cd(self, command: str):
        """디렉토리 이동 처리 내부 로직."""
        target_dir = command.strip()[3:].strip()
        try:
            target_dir = shlex.split(target_dir)[0]
            os.chdir(target_dir)
            self.add_output(f"현재 디렉토리: {os.getcwd()}", is_error=False)
        except Exception as e:
            self.add_output(f"cd 처리 에러: {e}", is_error=True)

    def clear_history(self):
        """화면 지우기."""
        self.history = []
        self.refresh()
