"""CLI Tutor — 시나리오 파서 (ScenarioParser)

LLM이 생성한 JSON 텍스트를 파싱하여 구조화된 시나리오 데이터로 변환하고,
TUI 패널에 표시할 포매팅된 문자열을 생성합니다.
"""

import json
import re
from typing import Optional


class ScenarioParser:
    """LLM 시나리오 응답 파서 및 포매터."""

    @staticmethod
    def parse(raw_text: str) -> Optional[dict]:
        """LLM 응답 텍스트에서 JSON 시나리오를 추출.

        Returns:
            파싱된 시나리오 dict 또는 None (파싱 실패 시)
        """
        if not raw_text:
            return None

        # 1차: 직접 JSON 파싱 시도
        try:
            data = json.loads(raw_text.strip())
            if ScenarioParser._validate(data):
                return data
        except json.JSONDecodeError:
            pass

        # 2차: 마크다운 코드블록 내 JSON 추출 시도
        json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", raw_text, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(1).strip())
                if ScenarioParser._validate(data):
                    return data
            except json.JSONDecodeError:
                pass

        # 3차: 중괄호 범위 추출 시도
        brace_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if brace_match:
            try:
                data = json.loads(brace_match.group(0))
                if ScenarioParser._validate(data):
                    return data
            except json.JSONDecodeError:
                pass

        return None

    @staticmethod
    def _validate(data: dict) -> bool:
        """시나리오 JSON 스키마 최소 검증."""
        if not isinstance(data, dict):
            return False
        if "steps" not in data:
            return False
        if not isinstance(data["steps"], list) or len(data["steps"]) == 0:
            return False
        # 각 step에 최소 command 또는 explanation 존재
        for step in data["steps"]:
            if not isinstance(step, dict):
                return False
            if "command" not in step and "explanation" not in step:
                return False
        return True

    @staticmethod
    def format_steps(scenario: dict) -> str:
        """시나리오를 TUI 표시용 문자열로 포매팅.

        Example output:
            🎯 목표: Git 초기 설정
            ──────────────────
            [1] Homebrew 확인
                $ brew --version
                → Homebrew가 설치되어 있는지 확인합니다.

            [2] nvm 설치
                $ brew install nvm
                → Node 버전 관리자를 설치합니다.
        """
        lines = []
        goal = scenario.get("goal", "미정")
        lines.append(f"🎯 목표: {goal}")
        lines.append("─" * 30)

        for step in scenario.get("steps", []):
            idx = step.get("index", "?")
            title = step.get("title", "")
            command = step.get("command", "")
            explanation = step.get("explanation", "")
            caution = step.get("caution", "")

            lines.append(f"\n[{idx}] {title}")
            if command:
                lines.append(f"    $ {command}")
            if explanation:
                lines.append(f"    → {explanation}")
            if caution:
                lines.append(f"    ⚠️  {caution}")

        return "\n".join(lines)

    @staticmethod
    def format_raw_fallback(raw_text: str) -> str:
        """JSON 파싱 실패 시 원본 텍스트를 그대로 표시하기 위한 폴백."""
        return f"📝 (JSON 파싱 실패 — 원본 표시)\n{'─' * 30}\n{raw_text}"
