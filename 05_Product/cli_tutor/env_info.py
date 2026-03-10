"""CLI Tutor — 환경 감지 유닛 (EnvInfo)

운영체제, CPU 아키텍처, WSL 여부를 자동 감지하여
LLM 프롬프트에 환경 컨텍스트를 제공합니다.
"""

import platform
from dataclasses import dataclass


@dataclass
class EnvInfo:
    """시스템 환경 정보를 감지하고 보관하는 데이터 클래스."""

    os_type: str = ""
    arch: str = ""
    detail: str = ""
    is_wsl: bool = False

    def __post_init__(self):
        self.is_wsl = self._check_wsl()
        self.os_type = self._detect_os()
        self.arch = self._detect_arch()
        self.detail = f"{self.os_type}-{self.arch}"

    # ------------------------------------------------------------------
    # 내부 감지 메서드
    # ------------------------------------------------------------------

    def _detect_os(self) -> str:
        """운영체제 타입 감지 (windows / macos / linux / wsl / unknown)."""
        system = platform.system()
        if system == "Windows":
            return "windows"
        elif system == "Darwin":
            return "macos"
        elif system == "Linux":
            return "wsl" if self.is_wsl else "linux"
        return "unknown"

    def _detect_arch(self) -> str:
        """CPU 아키텍처 감지 (x86_64 / arm64 / 기타)."""
        arch = platform.machine().lower()
        if arch in ("x86_64", "amd64"):
            return "x86_64"
        elif arch in ("arm64", "aarch64"):
            return "arm64"
        return arch

    def _check_wsl(self) -> bool:
        """WSL(Windows Subsystem for Linux) 환경 여부 판별."""
        if platform.system() != "Linux":
            return False
        try:
            with open("/proc/version", "r") as f:
                content = f.read()
                return "WSL" in content or "Microsoft" in content
        except (FileNotFoundError, PermissionError):
            return False

    # ------------------------------------------------------------------
    # 공개 API
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """설정 저장/LLM 컨텍스트용 딕셔너리 변환."""
        return {
            "os_type": self.os_type,
            "arch": self.arch,
            "detail": self.detail,
            "is_wsl": self.is_wsl,
        }

    def to_prompt_context(self) -> str:
        """LLM 시스템 프롬프트에 삽입할 환경 정보 문자열."""
        lines = [
            f"- OS: {self.os_type}",
            f"- 아키텍처: {self.arch}",
            f"- 상세: {self.detail}",
        ]
        if self.is_wsl:
            lines.append("- WSL 환경: 예 (Windows Subsystem for Linux)")
        return "\n".join(lines)

    def __str__(self) -> str:
        wsl_tag = " (WSL)" if self.is_wsl else ""
        return f"OS: {self.os_type}{wsl_tag} | Arch: {self.arch}"
