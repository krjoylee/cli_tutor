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
        
        try:
            # PTY 연결이 아닌 단순 서브프로세스 캡처 방식 (v1.0 스펙)
            # 향후 대화형 명령어(vim, ssh, npm init 등) 지원을 위해 pty/winpty 업그레이드 여지 존재
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            stdout_bytes, stderr_bytes = await process.communicate()
            
            # 종료 대기 추가 (자원 해제 확실히)
            await process.wait()
            
            # 인코딩 처리 (Windows는 cp949/euc-kr, Linux/Mac은 utf-8)
            encoding = "cp949" if is_windows else "utf-8"
            
            try:
                stdout_str = stdout_bytes.decode(encoding, errors='replace')
                stderr_str = stderr_bytes.decode(encoding, errors='replace')
            except Exception:
                # 폴백: utf-8 시도
                stdout_str = stdout_bytes.decode('utf-8', errors='replace')
                stderr_str = stderr_bytes.decode('utf-8', errors='replace')

            # 화면 출력 추가
            if stdout_str:
                self.add_output(stdout_str)
            if stderr_str:
                self.add_output(stderr_str, is_error=True)
                
            exit_code = process.returncode
            
            # CD 명령(디렉토리 이동)에 대한 특수 처리
            if command.strip().startswith("cd ") and exit_code == 0:
                target_dir = command.strip()[3:].strip()
                # 셸 따옴표 제거
                try:
                    target_dir = shlex.split(target_dir)[0]
                except ValueError:
                    pass
                
                try:
                    os.chdir(target_dir)
                    self.add_output(f"현재 디렉토리: {os.getcwd()}", is_error=False)
                except Exception as e:
                    self.add_output(f"cd 내부 처리 에러: {e}", is_error=True)

            return exit_code, stdout_str, stderr_str

        except asyncio.CancelledError:
            # 워커 취소 시 대응
            return -1, "", "작업이 취소되었습니다."
        except ValueError as ve:
            if "closed pipe" in str(ve):
                self.add_output("⚠️ 파이프가 이미 닫혀 있습니다 (OS 버그 우회)", is_error=True)
                return -1, "", str(ve)
            raise
        except Exception as e:
            error_msg = f"실행 중 파이썬 내부 예외 발생: {str(e)}"
            self.add_output(error_msg, is_error=True)
            return -1, "", error_msg

    def clear_history(self):
        """화면 지우기."""
        self.history = []
        self.refresh()
