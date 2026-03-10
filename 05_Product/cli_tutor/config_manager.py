"""CLI Tutor — 설정 관리 유닛 (ConfigManager)

로컬 JSON 파일(~/.cli-tutor/config.json)에 API Key, LLM 설정 등을
영속적으로 저장하고 관리합니다.
"""

import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """JSON 기반 설정 파일 관리자."""

    CONFIG_DIR = Path.home() / ".cli-tutor"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    SESSIONS_DIR = CONFIG_DIR / "sessions"

    # 설정 기본값 스키마
    DEFAULTS = {
        "llm_provider": "",
        "llm_model": "",
        "groq_api_key": "",
        "gemini_api_key": "",
        "perplexity_api_key": "",
        "explanation_level": "beginner",   # beginner / intermediate / advanced
        "safety_mode": "manual",           # manual / semi-auto / auto
        "ui_theme": "dark",
    }

    def __init__(self):
        self._ensure_dirs()
        self.config: dict = self._load_config()

    # ------------------------------------------------------------------
    # 디렉토리 / 파일 관리
    # ------------------------------------------------------------------

    def _ensure_dirs(self):
        """설정 디렉토리와 세션 디렉토리 생성."""
        self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict:
        """설정 파일 로드. 없거나 손상 시 기본값 반환."""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                # 기본값과 병합 (새 키가 추가되어도 호환)
                merged = {**self.DEFAULTS, **saved}
                return merged
            except (json.JSONDecodeError, OSError):
                return dict(self.DEFAULTS)
        return dict(self.DEFAULTS)

    def save_config(self):
        """현재 설정을 JSON 파일로 저장."""
        self._ensure_dirs()
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # 값 접근 API
    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """설정값 조회."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """설정값 저장 (즉시 파일에 기록)."""
        self.config[key] = value
        self.save_config()

    # ------------------------------------------------------------------
    # 유틸리티
    # ------------------------------------------------------------------

    def is_configured(self) -> bool:
        """LLM provider와 API 키가 설정되었는지 확인."""
        provider = self.get("llm_provider", "")
        if not provider:
            return False
        key_map = {
            "groq": "groq_api_key",
            "perplexity": "perplexity_api_key",
            "gemini": "gemini_api_key",
        }
        api_key_field = key_map.get(provider, "")
        return bool(self.get(api_key_field, ""))

    def get_api_key(self) -> Optional[str]:
        """현재 선택된 provider의 API 키 반환."""
        provider = self.get("llm_provider", "")
        key_map = {
            "groq": "groq_api_key",
            "perplexity": "perplexity_api_key",
            "gemini": "gemini_api_key",
        }
        field = key_map.get(provider, "")
        return self.get(field, "") or None

    def get_model(self) -> str:
        """현재 선택된 provider의 모델명 반환."""
        provider = self.get("llm_provider", "")
        model = self.get("llm_model", "")
        if model:
            return model
        # 기본 모델 매핑
        model_defaults = {
            "groq": "openai/gpt-oss-120b",
            "perplexity": "sonar-small-online",
            "gemini": "gemini-2.0-flash",
        }
        return model_defaults.get(provider, "")

    def reset(self):
        """설정 초기화."""
        self.config = dict(self.DEFAULTS)
        self.save_config()

    def __repr__(self) -> str:
        provider = self.get("llm_provider", "N/A")
        return f"<ConfigManager provider={provider} path={self.CONFIG_FILE}>"
