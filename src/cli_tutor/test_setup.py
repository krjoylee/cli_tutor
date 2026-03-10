#!/usr/bin/env python3
"""
Gemini Tutor CLI v2.1 - 테스트 및 Setup 도구
Multi-LLM 통합 (Groq/Perplexity/Gemini)
Windows 11 PowerShell 5.1 호환
"""

import os
import sys
import json
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, List
from importlib import import_module

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# ============================================================================
# 유틸 함수
# ============================================================================

def get_processor_info() -> str:
    """프로세서 정보 조회"""
    try:
        if platform.system() == "Windows":
            import wmi
            computer = wmi.WMI()
            for proc in computer.Win32_Processor():
                return proc.Name
    except:
        pass
    return platform.processor() or "Unknown"


def get_python_path() -> str:
    """Python 실행 경로"""
    return sys.executable


def get_python_version() -> str:
    """Python 버전"""
    return f"{platform.python_implementation()} {platform.python_version()}"


def get_config_dir() -> Path:
    """설정 디렉토리"""
    config_dir = Path.home() / ".g-tutor"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """설정 파일 경로"""
    return get_config_dir() / "config.json"


def load_config() -> Dict[str, Any]:
    """설정 파일 로드"""
    config_file = get_config_file()
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_config(config: Dict[str, Any]):
    """설정 파일 저장"""
    config_file = get_config_file()
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


# ============================================================================
# Main Setup Tool
# ============================================================================

