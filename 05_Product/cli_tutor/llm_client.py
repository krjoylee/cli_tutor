"""CLI Tutor — Multi-LLM 추상 클라이언트 (LLMClient)

Groq / Perplexity / Gemini를 Provider 패턴으로 추상화하여
단일 인터페이스로 시나리오 생성 및 명령 해설을 수행합니다.
"""

import json
from typing import Optional

from .env_info import EnvInfo


class LLMClient:
    """다중 LLM Provider 클라이언트."""

    def __init__(self, provider: str, api_key: str, model: str):
        self.provider = provider
        self.api_key = api_key
        self.model = model

    # ------------------------------------------------------------------
    # 1. 시나리오 생성
    # ------------------------------------------------------------------

    def generate_scenario(self, goal: str, env_info: EnvInfo) -> Optional[str]:
        """사용자 목표에 대한 단계별 시나리오 생성 (JSON 형식 요청)."""
        system_prompt = self._build_scenario_prompt(env_info)
        return self._call_llm(system_prompt, goal)

    def _build_scenario_prompt(self, env_info: EnvInfo) -> str:
        return f"""당신은 터미널/CLI 명령어를 가르치는 훌륭한 한국어 튜터입니다.

사용자의 환경:
{env_info.to_prompt_context()}

사용자가 달성하고 싶은 목표를 받으면, 아래 JSON 형식으로 단계별 시나리오를 생성하세요:

{{
    "goal": "사용자의 목표 요약",
    "steps": [
        {{
            "index": 1,
            "title": "단계 제목",
            "command": "실행할 셸 명령어",
            "explanation": "이 명령어가 무엇을 하는지 간단 설명",
            "caution": "주의사항 (선택)"
        }}
    ]
}}

규칙:
- 최소 2단계, 최대 5단계로 구성하세요.
- 명령어는 {env_info.os_type} 환경에서 실행 가능해야 합니다.
- 한글로 설명하세요.
- 반드시 JSON만 출력하세요 (마크다운 코드블록 없이)."""

    # ------------------------------------------------------------------
    # 2. 명령어 해설
    # ------------------------------------------------------------------

    def explain_command(
        self, command: str, output: str, exit_code: int
    ) -> Optional[str]:
        """실행된 명령어와 결과에 대한 해설 생성."""
        prompt = f"""다음 명령어의 실행 결과를 분석하고 해설해 주세요.

명령어: {command}
종료 코드: {exit_code}
출력 (최대 500자):
{output[:500]}

아래 형식으로 답변해 주세요:
1. **이 명령어의 역할**: (한 줄 요약)
2. **실행 결과**: (성공/실패 판정과 간단 해석)
3. **원인 분석**: (실패 시 가능한 원인)
4. **다음 제안**: (이어서 실행할 명령어 1~2개)

한글로 답변하세요."""

        return self._call_llm("", prompt)

    # ------------------------------------------------------------------
    # 3. 자유 질의
    # ------------------------------------------------------------------

    def ask(self, question: str, env_info: EnvInfo) -> Optional[str]:
        """자유로운 CLI 관련 질문에 대한 답변 생성."""
        system_prompt = f"""당신은 터미널/CLI 전문 튜터입니다.
사용자 환경: {env_info.detail}
한글로 친절하고 간결하게 답변하세요."""
        return self._call_llm(system_prompt, question)

    # ------------------------------------------------------------------
    # Provider별 호출 구현
    # ------------------------------------------------------------------

    def _call_llm(self, system_prompt: str, user_message: str) -> Optional[str]:
        """Provider에 따라 적절한 LLM API를 호출."""
        try:
            if self.provider == "groq":
                return self._call_groq(system_prompt, user_message)
            elif self.provider == "perplexity":
                return self._call_perplexity(system_prompt, user_message)
            elif self.provider == "gemini":
                return self._call_gemini(system_prompt, user_message)
            else:
                return f"❌ 알 수 없는 LLM Provider: {self.provider}"
        except Exception as e:
            return f"❌ LLM 호출 실패: {e}"

    def _call_groq(self, system_prompt: str, user_message: str) -> Optional[str]:
        """Groq API 호출."""
        from groq import Groq

        client = Groq(api_key=self.api_key)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        completion = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_completion_tokens=2048,
            stream=False,
        )
        return completion.choices[0].message.content

    def _call_perplexity(self, system_prompt: str, user_message: str) -> Optional[str]:
        """Perplexity API 호출 (httpx 직접 사용)."""
        import httpx

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.3,
        }
        response = httpx.post(
            "https://api.perplexity.ai/chat/completions",
            json=payload,
            headers=headers,
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"❌ Perplexity API 오류: {response.status_code} - {response.text[:200]}"

    def _call_gemini(self, system_prompt: str, user_message: str) -> Optional[str]:
        """Google Gemini API 호출."""
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model_kwargs = {}
        if system_prompt:
            model_kwargs["system_instruction"] = system_prompt

        model = genai.GenerativeModel(self.model, **model_kwargs)
        response = model.generate_content(user_message)
        return response.text