class GeminiTutorSetupTool:
    """Gemini Tutor CLI Setup 도구"""
    
    def __init__(self):
        self.console = Console()
        self.config = load_config()
    
    def run(self):
        """Setup 도구 실행"""
        self.console.clear()
        
        # 헤더
        self.console.print(Panel(
            "[bold cyan]Gemini Tutor CLI v2.1 - 테스트 및 Setup 도구[/bold cyan]\n"
            "[yellow]Multi-LLM 통합 (Groq/Perplexity/Gemini)[/yellow]",
            border_style="cyan"
        ))
        
        # 시스템 정보
        self._show_system_info()
        
        # 의존성 확인
        self._check_dependencies()
        
        # 설정 확인
        self._check_saved_config()
        
        # API 테스트
        self._test_apis()
        
        # 추가 기능 테스트
        self._test_additional_features()
        
        # 완료
        self._show_completion()
    
    def _show_system_info(self):
        """시스템 정보 출력"""
        self.console.print("\n" + "="*60)
        self.console.print("📊 시스템 환경 정보")
        self.console.print("="*60 + "\n")
        
        info_table = Table(show_header=False, box=None)
        info_table.add_column("항목", style="cyan")
        info_table.add_column("값", style="green")
        
        info_table.add_row("[INFO] OS", platform.system())
        info_table.add_row("[INFO] 아키텍처", platform.machine())
        info_table.add_row("[INFO] 프로세서", get_processor_info())
        info_table.add_row("[INFO] Python", get_python_version())
        info_table.add_row("[INFO] Python 경로", get_python_path())
        info_table.add_row("[INFO] 설정 디렉토리", str(get_config_dir()))
        
        self.console.print(info_table)
    
    def _check_dependencies(self):
        """의존성 확인"""
        self.console.print("\n" + "="*60)
        self.console.print("📦 의존성 확인")
        self.console.print("="*60 + "\n")
        
        modules = {
            "groq": "Groq API 클라이언트",
            "google.generativeai": "Google Gemini API",
            "rich": "터미널 렌더링",
            "textual": "TUI 프레임워크",
            "httpx": "HTTP 클라이언트",
        }
        
        all_installed = True
        for module_name, description in modules.items():
            try:
                import_module(module_name.split(".")[0])
                self.console.print(f"[✅] {module_name:<25} - {description}")
            except ImportError:
                self.console.print(f"[❌] {module_name:<25} - {description} [RED](설치 필요)[/RED]")
                all_installed = False
        
        if all_installed:
            self.console.print("[green]✅ 모든 의존성 설치됨![/green]")
        else:
            self.console.print("\n[yellow]설치 명령:[/yellow]")
            self.console.print("pip install groq google-generativeai rich textual httpx")
    
    def _check_saved_config(self):
        """저장된 설정 확인"""
        self.console.print("\n" + "="*60)
        self.console.print("⚙️ 저장된 설정 확인")
        self.console.print("="*60 + "\n")
        
        config_file = get_config_file()
        
        if config_file.exists() and self.config:
            self.console.print(f"[✅] 설정 파일 발견: {config_file}\n")
            
            config_table = Table(show_header=False, box=None)
            config_table.add_column("설정", style="cyan")
            config_table.add_column("값", style="green")
            
            config_table.add_row("[INFO] llm_provider", self.config.get("llm_provider", "N/A"))
            config_table.add_row("[INFO] llm_model", self.config.get("llm_model", "N/A"))
            
            if self.config.get("groq_api_key"):
                masked_key = self.config["groq_api_key"][:10] + "..."
                config_table.add_row("[INFO] groq_api_key", masked_key)
            
            if self.config.get("gemini_api_key"):
                masked_key = self.config["gemini_api_key"][:10] + "..."
                config_table.add_row("[INFO] gemini_api_key", masked_key)
            
            if self.config.get("perplexity_api_key"):
                masked_key = self.config["perplexity_api_key"][:10] + "..."
                config_table.add_row("[INFO] perplexity_api_key", masked_key)
            
            self.console.print(config_table)
        else:
            self.console.print("[yellow]⚠️ 저장된 설정이 없습니다.[/yellow]")
            self.console.print("\n[yellow]메인 프로그램 실행 시 Setup 마법사가 자동으로 시작됩니다.[/yellow]")
    
    def _test_apis(self):
        """API 테스트"""
        self.console.print("\n" + "="*60)
        self.console.print("🧪 API 테스트")
        self.console.print("="*60 + "\n")
        
        if not self.config:
            self.console.print("[yellow]⚠️ 저장된 설정이 없어 API 테스트를 건너뜁니다.[/yellow]")
            return
        
        self.console.print("테스트할 API를 선택하세요:\n")
        self.console.print("1) Groq API 테스트")
        self.console.print("2) Google Gemini API 테스트")
        self.console.print("3) Perplexity API 테스트")
        self.console.print("4) 모두 테스트")
        self.console.print("5) 테스트 건너뛰기\n")
        
        choice = input("선택 (기본: 5) > ").strip() or "5"
        
        if choice in ["1", "4"]:
            self._test_groq()
        if choice in ["2", "4"]:
            self._test_gemini()
        if choice in ["3", "4"]:
            self._test_perplexity()
    
    def _test_groq(self):
        """Groq API 테스트"""
        self.console.print("\n" + "="*60)
        self.console.print("🧪 Groq API 테스트")
        self.console.print("="*60 + "\n")
        
        api_key = self.config.get("groq_api_key")
        if not api_key:
            self.console.print("[⚠️] Groq API 키가 설정되지 않음.\n")
            return
        
        try:
            from groq import Groq
            
            self.console.print("[INFO] Groq 클라이언트 초기화 중...")
            client = Groq(api_key=api_key)
            
            self.console.print("[INFO] 테스트 요청 전송 중...")
            completion = client.chat.completions.create(
                model=self.config.get("llm_model", "openai/gpt-oss-120b"),
                messages=[{"role": "user", "content": "안녕하세요"}],
                max_completion_tokens=100
            )
            
            response_text = completion.choices[0].message.content
            self.console.print(f"[✅] 응답 받음: {response_text[:100]}")
        
        except Exception as e:
            self.console.print(f"[❌] Groq API 테스트 실패: {e}")
    
    def _test_gemini(self):
        """Google Gemini API 테스트"""
        self.console.print("\n" + "="*60)
        self.console.print("🧪 Google Gemini API 테스트")
        self.console.print("="*60 + "\n")
        
        api_key = self.config.get("gemini_api_key")
        if not api_key:
            self.console.print("[⚠️] Gemini API 키가 설정되지 않음.\n")
            return
        
        try:
            import google.generativeai as genai
            
            self.console.print("[INFO] Gemini 클라이언트 초기화 중...")
            genai.configure(api_key=api_key)
            
            self.console.print("[INFO] 테스트 요청 전송 중...")
            model = genai.GenerativeModel(self.config.get("llm_model", "gemini-2.0-flash"))
            response = model.generate_content("안녕하세요")
            
            self.console.print(f"[✅] 응답 받음: {response.text[:100]}")
        
        except Exception as e:
            self.console.print(f"[❌] Gemini API 테스트 실패: {e}")
    
    def _test_perplexity(self):
        """Perplexity API 테스트"""
        self.console.print("\n" + "="*60)
        self.console.print("🧪 Perplexity API 테스트")
        self.console.print("="*60 + "\n")
        
        api_key = self.config.get("perplexity_api_key")
        if not api_key:
            self.console.print("[⚠️] Perplexity API 키가 설정되지 않음.\n")
            return
        
        try:
            import httpx
            
            self.console.print("[INFO] Perplexity 요청 전송 중...")
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "pplx-7b-online",
                "messages": [{"role": "user", "content": "안녕하세요"}],
                "max_tokens": 100
            }
            
            response = httpx.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result["choices"][0]["message"]["content"]
                self.console.print(f"[✅] 응답 받음: {response_text[:100]}")
            else:
                self.console.print(f"[❌] Perplexity API 오류: {response.status_code}")
        
        except Exception as e:
            self.console.print(f"[❌] Perplexity 테스트 실패: {e}")
    
    def _test_additional_features(self):
        """추가 기능 테스트"""
        self.console.print("\n" + "="*60)
        self.console.print("🧪 추가 기능 테스트")
        self.console.print("="*60 + "\n")
        
        self.console.print("1) 시나리오 생성 테스트")
        self.console.print("2) 건너뛰기\n")
        
        choice = input("선택 (기본: 2) > ").strip() or "2"
        
        if choice == "1":
            self._test_scenario()
    
    def _test_scenario(self):
        """시나리오 생성 테스트"""
        self.console.print("\n[INFO] 시나리오 생성 테스트 시작...\n")
        
        if not self.config or not self.config.get("groq_api_key"):
            self.console.print("[yellow]⚠️ Groq API 키가 설정되지 않아 테스트를 건너뜁니다.[/yellow]")
            return
        
        try:
            from groq import Groq
            
            client = Groq(api_key=self.config["groq_api_key"])
            
            completion = client.chat.completions.create(
                model=self.config.get("llm_model", "openai/gpt-oss-120b"),
                messages=[{
                    "role": "user",
                    "content": "폴더 크기를 확인하고 싶어. 단계별 명령어를 JSON 형식으로 3단계 정도만 만들어줘."
                }],
                max_completion_tokens=500
            )
            
            scenario = completion.choices[0].message.content
            self.console.print("[✅] 시나리오 생성 성공:\n")
            self.console.print(scenario)
        
        except Exception as e:
            self.console.print(f"[❌] 시나리오 생성 실패: {e}")
    
    def _show_completion(self):
        """테스트 완료"""
        self.console.print("\n" + "="*60)
        self.console.print("✅ 테스트 완료")
        self.console.print("="*60 + "\n")
        
        self.console.print("[yellow]다음 단계:[/yellow]\n")
        self.console.print("1. 메인 프로그램 실행:")
        self.console.print("   [cyan]python gemini_tutor_app_v2.1.py[/cyan]\n")
        self.console.print("[green]Happy Learning! 🚀[/green]\n")


# ============================================================================
# Main
# ============================================================================

def main():
    """메인 함수"""
    tool = GeminiTutorSetupTool()
    tool.run()


if __name__ == "__main__":
    main()
